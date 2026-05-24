import os, sys, shutil, json
os.makedirs('_utils', exist_ok=True)
for src in ['plot_utils.py']:
    for search in ['skills/shared-scripts', '../skills/shared-scripts']:
        p = os.path.join(search, src)
        if os.path.isfile(p):
            shutil.copy2(p, f'_utils/{src}')
            break
sys.path.insert(0, '.')
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten
setup_style()
import numpy as np
import matplotlib.pyplot as plt

with open('figures/problem_3_results.json', 'r') as f:
    data = json.load(f)
with open('figures/problem_1_results.json', 'r') as f:
    p1_data = json.load(f)

hours = np.arange(24)
P_wind = np.array(p1_data['power_curves']['P_wind'])
P_pv = np.array(p1_data['power_curves']['P_pv'])
P_load = np.array(p1_data['power_curves']['P_load'])
P_RE = P_wind + P_pv

# Get alpha schedule for 45 ton/day (best balance)
alpha_45 = np.array(data['typical_scenario']['45']['alpha'])
# Electrolyzer power: ALKEL 10MW + PEMEL 10MW = 20MW base, scaled by alpha
P_electrolyzer = alpha_45 * 20.0
# Ammonia synthesis: 0.75MW * 2 (scaled for 72 capacity) * alpha
P_ammonia = alpha_45 * 1.5
P_h2_nh3 = P_electrolyzer + P_ammonia
P_total_demand = P_h2_nh3 + P_load

fig, ax = plt.subplots(figsize=(9, 5.5))

# Stacked area: wind + PV generation
for layer, alpha in enumerate([0.30, 0.15]):
    ax.fill_between(hours, 0, P_wind - layer*0.2, alpha=alpha, color=PALETTE[0], linewidth=0)
ax.plot(hours, P_wind, color=PALETTE[0], linewidth=1.2, label='风电')

for layer, alpha in enumerate([0.30, 0.15]):
    ax.fill_between(hours, P_wind, P_RE - layer*0.2, alpha=alpha, color=PALETTE[1], linewidth=0)
ax.plot(hours, P_RE, color=PALETTE[1], linewidth=1.2, label='风电+光伏')

# Demand components
ax.plot(hours, P_load, '--', color=PALETTE[3], linewidth=1.5, label='常规负荷')
ax.plot(hours, P_total_demand, 'o-', color=PALETTE[4], linewidth=2.2, markersize=4,
        markeredgecolor='white', markeredgewidth=0.8, label='总用电负荷', zorder=5)

# Alpha schedule as bar overlay (secondary info)
ax2 = ax.twinx()
ax2.bar(hours, alpha_45, width=0.4, color=_lighten(PALETTE[2], 0.5), edgecolor=PALETTE[2],
        linewidth=0.8, alpha=0.4, label='制氢氨负荷率α')
ax2.set_ylabel('负荷率 α', fontsize=10, color=PALETTE[2])
ax2.set_ylim(0, 1.5)
ax2.tick_params(axis='y', labelcolor=PALETTE[2])

# Combined legend
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, frameon=True, edgecolor=COLORS['grid'],
          fontsize=9, loc='upper left', ncol=2)

ax.set_xlabel('时刻 (h)', fontsize=11)
ax.set_ylabel('功率 (MW)', fontsize=11)
ax.set_xlim(-0.5, 23.5)
ax.set_xticks(range(0, 24, 2))
ax.spines['top'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_q3_dispatch.pdf')
print("OK: fig_q3_dispatch.pdf")
