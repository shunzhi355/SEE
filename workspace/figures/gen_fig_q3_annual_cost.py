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
    p2_data = json.load(f)
with open('figures/problem_3_results.json', 'r') as f:
    p3_data = json.load(f)

q2_costs = sorted(p2_data['annual_analysis']['annual_cost_curve'])
q3_costs = sorted(p3_data['annual_analysis']['annual_cost_curve'])
x = np.arange(1, 25)

fig, ax = plt.subplots(figsize=(8, 5))

# Q2 line
for layer, alpha in enumerate([0.15, 0.08]):
    ax.fill_between(x, 0, np.array(q2_costs) - layer*50, alpha=alpha, color=PALETTE[4], linewidth=0)
ax.plot(x, q2_costs, 's-', color=PALETTE[4], linewidth=1.8, markersize=5,
        markeredgecolor='white', markeredgewidth=1.0, label='问题二（离散调节）')

# Q3 line
for layer, alpha in enumerate([0.15, 0.08]):
    ax.fill_between(x, 0, np.array(q3_costs) - layer*50, alpha=alpha, color=PALETTE[0], linewidth=0)
ax.plot(x, q3_costs, 'o-', color=PALETTE[0], linewidth=2.2, markersize=5,
        markeredgecolor='white', markeredgewidth=1.0, label='问题三（连续调节）')

# Mean lines
mean_q2 = np.mean(q2_costs)
mean_q3 = np.mean(q3_costs)
ax.axhline(mean_q2, color=PALETTE[4], linestyle=':', linewidth=1.0, alpha=0.5)
ax.axhline(mean_q3, color=PALETTE[0], linestyle=':', linewidth=1.0, alpha=0.5)

# Improvement annotation
improvement = (mean_q2 - mean_q3) / mean_q2 * 100
ax.annotate(f'连续调节降低 {improvement:.1f}%',
            xy=(12, (mean_q2+mean_q3)/2), xytext=(16, mean_q2+500),
            fontsize=9, fontweight='bold', color=PALETTE[0],
            arrowprops=dict(arrowstyle='->', color=PALETTE[0], lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=PALETTE[0], alpha=0.9))

ax.set_xlabel('场景序号（按成本排序）', fontsize=11)
ax.set_ylabel('吨氨成本 (元/吨)', fontsize=11)
ax.legend(frameon=True, edgecolor=COLORS['grid'], fontsize=9, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_q3_annual_cost.pdf')
print("OK: fig_q3_annual_cost.pdf")
