"""Builds paper/IShowSpeed_Rise_Paper.pdf from results.json, data/ and figures/."""
import json, os
from PIL import Image as PI
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
R = os.path.dirname(os.path.abspath(__file__)); r = json.load(open(f"{R}/results.json")); ss = getSampleStyleSheet()
B = ParagraphStyle("B", parent=ss["Normal"], fontName="Times-Roman", fontSize=10.5, leading=14, alignment=4, spaceAfter=6)
H = ParagraphStyle("H", parent=ss["Heading2"], fontName="Times-Bold", fontSize=13, spaceBefore=10, spaceAfter=4, keepWithNext=1)
T = ParagraphStyle("T", parent=ss["Title"], fontName="Times-Bold", fontSize=18, leading=22)
C = ParagraphStyle("C", parent=B, fontSize=9, leading=11, alignment=1, textColor=colors.HexColor("#444444"))
S = ParagraphStyle("S", parent=B, fontSize=9.5, leading=12.5, alignment=0, leftIndent=14, firstLineIndent=-14)
def fig(n, w=6.2):
    a, b = PI.open(f"{R}/figures/{n}").size; return Image(f"{R}/figures/{n}", width=w*inch, height=w*inch*b/a)
def tbl(rows, w):
    t = Table(rows, colWidths=w); t.setStyle(TableStyle([("FONT", (0,0), (-1,-1), "Times-Roman", 9), ("FONT", (0,0), (-1,0), "Times-Bold", 9), ("LINEABOVE", (0,0), (-1,0), 1, colors.black), ("LINEBELOW", (0,0), (-1,0), .5, colors.black), ("LINEBELOW", (0,-1), (-1,-1), 1, colors.black)])); return t
