import json, os, numpy as np

with open('figures/problem_1_results.json') as f:
    p1 = json.load(f)
with open('figures/problem_2_results.json') as f:
    p2 = json.load(f)
with open('figures/problem_3_results.json') as f:
    p3 = json.load(f)
with open('figures/problem_4_results.json') as f:
    p4 = json.load(f)

# TABLE 1: Problem 1 indicators
energy = p1['energy']
indicators = p1['indicators']
table1 = """\\begin{table}[H]
\\centering
\\caption{问题一典型日各项电量指标及绿电指标汇总}
\\begin{tabular}{lcc}
\\toprule
指标 & 数值 & 是否达标 \\\\
\\midrule
"""
table1 += f"总用电量 (MWh) & {energy['E_total']:.2f} & — \\\\\n"
table1 += f"新能源发电量 (MWh) & {energy['E_RE']:.2f} & — \\\\\n"
table1 += f"网购电量 (MWh) & {energy['E_buy']:.2f} & — \\\\\n"
table1 += f"上网电量 (MWh) & {energy['E_sell']:.2f} & — \\\\\n"
table1 += f"自发自用电量 (MWh) & {energy['E_self_use']:.2f} & — \\\\\n"
table1 += "\\midrule\n"
r1_status = '是' if indicators['R1_satisfied'] else '\\textbf{否}'
r2_status = '是' if indicators['R2_satisfied'] else '\\textbf{否}'
r3_status = '是' if indicators['R3_satisfied'] else '\\textbf{否}'
table1 += f"自发自用比 R1 (>60\\%) & {indicators['R1']*100:.2f}\\% & {r1_status} \\\\\n"
table1 += f"绿电比例 R2 (>30\\%) & {indicators['R2']*100:.2f}\\% & {r2_status} \\\\\n"
table1 += f"上网比例 R3 (<20\\%) & {indicators['R3']*100:.2f}\\% & {r3_status} \\\\\n"
table1 += f"吨氨成本 (元/吨) & {p1['cost']['C_ton']:.2f} & — \\\\\n"
table1 += """\\bottomrule
\\end{tabular}
\\end{table}"""
with open('figures/TABLE_q1_indicators.tex', 'w', encoding='utf-8') as f:
    f.write(table1)
print("OK: TABLE_q1_indicators.tex")

# TABLE 2: Problem 2 typical scenario
table2 = """\\begin{table}[H]
\\centering
\\caption{典型场景各产量最优方案对比}
\\resizebox{\\textwidth}{!}{
\\begin{tabular}{ccccccc}
\\toprule
日产量(吨/日) & 开机时段(h) & 吨氨成本(元/吨) & R1(\\%) & R2(\\%) & R3(\\%) & 达标情况 \\\\
\\midrule
"""
for prod in [72, 63, 54, 45, 36]:
    t = p2['typical_scenario'][str(prod)]
    r1_ok = t['R1'] > 0.6
    r3_ok = t['R3'] < 0.2
    status = '全满足' if (r1_ok and r3_ok) else ('部分' if (r1_ok or r3_ok) else '不满足')
    table2 += f"{prod} & {t['N_on']} & {t['C_ton']:.2f} & {t['R1']*100:.2f} & {t['R2']*100:.2f} & {t['R3']*100:.2f} & {status} \\\\\n"
table2 += """\\bottomrule
\\end{tabular}}
\\end{table}"""
with open('figures/TABLE_q2_typical.tex', 'w', encoding='utf-8') as f:
    f.write(table2)
print("OK: TABLE_q2_typical.tex")

