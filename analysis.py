"""IShowSpeed rise: builds datasets, fits simple models, writes figures + results.json."""
import json, os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R = os.path.dirname(os.path.abspath(__file__)); D, F = f"{R}/data", f"{R}/figures"
os.makedirs(D, exist_ok=True); os.makedirs(F, exist_ok=True)

# ---------- DATASETS (compiled from public reporting; see data/sources.csv) ----------
yt = pd.DataFrame([
 ["Apr 2021",2021.29,0.10,"medium","Wikipedia mirror / Malay Mail"],["Jun 30 2021",2021.49,1.0,"high","esports.gg"],
 ["Jul 2022",2022.54,10.0,"medium","Wikipedia mirror / win.gg"],["Aug 2023",2023.62,20.0,"high","Wikipedia mirror / Malay Mail"],
 ["Jun 2 2024",2024.42,25.0,"medium","Wikipedia mirror"],["Aug 2024",2024.65,28.2,"medium","Express Tribune (Aug 24, 2024)"],
 ["Sep 16 2024",2024.71,30.0,"high","Sportskeeda / Deltias"],["Sep 24 2024",2024.73,32.0,"high","Sportskeeda"],
 ["Late 2024",2024.95,35.0,"low","Deltias (South America tour; exact date not given)"],["Sep 2025",2025.70,44.0,"medium","FOX LA (Speed Does America)"],
 ["Nov 2025",2025.87,46.0,"medium","streamer.guide"],["Jan 11 2026",2026.03,48.0,"high","The Star Kenya / ITWeb"],
 ["Jan 21 2026",2026.06,50.06,"high","Multiple (50,058,386 on Jan 22)"],["Mar 2026",2026.22,51.5,"medium","Wikipedia mirror (Mar 20, 2026)"],
 ["Jun 2026",2026.45,55.0,"medium","The Star (World Cup opener, Jun 16, 2026)"],["Jul 31 2026",2026.58,60.0,"high","win.gg"],
 ["Sep 12 2026",2026.70,61.3,"medium","elev8or"],["Nov 9 2026",2026.86,62.3,"high","vidIQ"],
], columns=["label","t_decimal_year","youtube_subs_m","date_confidence","source"])
oth = pd.DataFrame([
 ["TikTok","Sep 2024",2024.72,30.5,"medium","Malay Mail"],["TikTok","Jan 2026",2026.07,47.0,"medium","People of Color in Tech"],["TikTok","Sep 2026",2026.70,54.3,"medium","elev8or"],
 ["Instagram","Sep 2024",2024.72,24.3,"medium","Malay Mail"],["Instagram","Jan 2026",2026.07,45.0,"medium","People of Color in Tech"],
], columns=["platform","label","t_decimal_year","followers_m","date_confidence","source"])
tours = pd.DataFrame([
 ["Speed Does Asia (SE Asia)","2024-09-09","2024-09-24",15,3.0,None,"medium","Window Sep 9-24 only (~29M to 32M); 1M concurrent viewers in Indonesia reported"],
 ["Speed Does South America","2024/25 (date unclear)",None,15,1.2,None,"low","11 countries, 'over two weeks'; days approximate"],
 ["Speed Does Africa","2025-12-29","2026-01-25",28,4.0,None,"medium","20 countries; 'nearly 4M' in about a month; +360K on first Kenya day; 48M to 50M in 10 days"],
 ["Baseline (non-tour, Oct 13 - Nov 9 2026)","2026-10-13","2026-11-09",28,0.6,None,"high","vidIQ 28-day gain"],
], columns=["tour","start","end","days","subs_gained_m","subs_per_day_k","date_confidence","notes"])
tours["subs_per_day_k"] = (tours.subs_gained_m * 1000 / tours.days).round(1)
tl = pd.DataFrame([[2016,"YouTube channel created (Mar 21)","YouTube"],[2021,"100K subs in April, 1M by June 30","Growth"],
 [2022,"10M subs (Jul); Streamy Breakout Streamer","Award"],[2023,"20M subs (Aug); meets Cristiano Ronaldo","Collab"],
 [2024,"Euro 2024 tour; 30M (Sep) during Asia tour; Streamer Awards Streamer of the Year","Tour"],[2025,"China and America tours; Streamer Awards Streamer of the Year (reported)","Tour"],
 [2026,"Africa tour (20 countries); 50M on Jan 21; 60M on Jul 31; 62.3M by Nov 9","Record"]], columns=["year","event","category"])
