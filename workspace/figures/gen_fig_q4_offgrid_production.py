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

offgrid = data['offgrid_no_storage']
scenarios = list(offgrid.keys())
productions = [offgrid[s]['M_NH3'] for s in scenarios]
curtailments = [offgrid[s]['E_curtail'] for s in scenarios]
e_used = [offgrid[s]['E_used'] for s in scenarios]

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.grid(axis='y', alpha=0.12, linestyle='--', color=COLORS['grid'])
ax.set_axisbelow(True)

x = np.arange(len(scenarios))
width = 0.55

# Stacked bar: used energy + curtailed energy
bars1 = ax.bar(x, e_used, width=width, color=_lighten(PALETTE[0], 0.35),
               edgecolor=PALETTE[0], linewidth=1.2, label='有效利用电量 (MWh)')
bars2 = ax.bar(x, curtailments, width=width, bottom=e_used,
               color=_lighten(PALETTE[4], 0.35), edgecolor=PALETTE[4], linewidth=1.2, label='弃电量 (MWh)')

# Production line on secondary axis
ax2 = ax.twinx()
ax2.plot(x, productions, 'D-', color=PALETTE[2], linewidth=2.0, markersize=7,
         markeredgecolor='white', markeredgewidth=1.2, label='制氨产量 (吨/日)', zorder=5)
ax2.set_ylabel('制氨产量 (吨/日)', fontsize=10, color=PALETTE[2])
ax2.tick_params(axis='y', labelcolor=PALETTE[2])

# Capacity line
ax2.axhline(72, color=COLORS['ref_line'], linestyle=':', linewidth=1.0, alpha=0.5)
ax2.text(len(scenarios)-1, 72+1, '额定产能72吨/日', fontsize=8, color=COLORS['ref_line'], ha='right')

# Combined legend
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, frameon=True, edgecolor=COLORS['grid'],
          fontsize=9, loc='upper right')

ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=8, rotation=45, ha='right')
ax.set_xlabel('风光场景', fontsize=11)
ax.set_ylabel('电量 (MWh)', fontsize=11)
ax.spines['top'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_q4_offgrid_production.pdf')
print("OK: fig_q4_offgrid_production.pdf")
