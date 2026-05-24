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

with open('figures/problem_2_results.json', 'r') as f:
    data = json.load(f)

productions = [72, 63, 54, 45, 36]
typical = data['typical_scenario']
costs = [typical[str(p)]['C_ton'] for p in productions]

fig, ax = plt.subplots(figsize=(8, 5))
ax.grid(axis='y', alpha=0.12, linestyle='--', color=COLORS['grid'])
ax.set_axisbelow(True)

x = np.arange(len(productions))
width = 0.55

# Alternating row background
for i in range(len(productions)):
    if i % 2 == 0:
        ax.axvspan(x[i]-0.4, x[i]+0.4, alpha=0.03, color=PALETTE[0], zorder=0)

# Bars with gradient intensity based on cost
max_cost = max(costs)
for i, (prod, cost) in enumerate(zip(productions, costs)):
    intensity = cost / max_cost
    c = PALETTE[i % len(PALETTE)]
    bar = ax.bar(x[i], cost, width=width,
                 color=_lighten(c, 0.35), edgecolor=c, linewidth=1.3, zorder=3)
    # Value label on top
    ax.text(x[i], cost + max_cost*0.02, f'¥{cost:.0f}',
            ha='center', va='bottom', fontsize=9, fontweight='bold', color=c)

# Highlight best (lowest cost)
best_idx = np.argmin(costs)
ax.bar(x[best_idx], costs[best_idx], width=width,
       color=_lighten(PALETTE[best_idx], 0.2), edgecolor=PALETTE[best_idx], linewidth=2.5, zorder=4)
ax.annotate('最优', xy=(x[best_idx], costs[best_idx]),
            xytext=(x[best_idx]+0.5, costs[best_idx]+max_cost*0.08),
            fontsize=10, fontweight='bold', color=PALETTE[best_idx],
            arrowprops=dict(arrowstyle='->', color=PALETTE[best_idx], lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor=PALETTE[best_idx], alpha=0.9))

ax.set_xticks(x)
ax.set_xticklabels([f'{p}吨/日' for p in productions], fontsize=10)
ax.set_xlabel('日产量', fontsize=11)
ax.set_ylabel('吨氨成本 (元/吨)', fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_q2_cost_compare.pdf')
print("OK: fig_q2_cost_compare.pdf")
