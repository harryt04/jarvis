# Benchmark snapshot

A dated copy of slopalytics.com for the times the live read fails. The site fetched this data on
2026-11-18. Tell the developer that date whenever you use this page.

All rows are at **medium** effort. Cost and seconds are per benchmark task.

| Model | Intelligence | Coding | Cost per task | Seconds per task |
| --- | --- | --- | --- | --- |
| Gemini 4 Carbon | 58.3 | 47.9 | $4.16 | 1777 |
| GPT-6.2 Astra | 57.0 | 51.4 | $1.62 | 270 |
| Fable 5.2 | 56.4 | 46.8 | $3.80 | 385 |
| Gemini 4 Neon | 54.9 | 44.0 | $1.90 | 496 |
| GPT-6.2 Sol | 52.7 | 47.3 | $0.41 | 195 |
| Opus 5.5 | 48.2 | 40.9 | $2.45 | 412 |
| Gemini 4 Hydrogen | 41.2 | 30.6 | $0.80 | 246 |
| GPT-6.1 Terra | 38.2 | 33.7 | $0.17 | 175 |
| Sonnet 5.5 | 30.8 | 18.5 | $0.78 | 224 |
| Haiku 5.5 | 24.6 | 15.7 | $0.09 | 239 |
| GPT-6 Luna | 18.5 | 8.7 | $0.04 | 209 |

What these numbers said on that date (inference, not a measured bake-off):

- GPT-6.2 Sol at medium had the best score per dollar and was the fastest of the strong models.
- At high effort: GPT-6.2 Astra 60.1 / 52.3 at $2.07, Gemini 4 Neon 59.6 / 50.6 at $3.74, Fable 5.2
  61.8 / 53.3 at $9.08.
- Claude needed effort: Opus 5.5 scored 48.2 at medium and 57.4 at xhigh; Sonnet 5.5 scored 30.8 at
  medium and 49.9 at xhigh.
- For cheap bulk work GPT-6.1 Terra at low (29.4 at $0.07) outscored Haiku 5.5 at medium.
- Gemini 4 Carbon took about 30 minutes per task.
