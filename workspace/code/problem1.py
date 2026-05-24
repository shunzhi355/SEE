"""问题一：典型风光场景下绿电直连指标分析"""
import numpy as np
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_loader import (load_load_curve, load_typical_wind_pv, load_prices,
                          get_sell_price, PARAMS_BASE, P_WIND_CAP, P_PV_CAP, P_LOAD_PEAK)
from utils import calc_green_indicators, check_indicators, calc_cost_ton, validate_constraints

def solve_problem1():
    print("=" * 60)
    print("问题一：典型风光场景下绿电直连指标分析")
    print("=" * 60)
    
    # 读取数据
    load_pu = load_load_curve()
    wind_pu, pv_pu = load_typical_wind_pv()
    prices = load_prices()
    c_sell = get_sell_price()
    params = PARAMS_BASE
    
    # 计算实际功率 (MW)
    P_load = load_pu * P_LOAD_PEAK
    P_wind = wind_pu * P_WIND_CAP
    P_pv = pv_pu * P_PV_CAP
    
    # 电氢氨装置满负荷功率
    P_EHA_rated = params['P_ALK'] + params['P_PEM'] + params['P_NH3']  # 20.75 MW
    print(f"电氢氨装置额定功率: {P_EHA_rated} MW")
    print(f"常规负荷范围: [{P_load.min():.2f}, {P_load.max():.2f}] MW")
    
    # 总用电功率
    P_demand = P_EHA_rated + P_load  # 24h
    
    # 净功率 = 风光 - 需求
    P_net = P_wind + P_pv - P_demand
    
    # 购售电功率
    P_buy = np.maximum(-P_net, 0)
    P_sell_arr = np.maximum(P_net, 0)
    
    # 电量计算 (MWh, Δt=1h)
    E_total = np.sum(P_demand)
    E_RE = np.sum(P_wind + P_pv)
    E_buy = np.sum(P_buy)
    E_sell = np.sum(P_sell_arr)
    
    print(f"\n--- 电量指标 ---")
    print(f"日总用电量 E_total = {E_total:.2f} MWh")
    print(f"新能源发电量 E_RE = {E_RE:.2f} MWh")
    print(f"网购电量 E_buy = {E_buy:.2f} MWh")
    print(f"上网电量 E_sell = {E_sell:.2f} MWh")
    
    # 绿电直连指标
    R1, R2, R3 = calc_green_indicators(E_total, E_RE, E_buy, E_sell)
    r1_ok, r2_ok, r3_ok = check_indicators(R1, R2, R3)
    
    print(f"\n--- 绿电直连指标 ---")
    print(f"自发自用比 R1 = {R1*100:.2f}% (要求>60%) {'✅' if r1_ok else '❌'}")
    print(f"绿电比例 R2 = {R2*100:.2f}% (要求>30%) {'✅' if r2_ok else '❌'}")
    print(f"上网比例 R3 = {R3*100:.2f}% (要求<20%) {'✅' if r3_ok else '❌'}")
    
    # 吨氨成本
    M_NH3 = 36.0  # 吨/日
    P_EHA_actual = np.full(24, P_EHA_rated)
    C_ton, cost_detail = calc_cost_ton(P_wind, P_pv, P_buy, P_sell_arr, 
                                        P_EHA_actual, params, prices, c_sell, M_NH3)
    
    print(f"\n--- 成本分析 ---")
    print(f"风光度电成本: {cost_detail['C_RE']:.0f} 元")
    print(f"运维成本: {cost_detail['C_OM']:.0f} 元")
    print(f"购电成本: {cost_detail['C_buy']:.0f} 元")
    print(f"售电收入: {cost_detail['C_sell']:.0f} 元")
    print(f"吨氨成本: {C_ton:.2f} 元/吨")
    
    # 验证
    results = {
        'E_total': E_total, 'E_RE': E_RE, 'E_buy': E_buy, 'E_sell': E_sell,
        'R1': R1, 'R2': R2, 'R3': R3, 'C_ton': C_ton,
        'P_buy_arr': P_buy.tolist(), 'P_sell_arr': P_sell_arr.tolist()
    }
    validate_constraints(results, "一")
    
    # 保存结果
    output = {
        'problem': '问题一',
        'power_curves': {
            'hours': list(range(24)),
            'P_load': P_load.tolist(),
            'P_wind': P_wind.tolist(),
            'P_pv': P_pv.tolist(),
            'P_demand': P_demand.tolist(),
            'P_buy': P_buy.tolist(),
            'P_sell': P_sell_arr.tolist(),
            'P_net': P_net.tolist(),
            'P_RE': (P_wind + P_pv).tolist(),
        },
        'energy': {
            'E_total': round(E_total, 2),
            'E_RE': round(E_RE, 2),
            'E_buy': round(E_buy, 2),
            'E_sell': round(E_sell, 2),
            'E_self_use': round(E_total - E_buy, 2),
        },
        'indicators': {
            'R1': round(R1, 4),
            'R2': round(R2, 4),
            'R3': round(R3, 4),
            'R1_satisfied': bool(r1_ok),
            'R2_satisfied': bool(r2_ok),
            'R3_satisfied': bool(r3_ok),
        },
        'cost': {
            'C_ton': round(C_ton, 2),
            'C_RE': round(cost_detail['C_RE'], 2),
            'C_OM': round(cost_detail['C_OM'], 2),
            'C_buy': round(cost_detail['C_buy'], 2),
            'C_sell': round(cost_detail['C_sell'], 2),
            'M_NH3': M_NH3,
        },
        'analysis': {
            'reason_R1_fail': '风光出力集中在白天(光伏10-16时)，夜间风力不足需大量购电，同时存在大量购售电导致自发自用比低',
            'reason_R3_fail': '白天光伏大量余电上网(占总发电量35.9%)，超过20%上限',
        }
    }
    
    os.makedirs('../figures', exist_ok=True)
    with open('../figures/problem_1_results.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 问题一结果已保存到 figures/problem_1_results.json")
    return output

if __name__ == '__main__':
    solve_problem1()
