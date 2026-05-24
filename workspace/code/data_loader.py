"""数据读取与预处理模块"""
import numpy as np
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'user_data')

def load_load_curve():
    """读取附件1：常规电负荷标幺曲线，返回24h标幺值数组"""
    df = pd.read_excel(os.path.join(DATA_DIR, '附件1：园区典型日常规电负荷标幺功率曲线.xlsx'))
    return df.iloc[:, 1].values.astype(float)

def load_typical_wind_pv():
    """读取附件2：典型日风光标幺曲线，返回(wind_pu, pv_pu)"""
    df = pd.read_excel(os.path.join(DATA_DIR, '附件2：典型日风电、光伏标幺功率表.xlsx'))
    wind_pu = df.iloc[:, 1].values.astype(float)
    pv_pu = df.iloc[:, 2].values.astype(float)
    return wind_pu, pv_pu

def load_wind_scenarios():
    """读取附件3：6种风电场景，返回(24, 6)数组"""
    df = pd.read_excel(os.path.join(DATA_DIR, '附件3：园区6种场景的风电标幺功率表.xlsx'))
    return df.iloc[:, 1:7].values.astype(float)

def load_pv_scenarios():
    """读取附件4：4种光伏场景，返回(24, 4)数组"""
    df = pd.read_excel(os.path.join(DATA_DIR, '附件4：园区4种场景的光伏标幺功率表.xlsx'))
    return df.iloc[:, 1:5].values.astype(float)

def load_prices():
    """构建24h分时电价数组（元/kWh）"""
    # 高峰: 10:00-15:00 (h10-14), 18:00-21:00 (h18-20)
    # 平时: 07:00-10:00 (h7-9), 15:00-18:00 (h15-17), 21:00-23:00 (h21-22)
    # 低谷: 23:00-次日07:00 (h23, h0-6)
    prices = np.zeros(24)
    peak_hours = [10, 11, 12, 13, 14, 18, 19, 20]
    flat_hours = [7, 8, 9, 15, 16, 17, 21, 22]
    valley_hours = [23, 0, 1, 2, 3, 4, 5, 6]
    for h in peak_hours:
        prices[h] = 0.8024
    for h in flat_hours:
        prices[h] = 0.6074
    for h in valley_hours:
        prices[h] = 0.3424
    return prices

def get_sell_price():
    """上网电价"""
    return 0.3779

# 设备参数
PARAMS_BASE = {
    'P_ALK': 10.0,       # MW
    'P_PEM': 10.0,       # MW
    'P_NH3': 0.75,       # MW
    'm_H2_ALK': 140.0,   # kg/h
    'm_H2_PEM': 160.0,   # kg/h
    'm_NH3': 1.5,        # t/h (1500 kg/h)
    'c_om_ALK': 0.1,     # 元/kWh
    'c_om_PEM': 0.15,    # 元/kWh
    'c_om_NH3': 0.002,   # 元/kWh
    'c_wind': 0.15,      # 元/kWh
    'c_pv': 0.12,        # 元/kWh
}

PARAMS_EXPANDED = {
    'P_ALK': 20.0,
    'P_PEM': 20.0,
    'P_NH3': 1.5,
    'm_H2_ALK': 280.0,
    'm_H2_PEM': 320.0,
    'm_NH3': 3.0,        # t/h
    'c_om_ALK': 0.1,
    'c_om_PEM': 0.15,
    'c_om_NH3': 0.002,
    'c_wind': 0.15,
    'c_pv': 0.12,
}

# 风电/光伏装机容量
P_WIND_CAP = 40.0  # MW
P_PV_CAP = 64.0    # MW
P_LOAD_PEAK = 6.0  # MW

# 储能参数
STORAGE_PARAMS = {
    'eta_c': 0.90,
    'eta_d': 0.90,
    'sigma': 0.002,       # 自损耗率 /h
    'invest_cost': 1000,  # 元/kWh = 100万元/MWh
    'lifetime_years': 15,
    'om_cost': 0.01,      # 元/kWh
}

PRODUCTION_LEVELS = [72, 63, 54, 45, 36]  # t/d
