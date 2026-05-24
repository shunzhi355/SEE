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

with open('figures/problem_4_results.json', 'r') as f:
    data = json.load(f)

econ = data['economics_comparison']

categories = ['吨氨成本\n(元/吨)', '年产量\n(吨)', '产能利用率\n(%)']
grid_vals = [econ['grid_connected_annual_cost'], econ['grid_connected_annual_prod'], 
             econ['grid_connected_annual_prod'] / (72*360) * 100]
offgrid_vals = [econ['offgrid_storage_annual_cost'], econ['offgrid_storage_annual_prod'],
                econ['offgrid_storage_annual_prod'] / (72*360) * 100]

fig, axes = plt.subplots(1, 3, figsize=(10, 4.5))

for idx, (cat, gv, ov) in enumerate(zip(categories, grid_vals, offgrid_vals)):
    ax = axes[idx]
    ax.grid(axis='y', alpha=0.12, linestyle='--', color=COLORS['grid'])
    ax.set_axisbelow(True)
    
    x = np.array([0, 1])
    vals = [gv, ov]
    colors = [PALETTE[0], PALETTE[2]]
    labels = ['联网', '离网+储能']
    
    for i in range(2):
        ax.bar(x[i], vals[i], width=0.5, color=_lighten(colors[i], 0.35),
               edgecolor=colors[i], linewidth=1.5)
        ax.text(x[i], vals[i] + max(vals)*0.03, f'{vals[i]:.0f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color=colors[i])
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel(cat.replace('\n', ' '), fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

fig.tight_layout()
save_fig(fig, 'figures/fig_q4_economics.pdf')
print("OK: fig_q4_economics.pdf")