# TABLE 3: Problem 2 annual
ann2 = p2['annual_analysis']
total = ann2['full_satisfy'] + ann2['partial_satisfy'] + ann2['none_satisfy']
table3 = """\\begin{table}[H]
\\centering
\\caption{24场景全年绿电指标统计（问题二）}
\\begin{tabular}{lccc}
\\toprule
类别 & 场景数 & 占比 & 说明 \\\\
\\midrule
"""
table3 += f"全满足 & {ann2['full_satisfy']} & {ann2['full_satisfy']/total*100:.1f}\\% & 三项指标均达标 \\\\\n"
table3 += f"部分满足 & {ann2['partial_satisfy']} & {ann2['partial_satisfy']/total*100:.1f}\\% & 部分指标达标 \\\\\n"
table3 += f"全不满足 & {ann2['none_satisfy']} & {ann2['none_satisfy']/total*100:.1f}\\% & 三项指标均不达标 \\\\\n"
table3 += "\\midrule\n"
table3 += f"全年吨氨成本 & \\multicolumn{{3}}{{c}}{{\\textyen {ann2['annual_cost_per_ton']:.2f}/吨}} \\\\\n"
table3 += """\\bottomrule
\\end{tabular}
\\end{table}"""
with open('figures/TABLE_q2_annual.tex', 'w', encoding='utf-8') as f:
    f.write(table3)
print("OK: TABLE_q2_annual.tex")

# TABLE 4: Problem 3 scenarios
ann3 = p3['annual_analysis']
details3 = ann3['details']
table4 = """\\begin{table}[H]
\\centering
\\caption{问题三24场景连续调节最优方案汇总（部分场景）}
\\resizebox{\\textwidth}{!}{
\\begin{tabular}{ccccccc}
\\toprule
场景 & 最优产量(吨/日) & 吨氨成本(元/吨) & R1(\\%) & R2(\\%) & R3(\\%) & 达标情况 \\\\
\\midrule
"""
for d in details3[:10]:
    r1_ok = d['R1'] > 0.6
    r2_ok = d['R2'] > 0.3
    r3_ok = d['R3'] < 0.2
    n_ok = sum([r1_ok, r2_ok, r3_ok])
    status = '全满足' if n_ok == 3 else ('部分' if n_ok > 0 else '不满足')
    table4 += f"{d['scenario']} & {d['best_production']} & {d['C_ton']:.0f} & {d['R1']*100:.1f} & {d['R2']*100:.1f} & {d['R3']*100:.1f} & {status} \\\\\n"
table4 += """\\bottomrule
\\end{tabular}}
\\end{table}"""
with open('figures/TABLE_q3_scenarios.tex', 'w', encoding='utf-8') as f:
    f.write(table4)
print("OK: TABLE_q3_scenarios.tex")

# TABLE 5: Q2 vs Q3 comparison
table5 = """\\begin{table}[H]
\\centering
\\caption{问题二与问题三关键指标对比}
\\begin{tabular}{lccc}
\\toprule
指标 & 问题二（离散） & 问题三（连续） & 变化 \\\\
\\midrule
"""
table5 += f"全年吨氨成本 (元/吨) & {ann2['annual_cost_per_ton']:.2f} & {ann3['annual_cost_per_ton']:.2f} & {(ann3['annual_cost_per_ton']-ann2['annual_cost_per_ton'])/ann2['annual_cost_per_ton']*100:.1f}\\% \\\\\n"
table5 += f"全满足场景数 & {ann2['full_satisfy']} & {ann3['full_satisfy']} & +{ann3['full_satisfy']-ann2['full_satisfy']} \\\\\n"
table5 += f"部分满足场景数 & {ann2['partial_satisfy']} & {ann3['partial_satisfy']} & {ann3['partial_satisfy']-ann2['partial_satisfy']} \\\\\n"
table5 += f"全不满足场景数 & {ann2['none_satisfy']} & {ann3['none_satisfy']} & {ann3['none_satisfy']-ann2['none_satisfy']} \\\\\n"
table5 += """\\bottomrule
\\end{tabular}
\\end{table}"""
with open('figures/TABLE_q3_compare.tex', 'w', encoding='utf-8') as f:
    f.write(table5)
print("OK: TABLE_q3_compare.tex")

