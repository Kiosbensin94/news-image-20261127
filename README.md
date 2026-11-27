[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![make.fun rank](https://make.fun/badge/news-image-20261127/Kiosbensin94/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![make.fun reward](https://make.fun/badge/news-image-20261127/Kiosbensin94/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

# The World Today — 27 November 2026

Entry for the [make.fun bounty "Sum up 27 November's world news in one image"](https://make.fun/bounty/news-image-20261127) ($100, 50 places paid).

## The image

A newspaper front page, "THE WORLD TODAY — 27 NOVEMBER 2026", summarising Friday 27 November 2026's world news — 33 stories from 7 regions and 15 sources:

- **Main headlines:** drones kill 2 Italian technicians in Kuwait (Iran blamed, Tehran denies) · 10 killed in Gaza despite the ceasefire · Thanksgiving nor'easter grounds the 100th Macy's parade for the first time
- **The day in brief:** Kyiv hit by ballistic missiles, grain ships attacked off Odesa, Houthis claim a Saudi refinery hit, two tankers hit by mines, Bangkok refinery blast, EU split over a €45bn Ukraine loan, Spain's de Cos to lead the ECB, UK migration lowest since 1997, Kim vows more nuclear arms, Guinea-Bissau vote delayed to 2028
- **Also on 27 November:** Depardieu ordered to stand trial, tanker capsizes off Ibiza, New Zealand's final count due, Venezuela bridge loan, Gukesh–Sindarov title draw, Black Friday markets, Neuralink FDA clearance, and more
- **Where it happened:** world map with numbered pins · **The day in UTC** timeline · **Date check:** stories deliberately left out because they are not 27 November news

The image is drawn, not photographed: every word is typeset, so nothing is garbled.

## How it works

`main.ts` (Node 22, standard library only, no network) copies the bundled `entry.png` (1024×1024, under 1 MiB) to `/output/entry.png` and verifies the copy is byte-identical (SHA256 checked). Running it twice writes the same bytes.

## Files

- `main.ts` — the entry program
- `entry.png` — the newspaper front page (1024×1024 PNG)
- `LICENSE` — MIT
