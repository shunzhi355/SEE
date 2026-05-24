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

typical = data['typical_scenario']
productions = [72, 63, 54, 45, 36]

categories = ['自发自用比\n(>60%)', '绿电比例\n(>30%)', '上网比例\n(<20%)', '设备利用率', '成本效益']
N = len(categories)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist() + [0]

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
ax.set_facecolor('white')
ax.set_ylim(0, 1.15)

# Gradient ring background
ring_levels = [0.2, 0.4, 0.6, 0.8, 1.0]
theta_fill = np.linspace(0, 2*np.pi, 100)
for k, r in enumerate(ring_levels):
    r_prev = ring_levels[k-1] if k > 0 else 0
    if k % 2 == 0:
        ax.fill_between(theta_fill, r_prev, r, alpha=0.025, color=PALETTE[0], zorder=0)
    ax.plot(theta_fill, [r]*len(theta_fill), color='#E5E5E5', linewidth=0.5, zorder=1)
ax.set_yticks(ring_levels)
ax.set_yticklabels(['0.2','0.4','0.6','0.8','1.0'], fontsize=7, color='#C0C0C0')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=9.5, color=COLORS['text'])
ax.tick_params(axis='x', pad=18)

# Threshold line for R1>0.6
threshold_r1 = [0.6, 0.3, 0.2, 0.5, 0.5]  # normalized thresholds
threshold_vals = threshold_r1 + [threshold_r1[0]]
ax.plot(angles, threshold_vals, '--', color=COLORS['ref_line'], linewidth=1.5, alpha=0.6, label='指标阈值')

for i, prod in enumerate(productions):
    t = typical[str(prod)]
    R1 = t['R1']  # self-use ratio (>0.6 required)
    R2 = t['R2']  # green ratio (>0.3 required)
    R3 = t['R3']  # grid-sell ratio (<0.2 required, so 1-R3 for radar)
    utilization = t['N_on'] / 24.0
    cost_norm = 1 - (t['C_ton'] - 3000) / 4000  # normalize cost (lower is better)
    cost_norm = max(0, min(1, cost_norm))
    
    vals = [R1, R2, 1-R3, utilization, cost_norm]
    values = vals + [vals[0]]
    
    is_best = (prod == 54)  # 54 is a good balance
    lw = 2.5 if is_best else 1.2
    alpha_line = 1.0 if is_best else 0.5
    alpha_fill = 0.12 if is_best else 0.03
    
    ax.plot(angles, values, color=PALETTE[i], linewidth=lw, label=f'{prod}吨/日', alpha=alpha_line, zorder=3)
    ax.fill(angles, values, color=PALETTE[i], alpha=alpha_fill, zorder=1)

ax.legend(loc='best', bbox_to_anchor=(1.25, 1.05),
          frameon=True, edgecolor=COLORS['grid'], fontsize=9, facecolor='white')
fig.tight_layout()
save_fig(fig, 'figures/fig_q2_indicators.pdf')
print("OK: fig_q2_indicators.pdf")