src = pd.DataFrame([["vidIQ","https://vidiq.com/youtube-stats/channel/UCWsDFcIhY2DBi3GB5uykGXA"],["esports.gg","https://esports.gg/news/streamers/ishowspeed-50-million-subscribers"],
 ["win.gg (60M)","https://win.gg/ishowspeed-60-million-youtube-subscribers-falls-with-balloons/"],["win.gg (profile)","https://win.gg/who-is-ishowspeed/"],
 ["The Star Kenya (55M)","https://www.the-star.co.ke/news/2026-06-16-speed-hits-55-million-at-usa-vs-paraguay-match"],["ITWeb Africa","https://itweb.africa/article/youtube-sensation-ishowspeed-hits-48-million-views/mQwkoq6YlOJM3r9A"],
 ["Sportskeeda (32M)","https://www.sportskeeda.com/us/streamers/news-ishowspeed-celebrates-reaching-32-million-subscribers-bungee-jumping-stream"],["Deltias (South America)","https://deltiasgaming.com/?p=130549"],
 ["Malay Mail","https://malaymail.com/news/life/2024/09/18/he-has-over-60m-followers-on-social-media-but-how-did-ishowspeed-get-so-popular-heres-the-lowdown-video/150772"],
 ["Streamer.guide","https://streamer.guide/blog/ishowspeed-50-million-youtube-subscribers"],["elev8or","https://www.elev8or.io/i/ishowspeed-bio"],["FOX LA","https://www.foxla.com/news/list-spots-ishowspeed-checked-out-during-sept-2025-los-angeles-visit"]],columns=["source","url"])
for n, d in dict(youtube_subscribers=yt, other_platforms=oth, tours=tours, career_timeline=tl, sources=src).items(): d.to_csv(f"{D}/{n}.csv", index=False)

# ---------- MODELS ----------
t, y = yt.t_decimal_year.values, yt.youtube_subs_m.values; res = {}
g = lambda lab: float(yt.loc[yt.label == lab, "t_decimal_year"].iloc[0])
steps = [("1M","10M",g("Jun 30 2021"),g("Jul 2022"),9),("10M","20M",g("Jul 2022"),g("Aug 2023"),10),("20M","30M",g("Aug 2023"),g("Sep 16 2024"),10),("30M","50M",g("Sep 16 2024"),g("Jan 21 2026"),20),("50M","60M",g("Jan 21 2026"),g("Jul 31 2026"),10)]
res["years_per_10m"] = {f"{a} to {b}": (t1 - t0) / n * 10 for a, b, t0, t1, n in steps}
pre = t <= 2024.75; post = t >= 2024.7
res["early_ln_slope"] = float(np.polyfit(t[(t >= 2021.4) & pre], np.log(y[(t >= 2021.4) & pre]), 1)[0])
b, a = np.polyfit(t[post], y[post], 1); p = a + b * t[post]
res["late_slope_m_per_yr"] = float(b); res["late_r2"] = float(1 - ((y[post] - p) ** 2).sum() / ((y[post] - y[post].mean()) ** 2).sum())
res["ytd_2026_m_per_yr"] = float((62.3 - 50.06) / (2026.86 - 2026.06))
tp = tours.set_index("tour").subs_per_day_k; base = float(tp["Baseline (non-tour, Oct 13 - Nov 9 2026)"])
res["tour_per_day_k"] = {k: float(v) for k, v in tp.items()}; res["baseline_per_day_k"] = base
res["tour_multiples"] = {k: float(v / base) for k, v in tp.items() if not k.startswith("Baseline")}
res["kenya_day_multiple"] = 360 / base
res["baseline_m_per_yr"] = 0.6 * 365 / 28
need = 100 - 62.3
res["scen"] = {"baseline": 2026.86 + need / res["baseline_m_per_yr"], "post2024_trend": 2026.86 + need / res["late_slope_m_per_yr"]}
res["views_per_new_sub_28d"] = 349.8e6 / 0.6e6; res["views_per_sub_total"] = 11479e6 / 62.3e6
res["yt_tt_total_m"] = 62.3 + 54.3
json.dump(res, open(f"{R}/results.json", "w"), indent=2)

# ---------- FIGURES ----------
P, T, O, G = "#dc2626", "#1e3a8a", "#ca8a04", "#888888"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
f, ax = plt.subplots(figsize=(6.8, 3.8)); ax.plot(t, y, "o-", color=P, ms=4)
for lab, yy in [("1M",1),("10M",10),("20M",20),("30M",30),("50M",50.06),("60M",60)]:
    tt = {"1M":g("Jun 30 2021"),"10M":g("Jul 2022"),"20M":g("Aug 2023"),"30M":g("Sep 16 2024"),"50M":g("Jan 21 2026"),"60M":g("Jul 31 2026")}[lab]; ax.annotate(lab, (tt, yy), textcoords="offset points", xytext=(-14, 6), fontsize=8)
