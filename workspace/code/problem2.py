"""问题二：基于离散制氨调节的运行优化"""
import numpy as np
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_loader import (load_load_curve, load_typical_wind_pv, load_wind_scenarios,
                          load_pv_scenarios, load_prices, get_sell_price,
                          PARAMS_EXPANDED, P_WIND_CAP, P_PV_CAP, P_LOAD_PEAK,
                          PRODUCTION_LEVELS)
from utils import calc_green_indicators, check_indicators, calc_cost_ton, validate_constraints

def optimize_discrete_schedule(P_wind, P_pv, P_load, prices, c_sell, params, N_on):
    P_EHA_rated = params["P_ALK"] + params["P_PEM"] + params["P_NH3"]
    marginal_costs = np.zeros(24)
    for t in range(24):
        P_RE_t = P_wind[t] + P_pv[t]
        surplus_off = P_RE_t - P_load[t]
        if surplus_off >= 0:
            cost_off = -surplus_off * c_sell * 1000
        else:
            cost_off = (-surplus_off) * prices[t] * 1000
        surplus_on = P_RE_t - P_load[t] - P_EHA_rated
        if surplus_on >= 0:
            cost_on = -surplus_on * c_sell * 1000
        else:
            cost_on = (-surplus_on) * prices[t] * 1000
        om_cost = (params["P_ALK"] * params["c_om_ALK"] + 
                   params["P_PEM"] * params["c_om_PEM"] + 
                   params["P_NH3"] * params["c_om_NH3"]) * 1000
        marginal_costs[t] = cost_on + om_cost - cost_off
    sorted_idx = np.argsort(marginal_costs)
    u = np.zeros(24)
    u[sorted_idx[:N_on]] = 1
    P_demand = u * P_EHA_rated + P_load
    P_net = P_wind + P_pv - P_demand
    P_buy = np.maximum(-P_net, 0)
    P_sell_arr = np.maximum(P_net, 0)
    E_total = np.sum(P_demand)
    E_RE = np.sum(P_wind + P_pv)
    E_buy = np.sum(P_buy)
    E_sell = np.sum(P_sell_arr)
    R1, R2, R3 = calc_green_indicators(E_total, E_RE, E_buy, E_sell)
    M_NH3 = N_on * params["m_NH3"]
    P_EHA_actual = u * P_EHA_rated
    C_ton, cost_detail = calc_cost_ton(P_wind, P_pv, P_buy, P_sell_arr,
                                        P_EHA_actual, params, prices, c_sell, M_NH3)
    return {
        "u": u.tolist(), "N_on": int(N_on), "M_NH3": M_NH3,
        "E_total": E_total, "E_RE": E_RE, "E_buy": E_buy, "E_sell": E_sell,
        "R1": R1, "R2": R2, "R3": R3, "C_ton": C_ton, "cost_detail": cost_detail,
        "P_buy": P_buy.tolist(), "P_sell": P_sell_arr.tolist(),
    }

