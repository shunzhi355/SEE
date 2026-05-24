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

# Extract typical scenario data - production levels and their on-hours
typical = data['typical_scenario']
productions = [72, 63, 54, 45, 36]
n_on = [typical[str(p)]['N_on'] for p in productions]

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.grid(axis='x', alpha=0.12, linestyle='--', color=COLORS['grid'])
ax.set_axisbelow(True)

y_labels = [f'{p}吨/日' for p in productions]
n = len(productions)

for i in range(n):
    hours_on = n_on[i]
    # Optimal scheduling: center the on-hours around peak RE generation (hours 8-16)
    # For discrete scheduling, start from hour that minimizes cost
    start = max(0, 12 - hours_on // 2)  # center around noon
    if start + hours_on > 24:
        start = 24 - hours_on
    
    c = PALETTE[i % len(PALETTE)]
    # Alternating row background
    if i % 2 == 0:
        ax.axhspan(i - 0.4, i + 0.4, alpha=0.03, color=PALETTE[0], zorder=0)
    
    ax.barh(i, hours_on, left=start, height=0.55,
            color=_lighten(c, 0.3), edgecolor=c, linewidth=1.3, zorder=3)
    ax.text(start + hours_on/2, i, f'{hours_on}h开机',
            ha='center', va='center', fontsize=9, fontweight='bold', color=c)
    
    # Cost annotation at end
    cost = typical[str(productions[i])]['C_ton']
    ax.text(start + hours_on + 0.3, i, f'¥{cost:.0f}/吨',
            ha='left', va='center', fontsize=8, color=COLORS['text'],
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor=COLORS['grid'], alpha=0.8, linewidth=0.5))

# RE peak period marker
ax.axvspan(9, 16, alpha=0.06, color=PALETTE[1], zorder=0)
ax.text(12.5, -0.8, '新能源出力高峰期', ha='center', va='center', fontsize=8,
        color=PALETTE[1], fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                  edgecolor=PALETTE[1], alpha=0.8))

ax.set_yticks(range(n))
ax.set_yticklabels(y_labels, fontsize=10)
ax.set_xlabel('时刻 (h)', fontsize=11)
ax.set_xlim(-0.5, 24.5)
ax.set_xticks(range(0, 25, 2))
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_q2_gantt.pdf')
print("OK: fig_q2_gantt.pdf")
