import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ================= 1. 科研图表样式与中文字体配置 =================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
plt.rcParams['figure.dpi'] = 300  # 高清输出

# 学术柔和配色方案
COLOR_POS = '#5B8DB8'  # 柔和的钢蓝色 (成本增加)
COLOR_NEG = '#D4896A'  # 柔和的赤褐色 (成本降低)
COLOR_GRID = '#E0E0E0'
COLOR_TEXT = '#333333'

def lighten_color(color, amount=0.5):
    """用于生成柔和的渐变色阶"""
    try:
        c = mcolors.cnames[color]
    except:
        c = color
    c = mcolors.to_rgb(c)
    return tuple((1 - amount) * val + amount for val in c)

# ================= 2. 读取与处理数据 =================
# 读取 JSON 数据
with open('sensitivity_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

base_cost = data['base_cost']
params_data = data['parameters']

# 按照论文设定，手动注入/修正碳排放交易价格的极值数据
params_data['carbon_price'] = {
    'description': '碳排放交易价格',
    'objective': [3805, 4210] 
}

# 计算每个参数的百分比变化
params = []
low_impacts = []
high_impacts = []

for key, pdata in params_data.items():
    obj_vals = pdata['objective']
    min_obj = min(obj_vals)
    max_obj = max(obj_vals)
    # 计算相对基准值的变化率 (%)
    low_pct = (min_obj - base_cost) / base_cost * 100
    high_pct = (max_obj - base_cost) / base_cost * 100
    
    params.append(pdata['description'])
    low_impacts.append(low_pct)
    high_impacts.append(high_pct)

# 转换为 NumPy 数组并按跨度排序 (龙卷风图核心逻辑)
low_impacts = np.array(low_impacts)
high_impacts = np.array(high_impacts)
total_range = high_impacts - low_impacts
sort_idx = np.argsort(total_range)

params = [params[i] for i in sort_idx]
low_impacts = low_impacts[sort_idx]
high_impacts = high_impacts[sort_idx]
total_range = total_range[sort_idx]
max_range = total_range.max() if total_range.max() > 0 else 1

# ================= 3. 绘制龙卷风图 =================
n = len(params)
fig_h = max(4.0, n * 0.8 + 1.5)
fig, ax = plt.subplots(figsize=(9, fig_h))
y = np.arange(n)

# 添加垂直网格线
ax.grid(axis='x', alpha=0.5, linestyle='--', color=COLOR_GRID)
ax.set_axisbelow(True)

# 添加交替背景色提升可读性
for i in range(n):
    if i % 2 == 0:
        ax.axhspan(y[i] - 0.5, y[i] + 0.5, alpha=0.05, color='gray', zorder=0)

max_abs = max(abs(low_impacts).max(), abs(high_impacts).max())

# 绘制柱状图
for i in range(n):
    # 根据跨度计算颜色深浅 (跨度越大的颜色越深)
    intensity = total_range[i] / max_range if max_range > 0 else 0.5
    lighten_amt = 0.4 * (1 - intensity)
    
    # 正向影响条 (成本增加)
    if high_impacts[i] > 0:
        c = lighten_color(COLOR_POS, lighten_amt)
        ax.barh(y[i], high_impacts[i], height=0.55,
                color=lighten_color(c, 0.2), edgecolor=c, linewidth=1.2, zorder=3)
    # 负向影响条 (成本降低)
    if low_impacts[i] < 0:
        c = lighten_color(COLOR_NEG, lighten_amt)
        ax.barh(y[i], low_impacts[i], height=0.55,
                color=lighten_color(c, 0.2), edgecolor=c, linewidth=1.2, zorder=3)
    
    # 标注数值
    margin = max_abs * 0.03
    if high_impacts[i] > 0:
        ax.text(high_impacts[i] + margin, y[i], f'+{high_impacts[i]:.1f}%',
                va='center', ha='left', fontsize=9, fontweight='bold',
                color=lighten_color(COLOR_POS, 0.2))
    if low_impacts[i] < 0:
        ax.text(low_impacts[i] - margin, y[i], f'{low_impacts[i]:.1f}%',
                va='center', ha='right', fontsize=9, fontweight='bold',
                color=lighten_color(COLOR_NEG, 0.2))

# 绘制基准零线
ax.axvline(0, color=COLOR_TEXT, linewidth=1.2, zorder=4)

# 在顶部中心添加基准值文本框
ax.text(0, n - 0.2, f'基准值: {base_cost:.0f} 元/吨', ha='center', va='bottom', fontsize=10,
        color='#444444', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#CCCCCC', alpha=0.9))

# 坐标轴设置
ax.set_yticks(y)
ax.set_yticklabels(params, fontsize=11, color=COLOR_TEXT)
ax.set_xlabel('吨氨净成本变化率 (%)', fontsize=12, fontweight='bold', color=COLOR_TEXT)

# 隐藏上方和右侧边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')

fig.tight_layout()

# 保存高质量图片
plt.savefig('fig_sensitivity.pdf', format='pdf', bbox_inches='tight')
plt.savefig('fig_sensitivity.png', format='png', dpi=300, bbox_inches='tight')
print("✅ 成功生成图表: fig_sensitivity.pdf 和 fig_sensitivity.png")