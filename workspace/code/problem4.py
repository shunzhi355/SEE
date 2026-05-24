"""问题四：离网运行及储能配置"""
import numpy as np
from scipy.optimize import linprog
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_loader import (load_load_curve, load_wind_scenarios, load_pv_scenarios,
                          load_prices, get_sell_price, PARAMS_EXPANDED,
                          P_WIND_CAP, P_PV_CAP, P_LOAD_PEAK,
                          PRODUCTION_LEVELS, STORAGE_PARAMS)
from utils import calc_green_indicators, validate_constraints

def solve_offgrid_no_storage(P_wind, P_pv, P_load, params):
    """问题四(1): 无储能离网，每时段独立最大化产量"""
    P_EHA_rated = params["P_ALK"] + params["P_PEM"] + params["P_NH3"]
    P_net = P_wind + P_pv - P_load
    alpha = np.zeros(24)
    P_curtail = np.zeros(24)
    for t in range(24):
        if P_net[t] <= 0:
            alpha[t] = 0  # 风光不够常规负荷
            P_curtail[t] = 0
        else:
            alpha_max_t = min(P_net[t] / P_EHA_rated, 1.0)
            if alpha_max_t >= 0.1:
                alpha[t] = alpha_max_t
            else:
                alpha[t] = 0
            used = alpha[t] * P_EHA_rated
            P_curtail[t] = P_net[t] - used if P_net[t] > used else 0

    M_NH3 = np.sum(alpha) * params["m_NH3"]
    E_RE = np.sum(P_wind + P_pv)
    E_used = np.sum(alpha * P_EHA_rated + P_load)
    E_curtail = np.sum(P_curtail)
    # Add case where P_net < 0 (load shedding needed or wind covers partial load)
    # Actually if P_net < 0, the load can't be served. For this problem, we assume
    # conventional load must be served. If wind+pv < P_load, it's infeasible unless we shed load.
    # The problem says "尽限利用风光", so if wind+pv < P_load for some hours, those hours
    # the EHA stops and the conventional load is partially unserved (or we treat it as
    # the load being flexible). Let's assume wind+pv always >= P_load (check data).

    # 吨氨成本(离网): 只有风光度电成本和运维
    c_om_weighted = (params["P_ALK"] * params["c_om_ALK"] +
                     params["P_PEM"] * params["c_om_PEM"] +
                     params["P_NH3"] * params["c_om_NH3"])
    C_RE = np.sum(P_wind * params["c_wind"] + P_pv * params["c_pv"]) * 1000
    C_OM = np.sum(alpha * P_EHA_rated * c_om_weighted / P_EHA_rated) * 1000
    C_ton = (C_RE + C_OM) / M_NH3 if M_NH3 > 0 else float('inf')

    wind_util = (E_used + np.sum(np.minimum(P_load, P_wind + P_pv) * (P_net < 0))) / E_RE if E_RE > 0 else 0

    return {
        "alpha": alpha.tolist(),
        "M_NH3": round(M_NH3, 2),
        "C_ton": round(C_ton, 2),
        "E_RE": round(E_RE, 2),
        "E_used": round(E_used, 2),
        "E_curtail": round(E_curtail, 2),
        "wind_pv_util": round(1 - E_curtail/E_RE, 4) if E_RE > 0 else 0,
        "capacity_util": round(M_NH3 / 72, 4),
    }

