"""公共工具函数"""
import numpy as np

def calc_green_indicators(E_total, E_RE, E_buy, E_sell):
    """计算绿电直连三项指标"""
    R1 = (E_total - E_sell - E_buy) / E_RE  # 自发自用比 > 60%
    R2 = (E_RE - E_sell) / E_total           # 绿电比例 > 30%
    R3 = E_sell / E_RE                       # 上网比例 < 20%
    return R1, R2, R3

def check_indicators(R1, R2, R3):
    """检查三项指标是否满足要求"""
    r1_ok = R1 > 0.60
    r2_ok = R2 > 0.30
    r3_ok = R3 < 0.20
    return r1_ok, r2_ok, r3_ok

def calc_cost_ton(P_wind, P_pv, P_buy, P_sell, P_EHA_actual, params, prices, c_sell, M_NH3):
    """
    计算吨氨成本（元/吨）
    P_wind, P_pv: 24h风光功率 (MW)
    P_buy, P_sell: 24h购售电功率 (MW)
    P_EHA_actual: 24h电氢氨实际功率 (MW)
    params: 设备参数字典
    prices: 24h分时电价 (元/kWh)
    c_sell: 上网电价 (元/kWh)
    M_NH3: 日产氨量 (吨)
    """
    # 风光度电成本（元）
    C_RE = np.sum(P_wind * params['c_wind'] + P_pv * params['c_pv']) * 1000
    
    # 运维成本（元）- 按实际运行功率计
    c_om_weighted = (params['P_ALK'] * params['c_om_ALK'] + 
                     params['P_PEM'] * params['c_om_PEM'] + 
                     params['P_NH3'] * params['c_om_NH3'])
    P_EHA_rated = params['P_ALK'] + params['P_PEM'] + params['P_NH3']
    c_om_per_mw = c_om_weighted / P_EHA_rated
    C_OM = np.sum(P_EHA_actual * c_om_per_mw) * 1000
    
    # 购电成本（元）
    C_buy = np.sum(P_buy * prices) * 1000
    
    # 售电收入（元）
    C_sell = np.sum(P_sell * c_sell) * 1000
    
    # 吨氨成本
    C_ton = (C_RE + C_OM + C_buy - C_sell) / M_NH3
    
    return C_ton, {'C_RE': C_RE, 'C_OM': C_OM, 'C_buy': C_buy, 'C_sell': C_sell}

def validate_constraints(results, problem_id):
    """验证结果满足所有物理约束"""
    errors = []
    
    # 能量守恒
    E_curtail = results.get('E_curtail', 0)
    balance = results['E_RE'] + results['E_buy'] - results['E_total'] - results['E_sell'] - E_curtail
    if abs(balance) > 0.01:
        errors.append(f"能量守恒违反: 误差={balance:.4f} MWh")
    
    # 功率非负
    if np.any(np.array(results.get('P_buy_arr', [0])) < -1e-6):
        errors.append("P_buy存在负值")
    if np.any(np.array(results.get('P_sell_arr', [0])) < -1e-6):
        errors.append("P_sell存在负值")
    
    # 指标范围
    for name in ['R1', 'R2', 'R3']:
        val = results.get(name, 0)
        if val < -0.01 or val > 1.01:
            errors.append(f"{name}={val:.4f} 超出[0,1]范围")
    
    # 成本合理性
    C_ton = results.get('C_ton', 0)
    if C_ton < 500 or C_ton > 20000:
        errors.append(f"吨氨成本={C_ton:.0f} 超出合理范围[500,20000]")
    
    if errors:
        print(f"⚠️ 问题{problem_id}验证失败:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print(f"✅ 问题{problem_id}所有约束验证通过")
        return True
