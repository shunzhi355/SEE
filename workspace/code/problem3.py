"""问题三：基于连续制氨调节的运行优化（线性规划）"""
import numpy as np
from scipy.optimize import linprog
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_loader import (load_load_curve, load_typical_wind_pv, load_wind_scenarios,
                          load_pv_scenarios, load_prices, get_sell_price,
                          PARAMS_EXPANDED, P_WIND_CAP, P_PV_CAP, P_LOAD_PEAK,
                          PRODUCTION_LEVELS)
from utils import calc_green_indicators, check_indicators, calc_cost_ton, validate_constraints

def solve_continuous_lp(P_wind, P_pv, P_load, prices, c_sell, params, M_target):
    """
    LP求解连续调度: x = [alpha(1..24), b(1..24), s(1..24)]
    功率平衡: alpha(t)*P_EHA + P_load(t) + s(t) = P_wind(t) + P_pv(t) + b(t)
    即: b(t) - s(t) = alpha(t)*P_EHA + P_load(t) - P_wind(t) - P_pv(t)
    """
    P_EHA_rated = params["P_ALK"] + params["P_PEM"] + params["P_NH3"]
    c_om_weighted = (params["P_ALK"] * params["c_om_ALK"] +
                     params["P_PEM"] * params["c_om_PEM"] +
                     params["P_NH3"] * params["c_om_NH3"])
    alpha_sum_target = M_target / params["m_NH3"]
    if alpha_sum_target < 2.4 or alpha_sum_target > 24.0:
        return None
    P_net = P_wind + P_pv - P_load  # 风光减去常规负荷

    # 由于谷电价<上网电价存在套利可能，直接用分段计算避免LP无界问题
    # 对每时段：给定alpha(t)，确定性地计算b和s
    # 用直接的决策变量alpha(t)优化，b/s由alpha决定

    # 目标函数只含alpha: 对每个alpha(t)值，成本=f(alpha(t))
    # deficit(t) = alpha(t)*P_EHA - P_net(t)
    # if deficit>0: b(t)=deficit, s(t)=0, cost=deficit*price(t)
    # if deficit<0: b(t)=0, s(t)=-deficit, income=-deficit*c_sell
    # 由于b*s=0自然满足互斥

    # 这变成分段线性问题。用LP处理：
    # 对于每个t，有两种情况的成本系数:
    # 当 alpha(t)*P_EHA >= P_net(t) (购电): 边际成本 = P_EHA*prices(t)*1000
    # 当 alpha(t)*P_EHA < P_net(t) (售电): 边际成本 = -P_EHA*c_sell*1000

    # 由于不知道哪种情况，用标准LP技巧:
    # 约束: b(t) - s(t) = alpha(t)*P_EHA - P_net(t) 改写为
    #        alpha(t)*P_EHA - b(t) + s(t) = P_net(t)
    # 目标中 b的系数=prices(t) (正，购电成本)，s的系数=c_sell (正，但取负号因为是收入)
    # 为防止套利(b,s同时>0)，确保对所有t: prices(t) + c_sell > 0 (天然满足)
    # 但实际问题是当 prices(t) < c_sell 时，增加b和s可套利
    # 解决方案：加上界约束，b和s的物理上界

    # b(t)物理上界: 最多购买P_EHA_rated + P_load_max = 41.5 + 4.2 ≈ 46 MW
    # s(t)物理上界: 最多售出P_wind_max + P_pv_max = 40 + 64 = 104 MW

    c = np.zeros(72)
    for t in range(24):
        c[t] = c_om_weighted * 1000          # alpha运维成本
        c[24 + t] = prices[t] * 1000         # 购电成本(元/MW-h * 1h)
        c[48 + t] = -c_sell * 1000           # 售电收入(负成本)

    A_eq = np.zeros((25, 72))
    b_eq = np.zeros(25)
    A_eq[0, :24] = 1.0
    b_eq[0] = alpha_sum_target
    for t in range(24):
        A_eq[1 + t, t] = P_EHA_rated       # alpha(t)*P_EHA
        A_eq[1 + t, 24 + t] = -1.0         # -b(t)
        A_eq[1 + t, 48 + t] = 1.0          # +s(t)
        b_eq[1 + t] = P_net[t]

    # 变量界 - 关键：给b和s加物理上界防止套利
    P_RE_max = P_wind.max() + P_pv.max()
    b_max = P_EHA_rated + P_LOAD_PEAK  # 最大购电
    s_max = P_RE_max                    # 最大售电
    bounds = []
    for t in range(24):
        bounds.append((0.1, 1.0))       # alpha
    for t in range(24):
        bounds.append((0, b_max))       # b
    for t in range(24):
        bounds.append((0, s_max))       # s

    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not result.success:
        return None

    alpha = result.x[:24]
    P_buy = result.x[24:48]
    P_sell_arr = result.x[48:72]

    # 清理微小的套利残余(b和s同时微正)
    for t in range(24):
        if P_buy[t] > 1e-6 and P_sell_arr[t] > 1e-6:
            net_flow = P_buy[t] - P_sell_arr[t]
            if net_flow > 0:
                P_buy[t] = net_flow
                P_sell_arr[t] = 0
            else:
                P_sell_arr[t] = -net_flow
                P_buy[t] = 0

    P_EHA_actual = alpha * P_EHA_rated
    P_demand = P_EHA_actual + P_load
    E_total = np.sum(P_demand)
    E_RE = np.sum(P_wind + P_pv)
    E_buy = np.sum(P_buy)
    E_sell = np.sum(P_sell_arr)
    R1, R2, R3 = calc_green_indicators(E_total, E_RE, E_buy, E_sell)
    C_RE = np.sum(P_wind * params["c_wind"] + P_pv * params["c_pv"]) * 1000
    C_OM = np.sum(P_EHA_actual * c_om_weighted / P_EHA_rated) * 1000
    C_buy_total = np.sum(P_buy * prices) * 1000
    C_sell_total = np.sum(P_sell_arr * c_sell) * 1000
    C_ton = (C_RE + C_OM + C_buy_total - C_sell_total) / M_target
    return {
        "alpha": alpha.tolist(), "P_buy": P_buy.tolist(), "P_sell": P_sell_arr.tolist(),
        "P_EHA_actual": P_EHA_actual.tolist(), "M_NH3": M_target,
        "E_total": E_total, "E_RE": E_RE, "E_buy": E_buy, "E_sell": E_sell,
        "R1": R1, "R2": R2, "R3": R3, "C_ton": C_ton, "C_RE": C_RE,
    }

