---
name: catalog
description: Show the Jarvis skill catalog as a Markdown table in chat.
disable-model-invocation: true
---

# Catalog

[`skills/README.md`](../README.md) is the single source of truth for the
catalog. Print its table; leave the wording to the file.

1. Read `../README.md` relative to this skill's directory
   (`skills/README.md` in the Jarvis checkout).
2. Reply with that file's `| Skill | What it does |` table, every row in file
   order, as a Markdown table in the chat. Rewrite each relative link target
   (`agent-browser/SKILL.md`) to the absolute path of that `SKILL.md` so the
   link opens from chat.
3. List every `skills/*/SKILL.md` directory. When one has no row, add one line
   under the table naming it as missing from the catalog.

Done when the reply holds every row of the file's table, and nothing else
beyond the optional missing-skills line.
