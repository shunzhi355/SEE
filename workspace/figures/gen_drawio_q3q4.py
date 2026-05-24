#!/usr/bin/env python3
"""Generate Q3, Q4 flow and energy topology DrawIO files."""
import os

# 1. 获取当前脚本所在的绝对路径 (也就是 workspace/figures/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. 如果你想把生成的 drawio 文件直接保存在脚本同级目录下，可以直接设为空或 "."
# 如果你想在脚本所在的目录下再建一个 figures 文件夹，就保持 "figures"
OUT_DIR = os.path.join(SCRIPT_DIR, ".") 

def write_file(filename, content):
    # 3. 关键一步：如果目标文件夹不存在，自动创建它！
    os.makedirs(OUT_DIR, exist_ok=True)
    
    path = os.path.join(OUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path} ({len(content)} bytes)")

OUT_DIR = "figures"

def write_file(filename, content):
    path = os.path.join(OUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path} ({len(content)} bytes)")

def q3_flow():
    xml = '<mxfile host="draw.io"><diagram name="Q3" id="fq3"><mxGraphModel dx="900" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="900" pageHeight="700" background="none" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
    # Start node
    xml += '<mxCell id="n1" value="&lt;b&gt;设定产能与碳市参数&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;功率连续可调(10%-100%)，引入碳价与排放因子&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="180" y="15" width="340" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e1" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="57" as="sourcePoint"/><mxPoint x="350" y="80" as="targetPoint"/></mxGeometry></mxCell>'
    # LP model (加入CCER)
    xml += '<mxCell id="n2" value="&lt;b&gt;构建线性规划(LP)模型&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;目标：融合CCER机制，最小化综合吨氨净成本&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0ECF5;strokeColor=#9A8AB0;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="170" y="80" width="360" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e2" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="122" as="sourcePoint"/><mxPoint x="350" y="145" as="targetPoint"/></mxGeometry></mxCell>'
    # Constraints
    xml += '<mxCell id="n3" value="&lt;b&gt;约束条件&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;功率平衡 + 日产量约束 + 绿电合规约束&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7AAA7A;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="170" y="145" width="360" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e3" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="187" as="sourcePoint"/><mxPoint x="350" y="210" as="targetPoint"/></mxGeometry></mxCell>'
    # Solve
    xml += '<mxCell id="n4" value="&lt;b&gt;HiGHS 求解器高效寻优&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;隐式调整购售电惩罚权重，获取最优调度&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="200" y="210" width="300" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e4" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="252" as="sourcePoint"/><mxPoint x="350" y="275" as="targetPoint"/></mxGeometry></mxCell>'
    # 24 scenarios
    xml += '<mxCell id="n5" value="&lt;b&gt;24场景遍历求解&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;6种风电 × 4种光伏 = 24种组合&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7AAA7A;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="200" y="275" width="300" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e5" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="317" as="sourcePoint"/><mxPoint x="350" y="340" as="targetPoint"/></mxGeometry></mxCell>'
    # Compare
    xml += '<mxCell id="n6" value="&lt;b&gt;统计分析&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;全年加权吨氨净成本 + 累计生态碳减排红利&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="170" y="340" width="360" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e6" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="382" as="sourcePoint"/><mxPoint x="350" y="405" as="targetPoint"/></mxGeometry></mxCell>'
    # Compare with Q2
    xml += '<mxCell id="n7" value="&lt;b&gt;与问题二对比分析&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;经济性与绿电指标的改善量评估&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#E8B860;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="200" y="405" width="300" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e7" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="447" as="sourcePoint"/><mxPoint x="350" y="470" as="targetPoint"/></mxGeometry></mxCell>'
    # Output
    xml += '<mxCell id="n8" value="&lt;b&gt;输出结果&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;柔性调度方案 + 净成本分布曲线 + 碳减排效益&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F0E8;strokeColor=#5A8A5A;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="170" y="470" width="360" height="42" as="geometry"/></mxCell>'
    # Tools box (加入 CCER)
    xml += '<mxCell id="tools" value="&lt;b&gt;工具与方法&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;线性规划(LP)&lt;br&gt;CCER基准线法&lt;br&gt;连续柔性调节&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0ECF5;strokeColor=#C8BCD8;strokeWidth=1.5;fontSize=10;fontStyle=1;verticalAlign=top;spacingTop=2;" vertex="1" parent="1"><mxGeometry x="620" y="150" width="140" height="90" as="geometry"/></mxCell>'
    xml += '</root></mxGraphModel></diagram></mxfile>'
    write_file("fig_flow_q3.drawio", xml)

