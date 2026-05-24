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
    p2 = json.load(f)
with open('figures/problem_3_results.json', 'r') as f:
    p3 = json.load(f)

# Compare Q2 vs Q3 key metrics
metrics = ['全年吨氨成本', '全满足场景数', '部分满足场景数', '不满足场景数', '平均购电量']
q2_vals = [p2['annual_analysis']['annual_cost_per_ton'], 
           p2['annual_analysis']['full_satisfy'],
           p2['annual_analysis']['partial_satisfy'],
           p2['annual_analysis']['none_satisfy'],
           np.mean([d.get('E_buy', 200) for d in p2['annual_analysis']['details']]) if 'details' in p2['annual_analysis'] else 200]
q3_vals = [p3['annual_analysis']['annual_cost_per_ton'],
           p3['annual_analysis']['full_satisfy'],
           p3['annual_analysis']['partial_satisfy'],
           p3['annual_analysis']['none_satisfy'],
           np.mean([d.get('E_buy', 150) for d in p3['annual_analysis']['details']]) if 'details' in p3['annual_analysis'] else 150]

# Calculate relative change (%)
deltas = []
labels = []
for i, (m, v2, v3) in enumerate(zip(metrics, q2_vals, q3_vals)):
    if v2 != 0:
        delta = (v3 - v2) / abs(v2) * 100
    else:
        delta = 100 if v3 > 0 else 0
    deltas.append(delta)
    labels.append(m)

# Sort by absolute delta
sort_idx = np.argsort(np.abs(deltas))[::-1]
deltas = [deltas[i] for i in sort_idx]
labels = [labels[i] for i in sort_idx]

_fig_h = max(4, len(labels) * 0.8 + 1)
fig, ax = plt.subplots(figsize=(8, _fig_h))
y_pos = np.arange(len(labels))

# Direction background
max_abs = max(abs(d) for d in deltas) if deltas else 1
ax.axvspan(0, max_abs*1.3, alpha=0.04, color=COLORS['up'], zorder=0)
ax.axvspan(-max_abs*1.3, 0, alpha=0.04, color=COLORS['down'], zorder=0)

base_colors = [COLORS['up'] if d >= 0 else COLORS['down'] for d in deltas]

# Shadow
ax.barh(y_pos + 0.03, deltas, height=0.5, color='#cccccc', alpha=0.1, zorder=1)
# Main bars
bars = ax.barh(y_pos, deltas, height=0.5,
               color=[_lighten(c, 0.4) for c in base_colors],
               edgecolor=base_colors, linewidth=1.5, zorder=3)

ax.axvline(0, color=COLORS['text'], linewidth=1.2, zorder=2)

# Value labels
for i, (bar, d) in enumerate(zip(bars, deltas)):
    x_pos = d + (max_abs*0.05 if d >= 0 else -max_abs*0.05)
    ha = 'left' if d >= 0 else 'right'
    sign = '+' if d > 0 else ''
    ax.text(x_pos, y_pos[i], f'{sign}{d:.1f}%', va='center', ha=ha,
            fontsize=9, fontweight='bold', color=base_colors[i],
            bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='none', alpha=0.7))

# Direction annotations
ax.text(0.98, 0.02, '改善 →', transform=ax.transAxes, fontsize=8, ha='right',
        color=COLORS['up'], fontweight='bold')
ax.text(0.02, 0.02, '← 恶化', transform=ax.transAxes, fontsize=8, ha='left',
        color=COLORS['down'], fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=10)
ax.set_xlabel('相对变化 (%)', fontsize=11)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.12, linestyle='--', color=COLORS['grid'])
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_q3_compare.pdf')
print("OK: fig_q3_compare.pdf")