def solve_problem2():
    print("=" * 60)
    print("问题二：基于离散制氨调节的运行优化")
    print("=" * 60)
    load_pu = load_load_curve()
    wind_pu_typical, pv_pu_typical = load_typical_wind_pv()
    wind_scenarios = load_wind_scenarios()
    pv_scenarios = load_pv_scenarios()
    prices = load_prices()
    c_sell = get_sell_price()
    params = PARAMS_EXPANDED
    P_load = load_pu * P_LOAD_PEAK
    P_EHA_rated = params["P_ALK"] + params["P_PEM"] + params["P_NH3"]
    print(f"扩容后电氢氨额定功率: {P_EHA_rated} MW")
    hours_needed = {p: int(p / params["m_NH3"]) for p in PRODUCTION_LEVELS}
    print(f"运行时段数: {hours_needed}")
    
    # 问题二(1): 典型场景
    print("\n--- 问题二(1): 典型场景分析 ---")
    P_wind_typical = wind_pu_typical * P_WIND_CAP
    P_pv_typical = pv_pu_typical * P_PV_CAP
    typical_results = {}
    for prod in PRODUCTION_LEVELS:
        N_on = hours_needed[prod]
        res = optimize_discrete_schedule(P_wind_typical, P_pv_typical, P_load, prices, c_sell, params, N_on)
        typical_results[prod] = res
        r1_ok, r2_ok, r3_ok = check_indicators(res["R1"], res["R2"], res["R3"])
        print(f"  产量{prod}t/d: N_on={N_on}h, C_ton={res['C_ton']:.0f}元/吨, "
              f"R1={res['R1']*100:.1f}%, R2={res['R2']*100:.1f}%, R3={res['R3']*100:.1f}%")
    best_prod = min(typical_results, key=lambda p: typical_results[p]["C_ton"])
    print(f"\n  最低吨氨成本产量: {best_prod} t/d, C_ton={typical_results[best_prod]['C_ton']:.0f} 元/吨")
    
    # 问题二(2): 24种场景
    print("\n--- 问题二(2): 24种场景全年分析 ---")
    all_scenario_results = {}
    for wi in range(6):
        for pj in range(4):
            scenario_name = f"W{wi+1}P{pj+1}"
            P_wind_s = wind_scenarios[:, wi] * P_WIND_CAP
            P_pv_s = pv_scenarios[:, pj] * P_PV_CAP
            scenario_data = {}
            for prod in PRODUCTION_LEVELS:
                N_on = hours_needed[prod]
                res = optimize_discrete_schedule(P_wind_s, P_pv_s, P_load, prices, c_sell, params, N_on)
                scenario_data[prod] = res
            all_scenario_results[scenario_name] = scenario_data
    
    # 统计
    cost_stats = {}
    for prod in PRODUCTION_LEVELS:
        costs = [all_scenario_results[s][prod]["C_ton"] for s in all_scenario_results]
        cost_stats[prod] = {"mean": np.mean(costs), "min": np.min(costs), "max": np.max(costs), "std": np.std(costs)}
        print(f"  {prod}t/d: 均值={np.mean(costs):.0f}, 范围=[{np.min(costs):.0f}, {np.max(costs):.0f}]")
    
    best_production_per_scenario = {}
    for s in all_scenario_results:
        best_p = min(PRODUCTION_LEVELS, key=lambda p: all_scenario_results[s][p]["C_ton"])
        best_production_per_scenario[s] = best_p
    
    full_satisfy = partial_satisfy = none_satisfy = 0
    annual_details = []
    for s in sorted(all_scenario_results.keys()):
        best_p = best_production_per_scenario[s]
        res = all_scenario_results[s][best_p]
        r1_ok, r2_ok, r3_ok = check_indicators(res["R1"], res["R2"], res["R3"])
        n_ok = sum([r1_ok, r2_ok, r3_ok])
        if n_ok == 3: full_satisfy += 1
        elif n_ok == 0: none_satisfy += 1
        else: partial_satisfy += 1
        annual_details.append({"scenario": s, "best_production": best_p, "C_ton": res["C_ton"],
            "R1": res["R1"], "R2": res["R2"], "R3": res["R3"],
            "R1_ok": bool(r1_ok), "R2_ok": bool(r2_ok), "R3_ok": bool(r3_ok),
            "E_buy": res["E_buy"], "E_sell": res["E_sell"]})
    
    print(f"\n  绿电指标统计: 全满足={full_satisfy}, 部分满足={partial_satisfy}, 全不满足={none_satisfy}")
    
    total_cost_w = sum(d["C_ton"] * d["best_production"] * 15 for d in annual_details)
    total_prod = sum(d["best_production"] * 15 for d in annual_details)
    annual_cost_per_ton = total_cost_w / total_prod
    print(f"  全年加权吨氨成本: {annual_cost_per_ton:.0f} 元/吨")
    
    annual_cost_curve = sorted([d["C_ton"] for d in annual_details])
    cost_matrix = {}
    for s in sorted(all_scenario_results.keys()):
        cost_matrix[s] = {str(p): round(all_scenario_results[s][p]["C_ton"], 0) for p in PRODUCTION_LEVELS}
    
    output = {
        "problem": "问题二",
        "typical_scenario": {str(p): {
            "N_on": typical_results[p]["N_on"], "M_NH3": typical_results[p]["M_NH3"],
            "C_ton": round(typical_results[p]["C_ton"], 2),
            "R1": round(typical_results[p]["R1"], 4), "R2": round(typical_results[p]["R2"], 4),
            "R3": round(typical_results[p]["R3"], 4),
            "schedule": typical_results[p]["u"],
            "E_buy": round(typical_results[p]["E_buy"], 2), "E_sell": round(typical_results[p]["E_sell"], 2),
            "utilization": round(typical_results[p]["N_on"] / 24, 4),
        } for p in PRODUCTION_LEVELS},
        "best_typical_production": best_prod,
        "best_typical_cost": round(typical_results[best_prod]["C_ton"], 2),
        "cost_matrix": cost_matrix,
        "cost_stats": {str(p): {k: round(v, 2) for k, v in cost_stats[p].items()} for p in PRODUCTION_LEVELS},
        "annual_analysis": {
            "full_satisfy": full_satisfy, "partial_satisfy": partial_satisfy, "none_satisfy": none_satisfy,
            "annual_cost_per_ton": round(annual_cost_per_ton, 2),
            "annual_cost_curve": [round(c, 2) for c in annual_cost_curve],
            "details": annual_details,
        },
        "best_production_per_scenario": best_production_per_scenario,
    }
    
    with open("../figures/problem_2_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 问题二结果已保存")
    return output

if __name__ == "__main__":
    solve_problem2()