vp = r["years_per_10m"]; tm = r["tour_multiples"]; tp = r["tour_per_day_k"]; sc = r["scen"]; yr = lambda x: f"{int(x)}"
s = []; P = lambda t, st=B: s.append(Paragraph(t, st))
P("Touring Into Scale: A Quantitative Analysis of IShowSpeed's YouTube Growth, 2021-2026", T)
P("Nikhil Chandrashaker<br/>Data Science, California Lutheran University<br/>Working paper, November 2026", C)
P("Abstract", H)
P(f"IShowSpeed (Darren Watkins Jr.) grew from 1 million YouTube subscribers in June 2021 to about 62.3 million in November 2026. This paper compiles a small, source-documented dataset of his subscriber milestones, tour-period gains and cross-platform audience, and uses it to ask how his growth changed over time. Milestone velocity was steady at roughly one year per +10M subscribers through September 2024 (1.08 to 1.17 years), then accelerated to {vp['30M to 50M']:.2f} years (30M to 50M) and {vp['50M to 60M']:.2f} years (50M to 60M). Since late 2024, growth is close to linear at about {r['late_slope_m_per_yr']:.1f}M subscribers per year (R<super>2</super> = {r['late_r2']:.2f}). Reported tour windows show net adds of {tp['Speed Does South America']:.0f}K to {tp['Speed Does Asia (SE Asia)']:.0f}K per day, {tm['Speed Does South America']:.1f} to {tm['Speed Does Asia (SE Asia)']:.1f} times a recent non-tour baseline of {r['baseline_per_day_k']:.0f}K per day. Because tour windows were chosen after the fact and figures are approximate, the results are descriptive, not causal.")
P("1. Introduction", H)
P("Most creator growth studies focus on content strategy or platform algorithms. IShowSpeed is a useful counter-case because his audience growth is tied to a physical, event-like format: multi-week livestreamed tours across countries, plus high-profile encounters. Each tour is a natural experiment window, though an imperfect one. This project builds a transparent dataset from public reporting and asks: (i) how fast did he reach each subscriber milestone, (ii) how do tour windows compare with ordinary weeks, and (iii) what does a run-rate projection say about his stated goal of 100 million subscribers.")
P("2. Data and Methods", H)
P("All values come from public reporting (vidIQ, esports.gg, win.gg, The Star Kenya, ITWeb, Sportskeeda and others; see data/sources.csv). No platform API or scraping was used. The dataset has five tables: 18 dated YouTube subscriber points, 5 TikTok/Instagram snapshots, 4 tour or baseline windows, a career timeline and a source list. Each row carries a date-confidence flag. Dates are converted to decimal years; day-level dates are used where reported, otherwise mid-month.")
P("Models. (M1) Milestone velocity: years elapsed per +10M subscribers between dated milestones. (M2) Growth regimes: log-linear fit before September 2024 and ordinary least squares after. (M3) Tour comparison: net subscriber adds per day in reported tour windows relative to a 28-day non-tour baseline (October 13 to November 9, 2026). (M4) Run-rate projections of the date at which 100M would be reached under two assumed rates. All models are simple by design because the milestone series has only 18 points.")
P("3. Results", H)
P("3.1 Growth trajectory and milestone velocity (M1, M2)", H)
s.append(fig("fig1_growth.png", 5.4))
P(f"The channel gained its first million in about two months in 2021 (100K in April, 1M by June 30) and then grew steadily through three successive +10M steps, each taking about 1.1 years (Fig. 2). From September 2024 the pace shortened sharply: 30M to 50M took {vp['30M to 50M']:.2f} years per 10M and 50M to 60M took {vp['50M to 60M']:.2f}, about 0.52 years (about six months). A post-2024 linear fit gives {r['late_slope_m_per_yr']:.1f}M per year with R<super>2</super> = {r['late_r2']:.2f}, and 2026 year-to-date (Jan 21 to Nov 9) averages {r['ytd_2026_m_per_yr']:.1f}M per year. In relative terms growth is slowing (a fixed number of new subscribers is a smaller share of a larger base) while in absolute terms it is faster than ever.")
s.append(fig("fig2_velocity.png", 4.2))
t1 = [["Milestone step", "Years per +10M"]] + [[k, f"{v:.2f}"] for k, v in vp.items()]
s.append(tbl(t1, [2.2*inch, 1.8*inch])); s.append(Spacer(1, 6))
P("3.2 Tour windows versus baseline (M3)", H)
s.append(fig("fig3_tours.png", 5.2))
P(f"Reported tour windows imply net adds of about {tp['Speed Does Asia (SE Asia)']:.0f}K per day in Southeast Asia (Sept 9-24, 2024, about 3M), {tp['Speed Does Africa']:.0f}K per day on the Africa tour (about 4M over roughly 28 days) and about {tp['Speed Does South America']:.0f}K per day in South America (about 1.2M over roughly two weeks). Against a non-tour baseline of {r['baseline_per_day_k']:.0f}K per day (600K in the 28 days to Nov 9, 2026) these are {tm['Speed Does South America']:.1f}x, {tm['Speed Does Africa']:.1f}x and {tm['Speed Does Asia (SE Asia)']:.1f}x. His first day in Kenya alone was reported at over 360K new subscribers, about {r['kenya_day_multiple']:.0f}x the baseline. These windows are the highest-attention periods, chosen after the fact, and the baseline is from a different year and audience size, so the multiples are indicative only.")
P("3.3 Reach and conversion", H)
P(f"As of November 9, 2026, vidIQ lists about 11.48 billion total views, or roughly {r['views_per_sub_total']:.0f} views per subscriber. In the last 28 days he gained about 600K subscribers on about 350M views, roughly {r['views_per_new_sub_28d']:.0f} views per new subscriber. On other platforms he had about 54.3M TikTok followers (Sept 2026) and about 45M Instagram followers (Jan 2026), so YouTube plus TikTok alone is about {r['yt_tt_total_m']:.0f}M. A tracking site reports a YouTube engagement rate of 0.19%, which is low relative to peers; this likely reflects livestream-heavy viewing patterns rather than weak audience quality, but this analysis cannot test that.")
P("3.4 Time to 100 million (M4)", H)
s.append(fig("fig4_scenarios.png", 5.3))
P(f"Speed has said he is aiming for 100M. Extending the post-2024 trend ({r['late_slope_m_per_yr']:.1f}M per year) from 62.3M reaches 100M in about {yr(sc['post2024_trend'])} (mid-year). Extending only the recent non-tour pace (annualized {r['baseline_m_per_yr']:.1f}M per year) reaches it in about {yr(sc['baseline'])}. The gap of more than two years shows how much of his growth depends on tour-style events. This is a sensitivity exercise, not a forecast.")
P("4. Discussion", H)
P("Two patterns stand out. First, growth came in two regimes: a steady period of about one year per 10M subscribers, then a faster period that coincides with the global tour format (Fig. 5). Second, subscriber gains cluster in tour windows and in single viral days, so a few well-timed events plausibly account for a large share of net growth. The data cannot separate the effect of tours from the effect of celebrity encounters, platform promotion, a growing global audience or simple compounding.")
s.append(fig("fig5_flywheel.png", 5.8))
P("5. Limitations", H)
P("The dataset is small and secondhand: 18 YouTube milestone points, 5 other-platform snapshots and 4 tour windows, with no daily series. Several dates are approximate (the 35M South America point has no stated date, and the 2024 Europe tour has no isolated gain). Tour gains are rounded media estimates over windows that may not match actual tour boundaries. Subscriber counts can be revised and may include inactive accounts. The projection assumes constant rates and ignores new tours, platform changes and saturation. A stronger study would use daily subscriber data from a tracking service, tour start and end dates from his own streams, and controls such as other large streamers.")
P("6. Conclusion", H)
P(f"IShowSpeed's YouTube growth moved from a steady one year per 10M subscribers to roughly half that pace, and reported tour windows show several times the ordinary daily gain. Whether 100M arrives around {yr(sc['post2024_trend'])} or well after {yr(sc['baseline'])} depends largely on how often he runs tour-scale events. The accompanying dataset and code are intended as a starting point for a more rigorous replication with daily data.")
P("References", H)
for x in ["vidIQ. IShowSpeed YouTube statistics (as of Nov 9, 2026). vidiq.com/youtube-stats/channel/UCWsDFcIhY2DBi3GB5uykGXA", "esports.gg. IShowSpeed hits 50 million subs.", "win.gg. iShowSpeed hits 60 million YouTube subscribers (Aug 3, 2026).", "The Star (Kenya). Speed hits 55 million at USA vs Paraguay match (Jun 16, 2026).", "ITWeb Africa. YouTube sensation IShowSpeed hits 48 million (Jan 12, 2026).", "Sportskeeda. IShowSpeed celebrates reaching 32 million subscribers (Sept 2024).", "Deltias Gaming. IShowSpeed's South America tour garners 46M views.", "Malay Mail. How did IShowSpeed get so popular (Sept 18, 2024).", "elev8or. IShowSpeed creator profile (checked Sept 12, 2026)."]: P(x, S)
SimpleDocTemplate(f"{R}/paper/IShowSpeed_Rise_Paper.pdf", pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=.9*inch, bottomMargin=.9*inch, title="Touring Into Scale", author="Nikhil Chandrashaker").build(s)
