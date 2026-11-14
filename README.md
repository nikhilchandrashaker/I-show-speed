# Touring Into Scale: IShowSpeed Social Media Analytics

A small, reproducible case study of IShowSpeed's YouTube growth (2021 to 2026), centered on subscriber milestones and his global livestream tours. It includes a documented dataset, four simple models, five figures, and a short research paper.

**Live dashboard:** see the published artifact link in the chat
**Paper:** [`paper/IShowSpeed_Rise_Paper.pdf`](paper/IShowSpeed_Rise_Paper.pdf)

## Key findings

| Finding | Value |
|---|---|
| YouTube subscribers (Nov 9, 2026, vidIQ) | about 62.3M |
| Years per +10M subs, 1M to 30M | about 1.1 (steady) |
| Years per +10M subs, 30M to 50M / 50M to 60M | 0.67 / 0.52 |
| Post-2024 linear growth | about 14.7M subs/yr (R2 = 0.99) |
| Net adds per day: tour windows vs non-tour baseline | 80K to 200K vs about 21K |
| 100M date, post-2024 trend vs recent baseline pace | about 2029 vs about 2031 |

## Repository layout

```
analysis.py        builds the CSVs, fits the models, writes figures + results.json
build_paper.py     builds the PDF from results.json, data/ and figures/
data/              datasets (CSV)
figures/           fig1-fig5 (PNG)
paper/             final PDF
results.json       model outputs used in the paper
```

## Dataset

| File | Rows | Contents |
|---|---|---|
| `youtube_subscribers.csv` | 18 | Dated YouTube subscriber milestones (millions) with decimal-year dates and confidence |
| `other_platforms.csv` | 5 | TikTok and Instagram follower snapshots |
| `tours.csv` | 4 | Tour windows and a non-tour baseline: days, subs gained, subs per day |
| `career_timeline.csv` | 7 | Career events by year and category |
| `sources.csv` | 12 | Source names and URLs |

Every row that depends on a date or a disputed figure carries a `date_confidence` flag (`high`, `medium`, `low`).

## Models

1. **Milestone velocity (M1):** years elapsed per +10M subscribers between dated milestones.
2. **Growth regimes (M2):** log-linear fit before Sept 2024, OLS after.
3. **Tour vs baseline (M3):** net adds per day in tour windows relative to a 28-day non-tour baseline.
4. **Run-rate projections (M4):** date at which 100M is reached under two assumed rates.

## Run it

```bash
pip install pandas numpy matplotlib reportlab pillow
python analysis.py
python build_paper.py
```

## Limitations (read before citing)

- Only 18 milestone points, 5 other-platform snapshots and 4 tour windows; no daily series. Models are descriptive, not predictive or causal.
- Figures come from public reporting, not platform APIs, and can be revised.
- The 35M South America point has no stated date; its tour window is approximate (about 1.2M gained over roughly two weeks).
- Tour windows were chosen after the fact and are the highest-attention periods; the baseline is from a different year and audience size, so multiples are indicative only.
- The 100M projections assume constant rates and ignore new tours and saturation.

## Suggested next steps

- Replace milestones with daily subscriber data from a tracking service.
- Add exact tour start and end dates from his streams, plus Google Trends interest.
- Compare against other large streamers (for example, the Kai Cenat dataset) with a common baseline.

## Author

Nikhil Chandrashaker, Data Science, California Lutheran University