def q4_flow():
    xml = '<mxfile host="draw.io"><diagram name="Q4" id="fq4"><mxGraphModel dx="900" dy="750" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="900" pageHeight="750" background="none" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
    # Start
    xml += '<mxCell id="n1" value="&lt;b&gt;离网运行模式&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;断开外部电网，仅靠风光发电&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="220" y="15" width="280" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e1" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.25;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="290" y="57" as="sourcePoint"/><mxPoint x="190" y="85" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="e1b" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.75;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="430" y="57" as="sourcePoint"/><mxPoint x="530" y="85" as="targetPoint"/></mxGeometry></mxCell>'
    # Two parallel branches
    xml += '<mxCell id="n2a" value="&lt;b&gt;(1) 无储能调度&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;风光功率约束下产量&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7AAA7A;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="80" y="85" width="220" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="n2b" value="&lt;b&gt;(2) 储能配置优化&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;最大弃电场景储能容量&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#9A8AB0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="420" y="85" width="220" height="42" as="geometry"/></mxCell>'
    # Left branch continues
    xml += '<mxCell id="e2a" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="190" y="127" as="sourcePoint"/><mxPoint x="190" y="155" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="n3a" value="&lt;b&gt;连续功率调节&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;电解槽功率 = min(风光, 额定)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7AAA7A;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="70" y="155" width="240" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e3a" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="190" y="197" as="sourcePoint"/><mxPoint x="190" y="225" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="n4a" value="&lt;b&gt;计算各场景产量&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;全年制氨总量 + 年平均产能利用率&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7AAA7A;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="60" y="225" width="260" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e4a" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="190" y="267" as="sourcePoint"/><mxPoint x="190" y="295" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="n5a" value="&lt;b&gt;估算最小装机容量&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;能源自治的风/光装机下限&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="60" y="295" width="260" height="42" as="geometry"/></mxCell>'
    # Right branch continues
    xml += '<mxCell id="e2b" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="530" y="127" as="sourcePoint"/><mxPoint x="530" y="155" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="n3b" value="&lt;b&gt;识别最大弃电场景&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;风光出力最大时弃电最多&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#9A8AB0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="410" y="155" width="240" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e3b" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="530" y="197" as="sourcePoint"/><mxPoint x="530" y="225" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="n4b" value="&lt;b&gt;储能容量优化&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;最小化弃电 + SOC约束 + 充放电功率&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0ECF5;strokeColor=#9A8AB0;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="400" y="225" width="260" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e4b" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="530" y="267" as="sourcePoint"/><mxPoint x="530" y="295" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="n5b" value="&lt;b&gt;24场景储能调度&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;有储能参与的功率最优调度&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#9A8AB0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="410" y="295" width="240" height="42" as="geometry"/></mxCell>'
    # Merge
    xml += '<mxCell id="e5a" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.25;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="190" y="337" as="sourcePoint"/><mxPoint x="280" y="370" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="e5b" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.75;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="530" y="337" as="sourcePoint"/><mxPoint x="440" y="370" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="n6" value="&lt;b&gt;(3) 经济性对比分析&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;离网 vs 联网：全年吨氨成本对比&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="180" y="370" width="360" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e6" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="360" y="412" as="sourcePoint"/><mxPoint x="360" y="440" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="n7" value="&lt;b&gt;系统支撑成本价值&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;储能带来的能源自给与风光利用改善&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#E8B860;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="180" y="440" width="360" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e7" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="360" y="482" as="sourcePoint"/><mxPoint x="360" y="510" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="n8" value="&lt;b&gt;输出综合结果&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;储能配置方案 + 经济性分析 + 运行模式建议&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F0E8;strokeColor=#5A8A5A;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="180" y="510" width="360" height="42" as="geometry"/></mxCell>'
    # Tools
    xml += '<mxCell id="tools" value="&lt;b&gt;工具与方法&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;线性规划(LP)&lt;br&gt;储能 SOC 模型&lt;br&gt;经济性对比分析&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F0E8;strokeColor=#DDD4C0;strokeWidth=1.5;fontSize=10;fontStyle=1;verticalAlign=top;spacingTop=2;" vertex="1" parent="1"><mxGeometry x="620" y="220" width="150" height="90" as="geometry"/></mxCell>'
    xml += '</root></mxGraphModel></diagram></mxfile>'
    write_file("fig_flow_q4.drawio", xml)

