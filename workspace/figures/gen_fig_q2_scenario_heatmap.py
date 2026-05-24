import os, sys, shutil, json
os.makedirs('_utils', exist_ok=True)
for src in ['plot_utils.py']:
    for search in ['skills/shared-scripts', '../skills/shared-scripts']:
        p = os.path.join(search, src)
        if os.path.isfile(p):
            shutil.copy2(p, f'_utils/{src}')
            break
sys.path.insert(0, '.')
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS
setup_style()
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

with open('figures/problem_2_results.json', 'r') as f:
    data = json.load(f)

cost_matrix = data['cost_matrix']
productions = [72, 63, 54, 45, 36]
scenarios = list(cost_matrix.keys())

# Build matrix
matrix = np.zeros((len(scenarios), len(productions)))
for i, sc in enumerate(scenarios):
    for j, prod in enumerate(productions):
        matrix[i, j] = cost_matrix[sc][str(prod)]

fig, ax = plt.subplots(figsize=(8, 7))

# Use YlOrRd colormap (not RdYlGn!)
im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto', interpolation='nearest')

# Add text annotations with auto-contrast
norm_matrix = (matrix - matrix.min()) / (matrix.max() - matrix.min())
for i in range(len(scenarios)):
    for j in range(len(productions)):
        val = matrix[i, j]
        norm_val = norm_matrix[i, j]
        color = 'white' if norm_val > 0.6 else COLORS['text']
        ax.text(j, i, f'{val:.0f}', ha='center', va='center', fontsize=7.5,
                fontweight='bold' if val == matrix[i].min() else 'normal', color=color)

# Highlight minimum per row
for i in range(len(scenarios)):
    min_j = np.argmin(matrix[i])
    ax.add_patch(plt.Rectangle((min_j-0.45, i-0.45), 0.9, 0.9,
                                fill=False, edgecolor='white', linewidth=2.0))

ax.set_xticks(range(len(productions)))
ax.set_xticklabels([f'{p}吨/日' for p in productions], fontsize=9)
ax.set_yticks(range(len(scenarios)))
ax.set_yticklabels(scenarios, fontsize=8)
ax.set_xlabel('日产量', fontsize=11)
ax.set_ylabel('风光场景', fontsize=11)

cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label('吨氨成本 (元/吨)', fontsize=10)

fig.tight_layout()
save_fig(fig, 'figures/fig_q2_scenario_heatmap.pdf')
print("OK: fig_q2_scenario_heatmap.pdf")