# TABLE 6: Problem 4 offgrid
offgrid = p4['offgrid_no_storage']
table6 = """\\begin{table}[H]
\\centering
\\caption{离网各场景产量与成本（部分场景）}
\\resizebox{\\textwidth}{!}{
\\begin{tabular}{cccccc}
\\toprule
场景 & 制氨产量(吨/日) & 吨氨成本(元/吨) & 风光利用率(\\%) & 弃电量(MWh) & 发电量(MWh) \\\\
\\midrule
"""
for sc in list(offgrid.keys())[:10]:
    d = offgrid[sc]
    util = d['E_used'] / d['E_RE'] * 100 if d['E_RE'] > 0 else 0
    table6 += f"{sc} & {d['M_NH3']:.2f} & {d['C_ton']:.0f} & {util:.1f} & {d['E_curtail']:.1f} & {d['E_RE']:.1f} \\\\\n"
table6 += """\\bottomrule
\\end{tabular}}
\\end{table}"""
with open('figures/TABLE_q4_offgrid.tex', 'w', encoding='utf-8') as f:
    f.write(table6)
print("OK: TABLE_q4_offgrid.tex")

# TABLE 7: Storage config
sto = p4['storage_optimization']
sto_stats = p4['storage_stats']
table7 = """\\begin{table}[H]
\\centering
\\caption{储能配置方案及效果}
\\begin{tabular}{lc}
\\toprule
参数 & 数值 \\\\
\\midrule
"""
table7 += f"最优储能容量 (MWh) & {sto['best_C_sto_MWh']} \\\\\n"
table7 += f"目标场景 & {sto['target_scenario']} \\\\\n"
table7 += f"配储后制氨产量 (吨/日) & {sto['best_M_NH3']:.2f} \\\\\n"
table7 += f"配储后吨氨成本 (元/吨) & {sto['best_C_ton']:.2f} \\\\\n"
table7 += f"全年制氨总量 (吨) & {sto_stats['total_annual_production']:.1f} \\\\\n"
table7 += f"平均产能利用率 & {sto_stats['avg_capacity_util']*100:.2f}\\% \\\\\n"
table7 += """\\bottomrule
\\end{tabular}
\\end{table}"""
with open('figures/TABLE_q4_storage.tex', 'w', encoding='utf-8') as f:
    f.write(table7)
print("OK: TABLE_q4_storage.tex")

# TABLE 8: Economics comparison
econ = p4['economics_comparison']
cap_util_grid = econ['grid_connected_annual_prod'] / (72*360) * 100
cap_util_off = econ['offgrid_storage_annual_prod'] / (72*360) * 100
table8 = """\\begin{table}[H]
\\centering
\\caption{离网与联网运行模式全年经济性对比}
\\begin{tabular}{lccc}
\\toprule
指标 & 联网运行 & 离网+储能 & 差异 \\\\
\\midrule
"""
table8 += f"全年吨氨成本 (元/吨) & {econ['grid_connected_annual_cost']:.2f} & {econ['offgrid_storage_annual_cost']:.2f} & {(econ['offgrid_storage_annual_cost']-econ['grid_connected_annual_cost'])/econ['grid_connected_annual_cost']*100:.1f}\\% \\\\\n"
table8 += f"全年制氨总量 (吨) & {econ['grid_connected_annual_prod']} & {econ['offgrid_storage_annual_prod']:.0f} & {(econ['offgrid_storage_annual_prod']-econ['grid_connected_annual_prod'])/econ['grid_connected_annual_prod']*100:.1f}\\% \\\\\n"
table8 += f"产能利用率 (\\%) & {cap_util_grid:.1f} & {cap_util_off:.1f} & {cap_util_off-cap_util_grid:.1f} \\\\\n"
table8 += f"系统支撑成本 (万元) & — & — & {econ['system_support_cost']/10000:.0f} \\\\\n"
table8 += """\\bottomrule
\\end{tabular}
\\end{table}"""
with open('figures/TABLE_q4_economics.tex', 'w', encoding='utf-8') as f:
    f.write(table8)
print("OK: TABLE_q4_economics.tex")

print("\nAll 8 tables generated!")
