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

annual_costs = sorted(data['annual_analysis']['annual_cost_curve'])
x = np.arange(1, len(annual_costs)+1)

fig, ax = plt.subplots(figsize=(8, 5))

# Gradient fill
for layer, alpha in enumerate([0.25, 0.15, 0.06]):
    ax.fill_between(x, 0, np.array(annual_costs) - layer*50, alpha=alpha, color=PALETTE[0], linewidth=0)
ax.plot(x, annual_costs, 'o-', color=PALETTE[0], linewidth=2.0, markersize=5,
        markeredgecolor='white', markeredgewidth=1.0, label='问题二（离散调节）')

# Mean line
mean_cost = np.mean(annual_costs)
ax.axhline(mean_cost, color=COLORS['ref_line'], linestyle='--', linewidth=1.2, alpha=0.7)
ax.text(len(annual_costs)*0.85, mean_cost + 100, f'均值 ¥{mean_cost:.0f}/吨',
        fontsize=9, color=COLORS['ref_line'],
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=COLORS['ref_line'], alpha=0.8))

# Min/Max annotations
min_idx = np.argmin(annual_costs)
max_idx = np.argmax(annual_costs)
ax.scatter(x[min_idx], annual_costs[min_idx], s=100, color=PALETTE[2], edgecolor='white', linewidth=2, zorder=6)
ax.annotate(f'最低 ¥{annual_costs[min_idx]:.0f}',
            xy=(x[min_idx], annual_costs[min_idx]),
            xytext=(x[min_idx]+2, annual_costs[min_idx]-300),
            fontsize=9, fontweight='bold', color=PALETTE[2],
            arrowprops=dict(arrowstyle='->', color=PALETTE[2], lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=PALETTE[2], alpha=0.9))

ax.scatter(x[max_idx], annual_costs[max_idx], s=100, color=PALETTE[4], edgecolor='white', linewidth=2, zorder=6)
ax.annotate(f'最高 ¥{annual_costs[max_idx]:.0f}',
            xy=(x[max_idx], annual_costs[max_idx]),
            xytext=(x[max_idx]-3, annual_costs[max_idx]+300),
            fontsize=9, fontweight='bold', color=PALETTE[4],
            arrowprops=dict(arrowstyle='->', color=PALETTE[4], lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=PALETTE[4], alpha=0.9))

ax.set_xlabel('场景序号（按成本排序）', fontsize=11)
ax.set_ylabel('吨氨成本 (元/吨)', fontsize=11)
ax.legend(frameon=True, edgecolor=COLORS['grid'], fontsize=9, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_q2_annual_cost.pdf')
print("OK: fig_q2_annual_cost.pdf")
