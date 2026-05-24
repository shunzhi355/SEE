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
P_load = np.array(data['power_curves']['P_load'])
P_wind = np.array(data['power_curves']['P_wind'])
P_pv = np.array(data['power_curves']['P_pv'])
P_demand = np.array(data['power_curves']['P_demand'])
P_buy = np.array(data['power_curves']['P_buy'])
P_sell = np.array(data['power_curves']['P_sell']) if 'P_sell' in data['power_curves'] else np.zeros(24)

P_RE = P_wind + P_pv

fig, ax = plt.subplots(figsize=(9, 5.5))

# Area fills for power generation
for layer, alpha in enumerate([0.30, 0.18, 0.08]):
    ax.fill_between(hours, 0, P_wind - layer*0.3, alpha=alpha, color=PALETTE[0], linewidth=0)
ax.plot(hours, P_wind, color=PALETTE[0], linewidth=1.5, label='风电功率')

for layer, alpha in enumerate([0.30, 0.18, 0.08]):
    ax.fill_between(hours, P_wind + layer*0.3, P_RE - layer*0.3, alpha=alpha, color=PALETTE[1], linewidth=0)
ax.plot(hours, P_RE, color=PALETTE[1], linewidth=1.5, label='风电+光伏')

# Demand line
ax.plot(hours, P_demand, color=PALETTE[3], linewidth=2.2, linestyle='-', label='总用电负荷', zorder=5)

# Buy power area (where demand > RE)
buy_mask = P_demand > P_RE
if buy_mask.any():
    ax.fill_between(hours, P_RE, P_demand, where=buy_mask, alpha=0.2, color=PALETTE[4], linewidth=0)
    ax.fill_between(hours, P_RE, P_demand, where=buy_mask, alpha=0.1, color=PALETTE[4], linewidth=0)

# Sell power area (where RE > demand)
sell_mask = P_RE > P_demand
if sell_mask.any():
    ax.fill_between(hours, P_demand, P_RE, where=sell_mask, alpha=0.2, color=PALETTE[2], linewidth=0)

# Event markers for peak/valley
peak_re_idx = np.argmax(P_RE)
ax.axvline(x=hours[peak_re_idx], color=COLORS['ref_line'], linestyle=':', linewidth=1, alpha=0.6)
ax.text(hours[peak_re_idx]+0.3, P_RE[peak_re_idx]*0.95, f'新能源峰值\n{P_RE[peak_re_idx]:.1f}MW',
        fontsize=8, color=COLORS['ref_line'], va='top',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=COLORS['ref_line'], alpha=0.8, linewidth=0.5))

# Legend patches for buy/sell
from matplotlib.patches import Patch
legend_extra = [
    Patch(facecolor=_lighten(PALETTE[4], 0.3), edgecolor=PALETTE[4], label='购电区间'),
    Patch(facecolor=_lighten(PALETTE[2], 0.3), edgecolor=PALETTE[2], label='售电区间'),
]
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles + legend_extra, frameon=True, edgecolor=COLORS['grid'], fontsize=9, loc='upper left')

ax.set_xlabel('时刻 (h)', fontsize=11)
ax.set_ylabel('功率 (MW)', fontsize=11)
ax.set_xlim(0, 23)
ax.set_xticks(range(0, 24, 2))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_q1_power_balance.pdf')
print("OK: fig_q1_power_balance.pdf")
