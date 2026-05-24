"""灵敏度分析"""
import numpy as np
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_loader import (load_load_curve, load_typical_wind_pv, load_prices,
                          get_sell_price, PARAMS_EXPANDED, P_WIND_CAP, P_PV_CAP,
                          P_LOAD_PEAK)
from problem3 import solve_continuous_lp

def run_sensitivity():
    print("=" * 60)
    print("灵敏度分析")
    print("=" * 60)

    load_pu = load_load_curve()
    wind_pu, pv_pu = load_typical_wind_pv()
    prices_base = load_prices()
    c_sell_base = get_sell_price()
    
    # 注入基准 CCER 参数
    params = PARAMS_EXPANDED.copy()
    params["p_carbon"] = 70.0      # 基准碳价：70元/吨
    params["e_grid"] = 0.5703      # 区域电网边际排放因子 tCO2/MWh
    
    P_load = load_pu * P_LOAD_PEAK
    P_wind_base = wind_pu * P_WIND_CAP
    P_pv_base = pv_pu * P_PV_CAP
    M_target = 45  # 中间产量水平

    # 基准结果
    base_res = solve_continuous_lp(P_wind_base, P_pv_base, P_load, prices_base, c_sell_base, params, M_target)
    base_cost = base_res["C_ton"]
    print(f"基准: M={M_target}t/d, C_ton={base_cost:.0f} 元/吨 (包含基准碳收益)")

    sensitivity_results = {}

    # 1. 风电装机容量 ±20%
    print("\n--- 风电装机容量 ---")
    param_name = "wind_capacity"
    values = []
    objectives = []
    for factor in np.linspace(0.8, 1.2, 9):
        P_wind_s = wind_pu * (P_WIND_CAP * factor)
        res = solve_continuous_lp(P_wind_s, P_pv_base, P_load, prices_base, c_sell_base, params, M_target)
        if res:
            values.append(round(P_WIND_CAP * factor, 1))
            objectives.append(round(res["C_ton"], 2))
    sensitivity_results[param_name] = {"values": values, "objective": objectives,
        "unit": "MW", "base_value": P_WIND_CAP, "description": "风电装机容量"}
    print(f"  范围: {values[0]}~{values[-1]} MW, 成本: {objectives[0]:.0f}~{objectives[-1]:.0f}")

    # 2. 光伏装机容量 ±20%
    print("\n--- 光伏装机容量 ---")
    param_name = "pv_capacity"
    values = []
    objectives = []
    for factor in np.linspace(0.8, 1.2, 9):
        P_pv_s = pv_pu * (P_PV_CAP * factor)
        res = solve_continuous_lp(P_wind_base, P_pv_s, P_load, prices_base, c_sell_base, params, M_target)
        if res:
            values.append(round(P_PV_CAP * factor, 1))
            objectives.append(round(res["C_ton"], 2))
    sensitivity_results[param_name] = {"values": values, "objective": objectives,
        "unit": "MW", "base_value": P_PV_CAP, "description": "光伏装机容量"}
    print(f"  范围: {values[0]}~{values[-1]} MW, 成本: {objectives[0]:.0f}~{objectives[-1]:.0f}")

    # 3. 购电电价 ±30%
    print("\n--- 购电电价 ---")
    param_name = "buy_price"
    values = []
    objectives = []
    for factor in np.linspace(0.7, 1.3, 9):
        prices_s = prices_base * factor
        res = solve_continuous_lp(P_wind_base, P_pv_base, P_load, prices_s, c_sell_base, params, M_target)
        if res:
            values.append(round(factor, 2))
            objectives.append(round(res["C_ton"], 2))
    sensitivity_results[param_name] = {"values": values, "objective": objectives,
        "unit": "倍率", "base_value": 1.0, "description": "购电电价价格"}
    print(f"  倍率: {values[0]}~{values[-1]}, 成本: {objectives[0]:.0f}~{objectives[-1]:.0f}")

    # 4. 上网电价 ±30%
    print("\n--- 上网电价 ---")
    param_name = "sell_price"
    values = []
    objectives = []
    for factor in np.linspace(0.7, 1.3, 9):
        c_sell_s = c_sell_base * factor
        res = solve_continuous_lp(P_wind_base, P_pv_base, P_load, prices_base, c_sell_s, params, M_target)
        if res:
            values.append(round(c_sell_base * factor, 4))
            objectives.append(round(res["C_ton"], 2))
    sensitivity_results[param_name] = {"values": values, "objective": objectives,
        "unit": "元/kWh", "base_value": c_sell_base, "description": "上网电价"}
    print(f"  范围: {values[0]}~{values[-1]} 元/kWh, 成本: {objectives[0]:.0f}~{objectives[-1]:.0f}")

    # 5. 风电度电成本 ±30%
    print("\n--- 风电度电成本 ---")
    param_name = "wind_cost"
    values = []
    objectives = []
    for factor in np.linspace(0.7, 1.3, 9):
        params_s = params.copy()
        params_s["c_wind"] = 0.15 * factor
        res = solve_continuous_lp(P_wind_base, P_pv_base, P_load, prices_base, c_sell_base, params_s, M_target)
        if res:
            values.append(round(0.15 * factor, 4))
            objectives.append(round(res["C_ton"], 2))
    sensitivity_results[param_name] = {"values": values, "objective": objectives,
        "unit": "元/kWh", "base_value": 0.15, "description": "风电度电成本"}
    print(f"  范围: {values[0]}~{values[-1]} 元/kWh, 成本: {objectives[0]:.0f}~{objectives[-1]:.0f}")

    # 6. 光伏度电成本 ±30%
    print("\n--- 光伏度电成本 ---")
    param_name = "pv_cost"
    values = []
    objectives = []
    for factor in np.linspace(0.7, 1.3, 9):
        params_s = params.copy()
        params_s["c_pv"] = 0.12 * factor
        res = solve_continuous_lp(P_wind_base, P_pv_base, P_load, prices_base, c_sell_base, params_s, M_target)
        if res:
            values.append(round(0.12 * factor, 4))
            objectives.append(round(res["C_ton"], 2))
    sensitivity_results[param_name] = {"values": values, "objective": objectives,
        "unit": "元/kWh", "base_value": 0.12, "description": "光伏度电成本"}
    print(f"  范围: {values[0]}~{values[-1]} 元/kWh, 成本: {objectives[0]:.0f}~{objectives[-1]:.0f}")

    # 7. 碳排放交易价格 (0~150元/吨)
    print("\n--- 碳排放交易价格 ---")
    param_name = "carbon_price"
    values = []
    objectives = []
    for p_carb in np.linspace(0, 150, 9):
        params_s = params.copy()
        params_s["p_carbon"] = p_carb
        res = solve_continuous_lp(P_wind_base, P_pv_base, P_load, prices_base, c_sell_base, params_s, M_target)
        if res:
            # 兼容性处理：若底层 problem3.py 尚未支持 p_carbon 目标函数约束
            # 则在此处进行后处理扣除 CCER 收益，以保证数据能够正确跑出
            c_ton = res["C_ton"]
            if "E_buy" in res and "E_total" in res and res.get("_carbon_applied", False) == False:
                # 估算自用绿电：E_RE_used ≈ E_total - E_buy
                e_re_used = res["E_total"] - res["E_buy"]
                r_ccer = e_re_used * params_s["e_grid"] * p_carb / 1000  # 注意单位换算
                c_ton = (res["C_ton"] * M_target - r_ccer) / M_target
                
            values.append(round(p_carb, 1))
            objectives.append(round(c_ton, 2))
            
    sensitivity_results[param_name] = {"values": values, "objective": objectives,
        "unit": "元/吨", "base_value": 70.0, "description": "碳排放交易价格"}
    print(f"  范围: {values[0]}~{values[-1]} 元/吨, 成本: {objectives[0]:.0f}~{objectives[-1]:.0f}")

    output = {
        "base_cost": round(base_cost, 2),
        "M_target": M_target,
        "parameters": sensitivity_results,
    }
    with open("../figures/sensitivity_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n✅ 灵敏度分析结果已保存")
    return output

if __name__ == "__main__":
    run_sensitivity()