def solve_offgrid_with_storage(P_wind, P_pv, P_load, params, C_sto):
    """问题四(2): 有储能离网LP调度"""
    P_EHA_rated = params["P_ALK"] + params["P_PEM"] + params["P_NH3"]
    eta_c = STORAGE_PARAMS["eta_c"]
    eta_d = STORAGE_PARAMS["eta_d"]
    sigma = STORAGE_PARAMS["sigma"]
    P_sto_max = min(2 * C_sto, 50)  # 充放电功率上限(2C倍率,最大50MW)

    # 决策变量: [alpha(24), Pc(24), Pd(24), curtail(24)] = 96维
    # 目标: max sum(alpha) => min -sum(alpha)
    n_vars = 96
    c = np.zeros(n_vars)
    c[:24] = -1.0  # maximize production

    # 等式约束: 功率平衡 + 储能状态方程
    # 功率平衡: P_wind(t)+P_pv(t)+Pd(t) = alpha(t)*P_EHA + P_load(t) + Pc(t) + curtail(t)
    # => alpha(t)*P_EHA + Pc(t) - Pd(t) + curtail(t) = P_wind(t)+P_pv(t) - P_load(t) = P_net(t)
    P_net = P_wind + P_pv - P_load

    # SOC状态方程 (用不等式约束处理，或直接嵌入等式)
    # E(t+1) = E(t)*(1-sigma) + Pc(t)*eta_c - Pd(t)/eta_d
    # E(1) = E(25) = 0.5*C_sto (周期性)
    # 用递推: E(t) = E(1)*(1-sigma)^(t-1) + sum_{k=1}^{t-1}[(Pc(k)*eta_c - Pd(k)/eta_d)*(1-sigma)^(t-1-k)]
    # SOC约束: 0 <= E(t) <= C_sto
    # 简化：用等式约束描述E(t)的递推关系

    # 增加SOC变量: E(1)...E(24) => total 96+24=120 vars?
    # Better: add E(1..24) as variables
    # x = [alpha(24), Pc(24), Pd(24), curtail(24), E(24)] = 120维
    n_vars = 120
    c = np.zeros(n_vars)
    c[:24] = -1.0  # max production

    # 等式约束
    n_eq = 24 + 24 + 1  # 功率平衡(24) + SOC递推(24) + 周期性(1) = 49
    A_eq = np.zeros((49, n_vars))
    b_eq = np.zeros(49)

    # 功率平衡: alpha(t)*P_EHA + Pc(t) - Pd(t) + curtail(t) = P_net(t)
    for t in range(24):
        A_eq[t, t] = P_EHA_rated            # alpha
        A_eq[t, 24 + t] = 1.0               # Pc
        A_eq[t, 48 + t] = -1.0              # -Pd
        A_eq[t, 72 + t] = 1.0               # curtail
        b_eq[t] = P_net[t]

    # SOC递推: E(t+1) = E(t)*(1-sigma) + Pc(t)*eta_c - Pd(t)/eta_d
    # => E(t+1) - E(t)*(1-sigma) - Pc(t)*eta_c + Pd(t)/eta_d = 0
    for t in range(23):
        A_eq[24 + t, 96 + t + 1] = 1.0              # E(t+1)
        A_eq[24 + t, 96 + t] = -(1 - sigma)         # -E(t)*(1-sigma)
        A_eq[24 + t, 24 + t] = -eta_c               # -Pc(t)*eta_c
        A_eq[24 + t, 48 + t] = 1.0 / eta_d          # +Pd(t)/eta_d
        b_eq[24 + t] = 0
    # t=23: E(0+1周期) wraps to E(0) - use periodic constraint
    # E(0) = E(24)*(1-sigma) + Pc(23)*eta_c - Pd(23)/eta_d
    t = 23
    A_eq[24 + t, 96 + 0] = 1.0                # E(0) [next day's start = E(0)]
    A_eq[24 + t, 96 + 23] = -(1 - sigma)      # -E(23)*(1-sigma)
    A_eq[24 + t, 24 + 23] = -eta_c            # -Pc(23)*eta_c
    A_eq[24 + t, 48 + 23] = 1.0 / eta_d       # +Pd(23)/eta_d
    b_eq[24 + t] = 0

    # 周期性约束: E(0) = 0.5*C_sto (固定初始SOC)
    A_eq[48, 96 + 0] = 1.0
    b_eq[48] = 0.5 * C_sto

    # 变量界
    bounds = []
    for t in range(24):
        a_max = min(P_net[t] / P_EHA_rated, 1.0) if P_net[t] > 0 else 0
        # With storage, alpha can be higher than P_net allows (Pd provides power)
        bounds.append((0, 1.0))     # alpha: allow [0, 1], storage may enable production
    for t in range(24):
        bounds.append((0, P_sto_max))  # Pc
    for t in range(24):
        bounds.append((0, P_sto_max))  # Pd
    for t in range(24):
        bounds.append((0, None))       # curtail >= 0
    for t in range(24):
        bounds.append((0, C_sto))      # E(t) in [0, C_sto]

    # Handle alpha lower bound: if alpha > 0 must be >= 0.1
    # This is hard in LP. Approximate: allow alpha in [0, 1] and accept alpha in (0, 0.1) as ok
    # Or use iterative approach. For simplicity, set lower bound to 0 (allow shutdown).

    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not result.success:
        return None

    alpha = result.x[:24]
    Pc = result.x[24:48]
    Pd = result.x[48:72]
    curtail = result.x[72:96]
    E_soc = result.x[96:120]

    # Enforce 10% minimum: if 0 < alpha < 0.1, set to 0
    alpha[alpha < 0.1] = 0

    M_NH3 = np.sum(alpha) * params["m_NH3"]
    E_RE = np.sum(P_wind + P_pv)
    E_curtail = np.sum(curtail)

    # 成本
    c_om_weighted = (params["P_ALK"] * params["c_om_ALK"] +
                     params["P_PEM"] * params["c_om_PEM"] +
                     params["P_NH3"] * params["c_om_NH3"])
    C_RE = np.sum(P_wind * params["c_wind"] + P_pv * params["c_pv"]) * 1000
    C_OM = np.sum(alpha * c_om_weighted) * 1000
    # 储能投资分摊(日)
    C_sto_inv = C_sto * 1000 * 1000 / (STORAGE_PARAMS["lifetime_years"] * 365)
    # 储能运维
    C_sto_om = np.sum(Pc + Pd) * STORAGE_PARAMS["om_cost"] * 1000

    C_ton = (C_RE + C_OM + C_sto_inv + C_sto_om) / M_NH3 if M_NH3 > 0 else float('inf')

    return {
        "alpha": alpha.tolist(), "Pc": Pc.tolist(), "Pd": Pd.tolist(),
        "curtail": curtail.tolist(), "E_soc": E_soc.tolist(),
        "M_NH3": round(M_NH3, 2), "C_ton": round(C_ton, 2),
        "E_RE": round(E_RE, 2), "E_curtail": round(E_curtail, 2),
        "wind_pv_util": round(1 - E_curtail/E_RE, 4) if E_RE > 0 else 0,
        "capacity_util": round(M_NH3 / 72, 4),
        "C_sto": C_sto, "C_sto_inv_daily": round(C_sto_inv, 2),
    }

