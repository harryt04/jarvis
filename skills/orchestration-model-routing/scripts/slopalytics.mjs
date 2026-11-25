#!/usr/bin/env node
// Prints slopalytics.com benchmark rows for named models at named effort levels.
// The site is a JavaScript app that holds its data in the bundle, so a plain page fetch returns no
// numbers. This reads the bundle as text and never evaluates it.

import { pathToFileURL } from 'node:url';

export const SITE = 'https://slopalytics.com';
const PAGE_BYTES = 256 * 1024, BUNDLE_BYTES = 8 * 1024 * 1024, TIMEOUT_MS = 20_000, RECORD_CHARS = 6000;
const BUNDLE_PATH = /<script\b[^>]*\bsrc="(\/assets\/[A-Za-z0-9_.-]+\.js)"/;
const RECORD_START = /\{id:`([a-z0-9.-]+)`,family:`([a-z0-9.-]+)`/g;
const DEFAULT_LABS = ['anthropic', 'openai', 'google'];
const SORTS = { intelligence: 'intelligence', coding: 'coding', cost: 'cost', time: 'seconds' };

// The harness says gpt-6.2-sol; the site says gpt-6-2-sol.
export const normalize = name => String(name).trim().toLowerCase().replace(/[.\s_]+/g, '-');

export function findBundlePath(html) {
  return BUNDLE_PATH.exec(html)?.[1] ?? null;
}

const text = (source, key) => new RegExp(`(?<![A-Za-z])${key}:\`([^\`]*)\``).exec(source)?.[1] ?? null;
function number(source, key) {
  // Minified numbers drop the leading zero: cost:.41
  const raw = new RegExp(`(?<![A-Za-z])${key}:(-?(?:[0-9]|\\.[0-9])[0-9.e+-]*|null)`).exec(source)?.[1];
  if (raw == null || raw === 'null') return null;
  const value = Number(raw);
  return Number.isFinite(value) ? value : null;
}

function recordAt(source, start) {
  let depth = 0;
  const end = Math.min(source.length, start + RECORD_CHARS);
  for (let at = start; at < end; at += 1) {
    if (source[at] === '{') depth += 1;
    else if (source[at] === '}' && (depth -= 1) === 0) return source.slice(start, at + 1);
  }
  return null;
}

export function parseBundle(source) {
  const rows = [];
  for (const match of source.matchAll(RECORD_START)) {
    const record = recordAt(source, match.index);
    if (!record) continue;
    const [top, code = ''] = record.split(',code:{');
    rows.push({
      id: match[1], family: match[2], name: text(top, 'name') ?? match[2], lab: text(top, 'lab'),
      effort: text(top, 'effort') ?? 'default', released: text(top, 'released'),
      deprecated: /(?<![A-Za-z])deprecated:!0/.test(top),
      intelligence: number(top, 'intelligence'), coding: number(code, 'intelligence'),
      cost: number(top, 'cost'), tokens: number(top, 'tokens'), seconds: number(top, 'time'),
      tokensPerSecond: number(top, 'speed'), inputPrice: number(top, 'inputPrice'), outputPrice: number(top, 'outputPrice'),
    });
  }
  return { fetchedAt: /fetchedAt:`([^`]+)`/.exec(source)?.[1] ?? null, rows };
}

export function selectRows(rows, { models = [], efforts = ['medium'], labs = DEFAULT_LABS, sort = 'intelligence', limit = 40 } = {}) {
  const wanted = models.map(normalize).filter(Boolean);
  const anyEffort = efforts.includes('all');
  const matches = (row, model) => row.family === model || row.id === model || normalize(row.name) === model;
  let picked = rows.filter(row => anyEffort || efforts.includes(row.effort));
  picked = wanted.length
    ? picked.filter(row => wanted.some(model => matches(row, model)))
    : picked.filter(row => !row.deprecated && labs.includes(row.lab));
  const missing = wanted.filter(model => !rows.some(row => matches(row, model)));
  const key = SORTS[sort] ?? SORTS.intelligence;
  const ascending = key === 'cost' || key === 'seconds';
  picked.sort((a, b) => {
    if (a[key] == null) return b[key] == null ? 0 : 1;
    if (b[key] == null) return -1;
    return ascending ? a[key] - b[key] : b[key] - a[key];
  });
  return { rows: wanted.length ? picked : picked.slice(0, limit), missing };
}

const cell = (value, digits) => (value == null ? 'n/a' : value.toFixed(digits));
const money = value => (value == null ? 'n/a' : `$${value.toFixed(2)}`);

export function formatTable({ fetchedAt, rows, missing }) {
  const lines = [
    `slopalytics.com (Artificial Analysis data), site snapshot fetched ${fetchedAt ?? 'at an unknown time'}`,
    'Cost and seconds are per benchmark task. A score is comparable only at the effort level shown.',
    '',
    '| Model | Effort | Intelligence | Coding | Cost per task | Seconds per task | Tokens per second | Price in/out per MTok |',
    '| --- | --- | --- | --- | --- | --- | --- | --- |',
    ...rows.map(row => `| ${row.name} | ${row.effort} | ${cell(row.intelligence, 1)} | ${cell(row.coding, 1)} | ${money(row.cost)} | ${cell(row.seconds, 0)} | ${cell(row.tokensPerSecond, 0)} | ${money(row.inputPrice)} / ${money(row.outputPrice)} |`),
  ];
  if (!rows.length) lines.push('| (no rows matched) | | | | | | | |');
  for (const model of missing) lines.push(`Not on the site: ${model}. Do not guess its score; say it is unbenchmarked.`);
  return lines.join('\n');
}

async function fetchText(url, maxBytes) {
  if (!url.startsWith(`${SITE}/`)) throw new Error(`refusing to fetch outside ${SITE}: ${url}`);
  const response = await fetch(url, { signal: AbortSignal.timeout(TIMEOUT_MS), redirect: 'error', headers: { 'user-agent': 'model-routing-reader' } });
  if (!response.ok) throw new Error(`${url} returned HTTP ${response.status}`);
  const body = Buffer.from(await response.arrayBuffer());
  if (body.byteLength > maxBytes) throw new Error(`${url} is ${body.byteLength} bytes; the limit is ${maxBytes}`);
  return body.toString('utf8');
}

export async function readSite() {
  const path = findBundlePath(await fetchText(`${SITE}/`, PAGE_BYTES));
  if (!path) throw new Error('no /assets/*.js bundle found in the page');
  const parsed = parseBundle(await fetchText(`${SITE}${path}`, BUNDLE_BYTES));
  if (!parsed.rows.length) throw new Error('the bundle holds no model records in the expected shape');
  return parsed;
}

export function parseArgs(argv) {
  const options = { models: [], efforts: ['medium'], labs: DEFAULT_LABS, sort: 'intelligence', limit: 40, json: false, help: false };
  const list = value => String(value ?? '').split(',').map(part => part.trim().toLowerCase()).filter(Boolean);
  for (let at = 0; at < argv.length; at += 1) {
    const flag = argv[at];
    if (flag === '--json') options.json = true;
    else if (flag === '--help' || flag === '-h') options.help = true;
    else if (flag === '--models') options.models = list(argv[++at]);
    else if (flag === '--effort') options.efforts = list(argv[++at]);
    else if (flag === '--labs') options.labs = list(argv[++at]);
    else if (flag === '--sort') options.sort = String(argv[++at] ?? '').toLowerCase();
    else if (flag === '--limit') options.limit = Math.max(1, Math.min(200, Number(argv[++at]) || 40));
    else throw new Error(`unknown argument: ${flag}`);
  }
  if (!options.efforts.length) throw new Error('--effort needs a value such as medium, low,medium or all');
  if (!(options.sort in SORTS)) throw new Error(`--sort must be one of ${Object.keys(SORTS).join(', ')}`);
  return options;
}

const HELP = `usage: slopalytics.mjs [--models a,b] [--effort medium|low,high|all] [--sort intelligence|coding|cost|time] [--labs a,b] [--limit n] [--json]
  --models  harness or site model names (claude-opus-5-5, gpt-6.2-sol); every listed model is printed
  --effort  effort levels to print; default medium
  no --models: current models from --labs (default anthropic,openai,google), top --limit by --sort`;

async function main(argv) {
  const options = parseArgs(argv);
  if (options.help) return console.log(HELP);
  const { fetchedAt, rows } = await readSite();
  const selected = selectRows(rows, options);
  console.log(options.json ? JSON.stringify({ source: SITE, fetchedAt, ...selected }, null, 2) : formatTable({ fetchedAt, ...selected }));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main(process.argv.slice(2)).catch(error => {
    console.error(`slopalytics: ${error.message}`);
    console.error('No live numbers. Use the dated snapshot the skill points to, and tell the developer it is dated.');
    process.exit(1);
  });
}
