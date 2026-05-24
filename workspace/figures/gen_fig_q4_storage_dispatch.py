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
with open('figures/problem_1_results.json', 'r') as f:
    p1_data = json.load(f)

hours = np.arange(24)
# Use W4P1 (max curtailment scenario) wind/PV pattern - scale from typical
# W4 = high wind, P1 = high PV
P_wind_base = np.array(p1_data['power_curves']['P_wind'])
P_pv_base = np.array(p1_data['power_curves']['P_pv'])

# For W4P1 (highest RE scenario), scale up
P_wind = P_wind_base * 1.6  # W4 = high wind
P_pv = P_pv_base * 1.2  # P1 = high PV
P_RE = P_wind + P_pv
P_load = np.array(p1_data['power_curves']['P_load'])

# Storage: 5 MWh capacity, simulate charge/discharge
storage_cap = 5.0  # MWh
soc = np.zeros(25)
soc[0] = storage_cap * 0.5
P_storage = np.zeros(24)  # positive = discharge, negative = charge
P_max_charge = 2.5  # MW
P_max_discharge = 2.5  # MW

# Simple dispatch: charge when surplus, discharge when deficit
alpha_target = data['storage_optimization']['best_M_NH3'] / 72.0
P_h2nh3 = alpha_target * 21.5  # total electrolyzer + ammonia power

for t in range(24):
    surplus = P_RE[t] - P_load[t] - P_h2nh3
    if surplus > 0 and soc[t] < storage_cap:
        charge = min(surplus, P_max_charge, storage_cap - soc[t])
        P_storage[t] = -charge
        soc[t+1] = soc[t] + charge * 0.95
    elif surplus < 0 and soc[t] > 0:
        discharge = min(-surplus, P_max_discharge, soc[t])
        P_storage[t] = discharge
        soc[t+1] = soc[t] - discharge / 0.95
    else:
        soc[t+1] = soc[t]

fig, ax = plt.subplots(figsize=(9, 5.5))

# Area fills for generation
for layer, alpha in enumerate([0.25, 0.12]):
    ax.fill_between(hours, 0, P_wind - layer*0.3, alpha=alpha, color=PALETTE[0], linewidth=0)
ax.plot(hours, P_wind, color=PALETTE[0], linewidth=1.2, label='风电')

for layer, alpha in enumerate([0.25, 0.12]):
    ax.fill_between(hours, P_wind, P_RE - layer*0.3, alpha=alpha, color=PALETTE[1], linewidth=0)
ax.plot(hours, P_RE, color=PALETTE[1], linewidth=1.2, label='风电+光伏')

# Storage charge/discharge
charge_mask = P_storage < 0
discharge_mask = P_storage > 0
ax.bar(hours[charge_mask], P_storage[charge_mask], width=0.5,
       color=_lighten(PALETTE[3], 0.4), edgecolor=PALETTE[3], linewidth=1.0, label='储能充电')
ax.bar(hours[discharge_mask], P_storage[discharge_mask], width=0.5,
       color=_lighten(PALETTE[2], 0.4), edgecolor=PALETTE[2], linewidth=1.0, label='储能放电')

# SOC on secondary axis
ax2 = ax.twinx()
ax2.plot(hours, soc[:24], '--', color=PALETTE[5], linewidth=1.8, label='SOC')
ax2.set_ylabel('储能SOC (MWh)', fontsize=10, color=PALETTE[5])
ax2.set_ylim(0, storage_cap * 1.3)
ax2.tick_params(axis='y', labelcolor=PALETTE[5])

# Combined legend
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, frameon=True, edgecolor=COLORS['grid'],
          fontsize=8, loc='upper left', ncol=2)

ax.set_xlabel('时刻 (h)', fontsize=11)
ax.set_ylabel('功率 (MW)', fontsize=11)
ax.set_xlim(-0.5, 23.5)
ax.set_xticks(range(0, 24, 2))
ax.spines['top'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'figures/fig_q4_storage_dispatch.pdf')
print("OK: fig_q4_storage_dispatch.pdf")