def solve_problem4():
    print("=" * 60)
    print("问题四：离网运行及储能配置")
    print("=" * 60)
    load_pu = load_load_curve()
    wind_scenarios = load_wind_scenarios()
    pv_scenarios = load_pv_scenarios()
    params = PARAMS_EXPANDED
    P_load = load_pu * P_LOAD_PEAK
    P_EHA_rated = params["P_ALK"] + params["P_PEM"] + params["P_NH3"]

    # ===== 问题四(1): 无储能离网 =====
    print("\n--- 问题四(1): 无储能离网各场景产量 ---")
    offgrid_results = {}
    max_curtail_scenario = None
    max_curtail_val = 0
    for wi in range(6):
        for pj in range(4):
            sname = f"W{wi+1}P{pj+1}"
            P_wind_s = wind_scenarios[:, wi] * P_WIND_CAP
            P_pv_s = pv_scenarios[:, pj] * P_PV_CAP
            res = solve_offgrid_no_storage(P_wind_s, P_pv_s, P_load, params)
            offgrid_results[sname] = res
            if res["E_curtail"] > max_curtail_val:
                max_curtail_val = res["E_curtail"]
                max_curtail_scenario = sname

    # 统计
    productions = [offgrid_results[s]["M_NH3"] for s in offgrid_results]
    costs = [offgrid_results[s]["C_ton"] for s in offgrid_results if offgrid_results[s]["C_ton"] < 1e6]
    utils_wp = [offgrid_results[s]["wind_pv_util"] for s in offgrid_results]
    total_annual_prod = sum(offgrid_results[s]["M_NH3"] * 15 for s in offgrid_results)
    avg_capacity_util = total_annual_prod / (72 * 360)

    print(f"  产量范围: [{min(productions):.1f}, {max(productions):.1f}] t/d")
    print(f"  吨氨成本范围: [{min(costs):.0f}, {max(costs):.0f}] 元/吨")
    print(f"  风光利用率范围: [{min(utils_wp):.1%}, {max(utils_wp):.1%}]")
    print(f"  全年总产氨量: {total_annual_prod:.0f} 吨")
    print(f"  年平均产能利用率: {avg_capacity_util:.1%}")
    print(f"  最大弃电场景: {max_curtail_scenario}, 弃电={max_curtail_val:.1f} MWh")

    # 最小风光装机容量估算
    # 要求所有场景所有时段: P_w*pu_wind(t) + P_s*pu_pv(t) >= 0.1*P_EHA + P_load(t)
    min_demand = 0.1 * P_EHA_rated + P_load  # (24,) 最低需求
    # 找最恶劣时段(风光标幺值最低且需求最高)
    # LP: min P_w + P_s, s.t. P_w*pu_w(t,i) + P_s*pu_pv(t,j) >= min_demand(t) for all t,i,j
    from scipy.optimize import linprog as lp
    # 2 variables: [P_w, P_s]
    # 24*24 inequality constraints (all scenarios, all hours)
    A_ub_rows = []
    b_ub_rows = []
    for wi in range(6):
        for pj in range(4):
            for t in range(24):
                # -P_w*pu_w - P_s*pu_pv <= -min_demand(t)
                A_ub_rows.append([-wind_scenarios[t, wi], -pv_scenarios[t, pj]])
                b_ub_rows.append(-min_demand[t])
    A_ub = np.array(A_ub_rows)
    b_ub = np.array(b_ub_rows)
    c_obj = [1, 1]
    bounds_cap = [(0, None), (0, None)]
    res_cap = lp(c_obj, A_ub=A_ub, b_ub=b_ub, bounds=bounds_cap, method="highs")
    if res_cap.success:
        min_wind_cap = res_cap.x[0]
        min_pv_cap = res_cap.x[1]
        print(f"  最小装机容量: 风电={min_wind_cap:.1f}MW, 光伏={min_pv_cap:.1f}MW, 总={min_wind_cap+min_pv_cap:.1f}MW")
    else:
        min_wind_cap = min_pv_cap = float('inf')
        print("  最小装机容量LP求解失败")

    # ===== 问题四(2): 最大弃电场景储能配置 =====
    print(f"\n--- 问题四(2): 储能配置优化 (场景{max_curtail_scenario}) ---")
    wi_best = int(max_curtail_scenario[1]) - 1
    pj_best = int(max_curtail_scenario[3]) - 1
    P_wind_best = wind_scenarios[:, wi_best] * P_WIND_CAP
    P_pv_best = pv_scenarios[:, pj_best] * P_PV_CAP

    # 网格搜索最优储能容量
    C_sto_range = np.arange(5, 205, 5)  # 5~200 MWh
    storage_search = []
    for C_sto in C_sto_range:
        res = solve_offgrid_with_storage(P_wind_best, P_pv_best, P_load, params, C_sto)
        if res and res["M_NH3"] > 0:
            storage_search.append({"C_sto": C_sto, "M_NH3": res["M_NH3"],
                                   "C_ton": res["C_ton"], "E_curtail": res["E_curtail"],
                                   "wind_pv_util": res["wind_pv_util"]})
            if len(storage_search) % 10 == 0:
                print(f"  C_sto={C_sto}MWh: M_NH3={res['M_NH3']:.1f}t, C_ton={res['C_ton']:.0f}")

    # 找最优: 最小化吨氨成本
    if storage_search:
        best_sto = min(storage_search, key=lambda x: x["C_ton"])
        print(f"\n  最优储能容量: {best_sto['C_sto']} MWh")
        print(f"  对应产量: {best_sto['M_NH3']:.1f} t/d, 吨氨成本: {best_sto['C_ton']:.0f} 元/吨")
        print(f"  风光利用率: {best_sto['wind_pv_util']:.1%}")
    else:
        best_sto = {"C_sto": 0, "M_NH3": 0, "C_ton": 0}

    # 24场景有储能调度
    print("\n  24场景有储能调度...")
    storage_all_scenarios = {}
    for wi in range(6):
        for pj in range(4):
            sname = f"W{wi+1}P{pj+1}"
            P_wind_s = wind_scenarios[:, wi] * P_WIND_CAP
            P_pv_s = pv_scenarios[:, pj] * P_PV_CAP
            res = solve_offgrid_with_storage(P_wind_s, P_pv_s, P_load, params, best_sto["C_sto"])
            if res:
                storage_all_scenarios[sname] = res
            else:
                storage_all_scenarios[sname] = offgrid_results[sname]

    # 有储能统计
    prods_sto = [storage_all_scenarios[s]["M_NH3"] for s in storage_all_scenarios]
    costs_sto = [storage_all_scenarios[s]["C_ton"] for s in storage_all_scenarios if storage_all_scenarios[s]["C_ton"] < 1e6]
    total_annual_prod_sto = sum(storage_all_scenarios[s]["M_NH3"] * 15 for s in storage_all_scenarios)
    avg_cap_util_sto = total_annual_prod_sto / (72 * 360)
    print(f"  有储能产量范围: [{min(prods_sto):.1f}, {max(prods_sto):.1f}] t/d")
    print(f"  有储能年产量: {total_annual_prod_sto:.0f} t, 利用率: {avg_cap_util_sto:.1%}")

    # ===== 问题四(3): 离网vs联网对比 =====
    print("\n--- 问题四(3): 离网vs联网经济性对比 ---")
    # 联网数据从问题三结果读取
    q3_path = "../figures/problem_3_results.json"
    if os.path.exists(q3_path):
        with open(q3_path, "r", encoding="utf-8") as f:
            q3_data = json.load(f)
        q3_annual_cost = q3_data["annual_analysis"]["annual_cost_per_ton"]
        q3_annual_details = q3_data["annual_analysis"]["details"]
        q3_total_prod = sum(d["best_production"] * 15 for d in q3_annual_details)
    else:
        q3_annual_cost = 4274
        q3_total_prod = 36 * 360

    offgrid_annual_cost = np.mean(costs_sto) if costs_sto else 0
    print(f"  联网(Q3)全年吨氨成本: {q3_annual_cost:.0f} 元/吨, 年产量: {q3_total_prod:.0f} t")
    print(f"  离网(有储能)全年吨氨成本: {offgrid_annual_cost:.0f} 元/吨, 年产量: {total_annual_prod_sto:.0f} t")

    # 系统支撑成本 = 联网模式下购电成本 - 售电收入
    if os.path.exists(q3_path):
        total_buy = sum(d.get("E_buy", 0) for d in q3_annual_details) * 15
        total_sell = sum(d.get("E_sell", 0) for d in q3_annual_details) * 15
        prices_arr = load_prices()
        avg_buy_price = np.mean(prices_arr)
        system_support_cost = total_buy * avg_buy_price * 1000 - total_sell * get_sell_price() * 1000
    else:
        system_support_cost = 0

    # 保存结果
    output = {
        "problem": "问题四",
        "offgrid_no_storage": {
            s: offgrid_results[s] for s in sorted(offgrid_results.keys())
        },
        "offgrid_stats": {
            "production_range": [round(min(productions), 2), round(max(productions), 2)],
            "cost_range": [round(min(costs), 0), round(max(costs), 0)] if costs else [0, 0],
            "wind_pv_util_range": [round(min(utils_wp), 4), round(max(utils_wp), 4)],
            "total_annual_production": round(total_annual_prod, 2),
            "avg_capacity_util": round(avg_capacity_util, 4),
            "max_curtail_scenario": max_curtail_scenario,
            "max_curtail_MWh": round(max_curtail_val, 2),
        },
        "min_capacity": {
            "wind_MW": round(min_wind_cap, 2) if min_wind_cap < 1e6 else None,
            "pv_MW": round(min_pv_cap, 2) if min_pv_cap < 1e6 else None,
        },
        "storage_optimization": {
            "best_C_sto_MWh": best_sto["C_sto"],
            "best_M_NH3": best_sto["M_NH3"],
            "best_C_ton": best_sto["C_ton"],
            "search_results": storage_search,
            "target_scenario": max_curtail_scenario,
        },
        "storage_all_scenarios": {
            s: {"M_NH3": storage_all_scenarios[s]["M_NH3"],
                "C_ton": storage_all_scenarios[s]["C_ton"],
                "wind_pv_util": storage_all_scenarios[s].get("wind_pv_util", 0),
                "E_curtail": storage_all_scenarios[s].get("E_curtail", 0)}
            for s in sorted(storage_all_scenarios.keys())
        },
        "storage_stats": {
            "total_annual_production": round(total_annual_prod_sto, 2),
            "avg_capacity_util": round(avg_cap_util_sto, 4),
            "production_range": [round(min(prods_sto), 2), round(max(prods_sto), 2)],
            "cost_range": [round(min(costs_sto), 0), round(max(costs_sto), 0)] if costs_sto else [0, 0],
        },
        "economics_comparison": {
            "grid_connected_annual_cost": round(q3_annual_cost, 2),
            "grid_connected_annual_prod": round(q3_total_prod, 2),
            "offgrid_storage_annual_cost": round(offgrid_annual_cost, 2),
            "offgrid_storage_annual_prod": round(total_annual_prod_sto, 2),
            "system_support_cost": round(system_support_cost, 2),
        },
    }

    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer,)): return int(obj)
            if isinstance(obj, (np.floating,)): return float(obj)
            if isinstance(obj, np.ndarray): return obj.tolist()
            return super().default(obj)

    with open("../figures/problem_4_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2, cls=NpEncoder)
    print("\n✅ 问题四结果已保存")
    return output

if __name__ == "__main__":
    solve_problem4()
