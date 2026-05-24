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

with open('figures/problem_1_results.json', 'r') as f:
    data = json.load(f)

hours = np.array(data['power_curves']['hours'])
P_wind = np.array(data['power_curves']['P_wind'])
P_pv = np.array(data['power_curves']['P_pv'])
P_demand = np.array(data['power_curves']['P_demand'])
P_load = np.array(data['power_curves']['P_load'])

P_RE = P_wind + P_pv
P_net = P_RE - P_demand  # net power (positive = surplus)

fig, ax1 = plt.subplots(figsize=(9, 5.5))
ax2 = ax1.twinx()

# Bar chart for wind and PV (stacked)
width = 0.6
bars1 = ax1.bar(hours, P_wind, width=width, color=_lighten(PALETTE[0], 0.4),
                edgecolor=PALETTE[0], linewidth=1.0, label='风电')
bars2 = ax1.bar(hours, P_pv, width=width, bottom=P_wind,
                color=_lighten(PALETTE[1], 0.4), edgecolor=PALETTE[1], linewidth=1.0, label='光伏')

# Demand line on primary axis
ax1.plot(hours, P_demand, 'o-', color=PALETTE[3], linewidth=2.0, markersize=4,
         markeredgecolor='white', markeredgewidth=0.8, label='总用电负荷', zorder=5)

# Net power on secondary axis
ax2.plot(hours, P_net, 's-', color=PALETTE[2], linewidth=2.0, markersize=5,
         markeredgecolor='white', markeredgewidth=1.0, label='净功率', zorder=5)
for layer, alpha in enumerate([0.12, 0.06]):
    ax2.fill_between(hours, 0, P_net, alpha=alpha, color=PALETTE[2], linewidth=0)
ax2.axhline(0, color=COLORS['text'], linewidth=0.8, linestyle='-', alpha=0.5)

# Peak highlight
peak_idx = np.argmax(P_RE)
ax1.scatter(hours[peak_idx], P_RE[peak_idx], s=120, color=PALETTE[1],
            edgecolor='white', linewidth=2, zorder=6)
ax1.annotate(f'峰值 {P_RE[peak_idx]:.1f}MW',
             xy=(hours[peak_idx], P_RE[peak_idx]),
             xytext=(hours[peak_idx]+2, P_RE[peak_idx]+3),
             fontsize=9, fontweight='bold', color=PALETTE[1],
             arrowprops=dict(arrowstyle='->', color=PALETTE[1], lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=PALETTE[1], alpha=0.9))

ax1.set_xlabel('时刻 (h)', fontsize=11)
ax1.set_ylabel('功率 (MW)', fontsize=11, color=COLORS['text'])
ax2.set_ylabel('净功率 (MW)', fontsize=11, color=PALETTE[2])
ax2.tick_params(axis='y', labelcolor=PALETTE[2])
ax1.set_xlim(-0.5, 23.5)
ax1.set_xticks(range(0, 24, 2))

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, frameon=True, edgecolor=COLORS['grid'],
           fontsize=9, loc='upper left')

ax1.spines['top'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_q1_power_detail.pdf')
print("OK: fig_q1_power_detail.pdf")