ax.axvspan(2025.99, 2026.07, color=O, alpha=.25, label="Africa tour (Jan 2026)"); ax.set_xlabel("Year"); ax.set_ylabel("YouTube subscribers (millions)"); ax.legend(frameon=False, fontsize=8)
ax.set_title("Fig. 1: YouTube subscriber milestones"); f.tight_layout(); f.savefig(f"{F}/fig1_growth.png", dpi=200); plt.close()
f, ax = plt.subplots(figsize=(6.4, 3.5)); k = list(res["years_per_10m"]); v = list(res["years_per_10m"].values())
bb = ax.bar([s.replace(" to ", "\nto ") for s in k], v, color=P)
for r_, x in zip(v, bb): ax.text(x.get_x() + x.get_width() / 2, r_ + .02, f"{r_:.2f}", ha="center", fontsize=9)
ax.set_ylabel("Years per +10M subscribers"); ax.set_ylim(0, 1.35); ax.set_title("Fig. 2: Milestone velocity"); f.tight_layout(); f.savefig(f"{F}/fig2_velocity.png", dpi=200); plt.close()
f, ax = plt.subplots(figsize=(6.6, 3.6)); nm = ["Baseline\n(Oct-Nov 2026)", "South America", "Africa", "SE Asia"]; vv = [base, tp["Speed Does South America"], tp["Speed Does Africa"], tp["Speed Does Asia (SE Asia)"]]
bb = ax.bar(nm, vv, color=[G, O, O, O])
for r_, x in zip(vv, bb): ax.text(x.get_x() + x.get_width() / 2, r_ + 3, f"{r_:.0f}K", ha="center", fontsize=9)
ax.set_ylabel("Net new subs per day (thousands)"); ax.set_title("Fig. 3: Tour windows vs non-tour baseline"); f.tight_layout(); f.savefig(f"{F}/fig3_tours.png", dpi=200); plt.close()
f, ax = plt.subplots(figsize=(6.8, 3.7)); tt = np.linspace(2026.86, 2033, 50)
ax.plot(t, y, "o-", color=P, ms=3, label="Observed")
ax.plot(tt, 62.3 + res["late_slope_m_per_yr"] * (tt - 2026.86), "--", color=O, label=f"Post-2024 trend ({res['late_slope_m_per_yr']:.1f}M/yr)")
ax.plot(tt, 62.3 + res["baseline_m_per_yr"] * (tt - 2026.86), "--", color=G, label=f"Oct 2026 baseline ({res['baseline_m_per_yr']:.1f}M/yr)")
ax.axhline(100, color="black", lw=.8, ls=":"); ax.text(2021.3, 102, "100M (stated goal)", fontsize=8); ax.set_ylim(0, 112); ax.set_xlabel("Year"); ax.set_ylabel("Subscribers (millions)")
ax.legend(frameon=False, fontsize=8, loc="center left"); ax.set_title("Fig. 4: Time to 100M under two run-rates (illustrative)"); f.tight_layout(); f.savefig(f"{F}/fig4_scenarios.png", dpi=200); plt.close()
f, ax = plt.subplots(figsize=(7.4, 2.8)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 3)
nodes = ["Unfiltered\nlivestreams", "Viral clips +\ncelebrity meets", "Global IRL\ntours", "Local-fan\nsub surges", "Records, press,\nbrand deals", "Bigger next\ntour"]
for i, n in enumerate(nodes):
    x = 0.1 + i * 1.64; ax.add_patch(FancyBboxPatch((x, 1.0), 1.4, 1.0, boxstyle="round,pad=0.03", fc=P if i in (2, 3) else "#fee2e2", ec=P))
    ax.text(x + .7, 1.5, n, ha="center", va="center", fontsize=7.5, color="white" if i in (2, 3) else "black")
    if i < 5: ax.annotate("", xy=(x + 1.62, 1.5), xytext=(x + 1.43, 1.5), arrowprops=dict(arrowstyle="->", color=G))
ax.annotate("", xy=(2.9, 0.9), xytext=(9.0, 0.9), arrowprops=dict(arrowstyle="->", color=O, connectionstyle="arc3,rad=-0.25"))
ax.text(5.9, 0.12, "feedback: each tour's attention funds and justifies the next", ha="center", fontsize=8, color=O)
ax.set_title("Fig. 5: Conceptual growth flywheel (author's synthesis, not estimated)", fontsize=10); f.savefig(f"{F}/fig5_flywheel.png", dpi=200, bbox_inches="tight"); plt.close()
print(json.dumps(res, indent=1))