def energy_topology():
    xml = '<mxfile host="draw.io"><diagram name="energy" id="etopo"><mxGraphModel dx="900" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="900" pageHeight="600" background="none" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
    # External grid
    xml += '<mxCell id="grid" value="&lt;b&gt;外部电网&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;购电/售电&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5EDED;strokeColor=#B08080;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="380" y="15" width="140" height="42" as="geometry"/></mxCell>'
    # Wind
    xml += '<mxCell id="wind" value="&lt;b&gt;风电&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;40MW&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0ECF8;strokeColor=#6c8ebf;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="60" y="120" width="120" height="42" as="geometry"/></mxCell>'
    # PV
    xml += '<mxCell id="pv" value="&lt;b&gt;光伏&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;64MW&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF5E6;strokeColor=#E8B860;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="60" y="200" width="120" height="42" as="geometry"/></mxCell>'
    # Bus bar
    xml += '<mxCell id="bus" value="&lt;b&gt;园区母线&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=2.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="280" y="140" width="140" height="36" as="geometry"/></mxCell>'
    # Storage
    xml += '<mxCell id="stor" value="&lt;b&gt;储能&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;电池储能&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F0E8;strokeColor=#5A8A5A;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="500" y="120" width="120" height="42" as="geometry"/></mxCell>'
    # ALKEL
    xml += '<mxCell id="alkel" value="&lt;b&gt;碱性电解槽&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;ALKEL 10MW&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0ECF8;strokeColor=#6c8ebf;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="200" y="260" width="140" height="42" as="geometry"/></mxCell>'
    # PEMEL
    xml += '<mxCell id="pemel" value="&lt;b&gt;质子交换膜电解槽&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;PEMEL 10MW&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0ECF8;strokeColor=#6c8ebf;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="380" y="260" width="160" height="42" as="geometry"/></mxCell>'
    # Load
    xml += '<mxCell id="load" value="&lt;b&gt;常规电负荷&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;峰值 6MW&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#999999;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="600" y="260" width="120" height="42" as="geometry"/></mxCell>'
    # Ammonia synthesis
    xml += '<mxCell id="nh3" value="&lt;b&gt;合成氨装置&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;0.75MW, 1.5吨/h&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0ECF5;strokeColor=#9A8AB0;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="280" y="380" width="160" height="42" as="geometry"/></mxCell>'
    # Ammonia output
    xml += '<mxCell id="nh3out" value="&lt;b&gt;氨产品输出&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;36-72吨/日&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5EDED;strokeColor=#B08080;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="280" y="470" width="160" height="42" as="geometry"/></mxCell>'
    # Edges: wind/pv to bus
    xml += '<mxCell id="ew" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=2;strokeColor=#6c8ebf;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.3;"><mxGeometry relative="1" as="geometry"><mxPoint x="180" y="141" as="sourcePoint"/><mxPoint x="280" y="151" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="epv" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=2;strokeColor=#E8B860;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.7;"><mxGeometry relative="1" as="geometry"><mxPoint x="180" y="221" as="sourcePoint"/><mxPoint x="280" y="165" as="targetPoint"/></mxGeometry></mxCell>'
    # Bus to grid (bidirectional)
    xml += '<mxCell id="eg" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=2;strokeColor=#B08080;endArrow=block;endFill=1;startArrow=block;startFill=1;exitX=0.5;exitY=0;entryX=0.5;entryY=1;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="140" as="sourcePoint"/><mxPoint x="450" y="57" as="targetPoint"/></mxGeometry></mxCell>'
    # Bus to storage
    xml += '<mxCell id="es" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=2;strokeColor=#5A8A5A;endArrow=block;endFill=1;startArrow=block;startFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;"><mxGeometry relative="1" as="geometry"><mxPoint x="420" y="158" as="sourcePoint"/><mxPoint x="500" y="141" as="targetPoint"/></mxGeometry></mxCell>'
    # Bus to electrolyzers
    xml += '<mxCell id="ea" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=2;strokeColor=#6c8ebf;endArrow=block;endFill=1;exitX=0.3;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="322" y="176" as="sourcePoint"/><mxPoint x="270" y="260" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="ep" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=2;strokeColor=#6c8ebf;endArrow=block;endFill=1;exitX=0.7;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="378" y="176" as="sourcePoint"/><mxPoint x="460" y="260" as="targetPoint"/></mxGeometry></mxCell>'
    # Bus to load
    xml += '<mxCell id="el" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=2;strokeColor=#999999;endArrow=block;endFill=1;exitX=1;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="420" y="176" as="sourcePoint"/><mxPoint x="660" y="260" as="targetPoint"/></mxGeometry></mxCell>'
    # H2 flow: electrolyzers to NH3
    xml += '<mxCell id="eh1" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=2;strokeColor=#7AAA7A;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.3;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="270" y="302" as="sourcePoint"/><mxPoint x="328" y="380" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="eh2" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=2;strokeColor=#7AAA7A;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.7;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="460" y="302" as="sourcePoint"/><mxPoint x="392" y="380" as="targetPoint"/></mxGeometry></mxCell>'
    # NH3 to output
    xml += '<mxCell id="en" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=2;strokeColor=#9A8AB0;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="360" y="422" as="sourcePoint"/><mxPoint x="360" y="470" as="targetPoint"/></mxGeometry></mxCell>'
    # Legend
    xml += '<mxCell id="leg1" value="&lt;font style=&quot;font-size:9px;&quot;&gt;&lt;font color=&quot;#6c8ebf&quot;&gt;——&lt;/font&gt; 电力流  &lt;font color=&quot;#7AAA7A&quot;&gt;——&lt;/font&gt; 氢气流  &lt;font color=&quot;#9A8AB0&quot;&gt;——&lt;/font&gt; 氨流&lt;/font&gt;" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;strokeColor=none;fillColor=none;fontSize=10;" vertex="1" parent="1"><mxGeometry x="250" y="530" width="300" height="20" as="geometry"/></mxCell>'
    xml += '</root></mxGraphModel></diagram></mxfile>'
    write_file("fig_energy_topology.drawio", xml)

if __name__ == "__main__":
    q3_flow()
    q4_flow()
    energy_topology()
    print("All done!")