def solve_problem3():
    print("=" * 60)
    print("问题三：基于连续制氨调节的运行优化")
    print("=" * 60)
    load_pu = load_load_curve()
    wind_pu_typical, pv_pu_typical = load_typical_wind_pv()
    wind_scenarios = load_wind_scenarios()
    pv_scenarios = load_pv_scenarios()
    prices = load_prices()
    c_sell = get_sell_price()
    params = PARAMS_EXPANDED
    P_load = load_pu * P_LOAD_PEAK

    print("\n--- 24种场景x5产量 LP求解 ---")
    all_results = {}
    for wi in range(6):
        for pj in range(4):
            scenario_name = f"W{wi+1}P{pj+1}"
            P_wind_s = wind_scenarios[:, wi] * P_WIND_CAP
            P_pv_s = pv_scenarios[:, pj] * P_PV_CAP
            scenario_data = {}
            for prod in PRODUCTION_LEVELS:
                res = solve_continuous_lp(P_wind_s, P_pv_s, P_load, prices, c_sell, params, prod)
                if res is not None:
                    scenario_data[prod] = res
                else:
                    scenario_data[prod] = {"C_ton": 99999, "R1": 0, "R2": 0, "R3": 0, "M_NH3": prod}
            all_results[scenario_name] = scenario_data

    print("\n  各产量水平吨氨成本统计:")
    cost_stats = {}
    for prod in PRODUCTION_LEVELS:
        costs = [all_results[s][prod]["C_ton"] for s in all_results if all_results[s][prod]["C_ton"] < 90000]
        if costs:
            cost_stats[prod] = {"mean": np.mean(costs), "min": np.min(costs),
                                "max": np.max(costs), "std": np.std(costs)}
            print(f"  {prod}t/d: mean={np.mean(costs):.0f}, [{np.min(costs):.0f}, {np.max(costs):.0f}]")

    best_prod_per_scenario = {}
    for s in all_results:
        valid = {p: all_results[s][p]["C_ton"] for p in PRODUCTION_LEVELS if all_results[s][p]["C_ton"] < 90000}
        best_prod_per_scenario[s] = min(valid, key=valid.get) if valid else 36

    full_satisfy = partial_satisfy = none_satisfy = 0
    annual_details = []
    for s in sorted(all_results.keys()):
        best_p = best_prod_per_scenario[s]
        res = all_results[s][best_p]
        r1_ok, r2_ok, r3_ok = check_indicators(res["R1"], res["R2"], res["R3"])
        n_ok = sum([r1_ok, r2_ok, r3_ok])
        if n_ok == 3: full_satisfy += 1
        elif n_ok == 0: none_satisfy += 1
        else: partial_satisfy += 1
        annual_details.append({"scenario": s, "best_production": best_p,
            "C_ton": res["C_ton"], "R1": res["R1"], "R2": res["R2"], "R3": res["R3"],
            "R1_ok": bool(r1_ok), "R2_ok": bool(r2_ok), "R3_ok": bool(r3_ok),
            "E_buy": res.get("E_buy", 0), "E_sell": res.get("E_sell", 0)})

    print(f"\n  绿电指标: 全满足={full_satisfy}, 部分={partial_satisfy}, 全不满足={none_satisfy}")
    total_cost_w = sum(d["C_ton"] * d["best_production"] * 15 for d in annual_details)
    total_prod = sum(d["best_production"] * 15 for d in annual_details)
    annual_cost_per_ton = total_cost_w / total_prod
    print(f"  全年加权吨氨成本: {annual_cost_per_ton:.0f} 元/吨")
    annual_cost_curve = sorted([d["C_ton"] for d in annual_details])

    # 典型场景
    P_wind_typical = wind_pu_typical * P_WIND_CAP
    P_pv_typical = pv_pu_typical * P_PV_CAP
    typical_results = {}
    print("\n--- 典型场景连续调度 ---")
    for prod in PRODUCTION_LEVELS:
        res = solve_continuous_lp(P_wind_typical, P_pv_typical, P_load, prices, c_sell, params, prod)
        if res:
            typical_results[prod] = res
            print(f"  {prod}t/d: C_ton={res['C_ton']:.0f}, R1={res['R1']*100:.1f}%, R2={res['R2']*100:.1f}%, R3={res['R3']*100:.1f}%")

    output = {
        "problem": "问题三",
        "typical_scenario": {str(p): {
            "C_ton": round(typical_results[p]["C_ton"], 2),
            "R1": round(typical_results[p]["R1"], 4), "R2": round(typical_results[p]["R2"], 4),
            "R3": round(typical_results[p]["R3"], 4),
            "alpha": typical_results[p]["alpha"],
            "E_buy": round(typical_results[p]["E_buy"], 2),
            "E_sell": round(typical_results[p]["E_sell"], 2),
        } for p in PRODUCTION_LEVELS if p in typical_results},
        "all_scenarios": {s: {str(p): {
            "C_ton": round(all_results[s][p]["C_ton"], 2),
            "R1": round(all_results[s][p]["R1"], 4),
            "R2": round(all_results[s][p]["R2"], 4),
            "R3": round(all_results[s][p]["R3"], 4),
        } for p in PRODUCTION_LEVELS} for s in sorted(all_results.keys())},
        "cost_stats": {str(p): {k: round(v, 2) for k, v in cost_stats[p].items()} for p in cost_stats},
        "annual_analysis": {
            "full_satisfy": full_satisfy, "partial_satisfy": partial_satisfy,
            "none_satisfy": none_satisfy,
            "annual_cost_per_ton": round(annual_cost_per_ton, 2),
            "annual_cost_curve": [round(c, 2) for c in annual_cost_curve],
            "details": annual_details,
        },
        "best_production_per_scenario": best_prod_per_scenario,
    }
    with open("../figures/problem_3_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n✅ 问题三结果已保存")
    return output

if __name__ == "__main__":
    solve_problem3()
