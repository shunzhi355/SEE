# 图表生成报告

## 生成概况

- 数据图表: 14 张 PDF
- LaTeX 表格: 8 个 .tex 文件
- LaTeX 引用文件: figures/latex_includes.tex
- DrawIO 架构图: 待下一步骤生成

## 图表清单

### 问题一
| 文件 | 类型 | 说明 |
|------|------|------|
| fig_q1_power_balance.pdf | 面积图 | 典型日功率平衡曲线 |
| fig_q1_power_detail.pdf | 双轴图 | 风光发电与负荷功率对比 |
| TABLE_q1_indicators.tex | 表格 | 电量指标及绿电指标汇总 |

### 问题二
| 文件 | 类型 | 说明 |
|------|------|------|
| fig_q2_gantt.pdf | 甘特图 | 各产量最优开机时段 |
| fig_q2_cost_compare.pdf | 柱状图 | 不同产量吨氨成本对比 |
| fig_q2_indicators.pdf | 雷达图 | 各产量绿电指标对比 |
| fig_q2_scenario_heatmap.pdf | 热力图 | 24场景×5产量成本矩阵 |
| fig_q2_annual_cost.pdf | 折线图 | 全年吨氨成本分布 |
| TABLE_q2_typical.tex | 表格 | 典型场景各产量方案对比 |
| TABLE_q2_annual.tex | 表格 | 全年绿电指标统计 |

### 问题三
| 文件 | 类型 | 说明 |
|------|------|------|
| fig_q3_dispatch.pdf | 面积图 | 连续调度功率分配 |
| fig_q3_annual_cost.pdf | 折线图 | Q2与Q3成本对比 |
| fig_q3_compare.pdf | 发散柱状图 | Q3相对Q2指标变化 |
| TABLE_q3_scenarios.tex | 表格 | 24场景最优方案汇总 |
| TABLE_q3_compare.tex | 表格 | Q2与Q3关键指标对比 |

### 问题四
| 文件 | 类型 | 说明 |
|------|------|------|
| fig_q4_offgrid_production.pdf | 堆叠柱状图 | 离网产量与电量分布 |
| fig_q4_storage_dispatch.pdf | 面积图 | 储能充放电调度 |
| fig_q4_economics.pdf | 分组柱状图 | 离网vs联网经济性 |
| TABLE_q4_offgrid.tex | 表格 | 离网各场景产量成本 |
| TABLE_q4_storage.tex | 表格 | 储能配置方案 |
| TABLE_q4_economics.tex | 表格 | 经济性对比 |

### 灵敏度分析
| 文件 | 类型 | 说明 |
|------|------|------|
| fig_sensitivity.pdf | 龙卷风图 | 参数灵敏度分析 |

## 图表多样性
- 面积图: 3次
- 折线图: 2次
- 柱状图: 2次
- 双轴图: 1次
- 甘特图: 1次
- 雷达图: 1次
- 热力图: 1次
- 发散柱状图: 1次
- 堆叠柱状图: 1次
- 龙卷风图: 1次

共10种不同图表类型，多样性合格。

## 质量检查
- ✅ 所有14个脚本均成功生成PDF
- ✅ 所有PDF文件大小正常（18-48KB）
- ✅ 8个LaTeX表格全部生成
- ✅ latex_includes.tex 已生成
- ✅ 使用统一调色板（setup_style）
- ✅ 无plt.title()（标题在LaTeX caption中）
- ✅ 中文标签和图例
