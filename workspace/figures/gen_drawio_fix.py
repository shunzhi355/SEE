#!/usr/bin/env python3
"""Fix Q3 and Q4 flow diagrams by adding decision diamond nodes."""
import os

OUT_DIR = "figures"

def write_file(filename, content):
    path = os.path.join(OUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path} ({len(content)} bytes)")

def q3_flow_fixed():
    xml = '<mxfile host="draw.io"><diagram name="Q3" id="fq3"><mxGraphModel dx="900" dy="750" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="900" pageHeight="750" background="none" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
    
    # 1. Start node (加入碳价参数)
    xml += '<mxCell id="n1" value="&lt;b&gt;设定产能与碳市参数&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;功率连续可调(10%-100%)，引入碳价与排放因子&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="200" y="15" width="300" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e1" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="57" as="sourcePoint"/><mxPoint x="350" y="80" as="targetPoint"/></mxGeometry></mxCell>'
    
    # 2. LP model (加入 CCER 目标)
    xml += '<mxCell id="n2" value="&lt;b&gt;构建线性规划(LP)模型&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;目标: 融合CCER机制，最小化综合吨氨净成本&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0ECF5;strokeColor=#9A8AB0;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="170" y="80" width="360" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e2" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="122" as="sourcePoint"/><mxPoint x="350" y="145" as="targetPoint"/></mxGeometry></mxCell>'
    
    # 3. Constraints
    xml += '<mxCell id="n3" value="&lt;b&gt;约束条件&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;功率上下限 + 日产量约束 + 绿电合规约束&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7AAA7A;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="170" y="145" width="360" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e3" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="187" as="sourcePoint"/><mxPoint x="350" y="210" as="targetPoint"/></mxGeometry></mxCell>'
    
    # 4. Solve (HiGHS求解)
    xml += '<mxCell id="n4" value="&lt;b&gt;HiGHS 求解器高效寻优&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;碳收益隐式调整边际惩罚，获取最优调度&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="200" y="210" width="300" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e4" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="252" as="sourcePoint"/><mxPoint x="350" y="280" as="targetPoint"/></mxGeometry></mxCell>'
    
    # 5. Decision diamond - feasible? (保留高级菱形框)
    xml += '<mxCell id="n5" value="&lt;b&gt;求解可行?&lt;/b&gt;" style="rhombus;whiteSpace=wrap;html=1;fillColor=#F5F0E8;strokeColor=#B0A080;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="290" y="280" width="120" height="70" as="geometry"/></mxCell>'
    
    # Yes branch
    xml += '<mxCell id="e5y" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#7AAA7A;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="350" as="sourcePoint"/><mxPoint x="350" y="380" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="lb5y" value="&lt;font style=&quot;font-size:10px;color:#7AAA7A;&quot;&gt;&lt;b&gt;是&lt;/b&gt;&lt;/font&gt;" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;strokeColor=none;fillColor=none;" vertex="1" parent="1"><mxGeometry x="355" y="355" width="25" height="18" as="geometry"/></mxCell>'
    
    # No branch - relax constraints
    xml += '<mxCell id="e5n" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#B08080;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=1;entryY=0.5;"><mxGeometry relative="1" as="geometry"><mxPoint x="410" y="315" as="sourcePoint"/><mxPoint x="530" y="166" as="targetPoint"/><Array as="points"><mxPoint x="600" y="315"/><mxPoint x="600" y="166"/></Array></mxGeometry></mxCell>'
    xml += '<mxCell id="lb5n" value="&lt;font style=&quot;font-size:10px;color:#B08080;&quot;&gt;&lt;b&gt;否（降低产量）&lt;/b&gt;&lt;/font&gt;" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;strokeColor=none;fillColor=none;" vertex="1" parent="1"><mxGeometry x="510" y="290" width="100" height="18" as="geometry"/></mxCell>'
    
    # 6. 24 scenarios
    xml += '<mxCell id="n6" value="&lt;b&gt;24场景遍历求解&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;6种风电 × 4种光伏 = 24种组合&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7AAA7A;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="200" y="380" width="300" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e6" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="422" as="sourcePoint"/><mxPoint x="350" y="450" as="targetPoint"/></mxGeometry></mxCell>'
    
    # 7. Statistics (加入碳减排分析)
    xml += '<mxCell id="n7" value="&lt;b&gt;统计分析 + 与问题二对比&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;累计碳减排效益与经济性/绿电指标综合评估&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="160" y="450" width="380" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e7" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="350" y="492" as="sourcePoint"/><mxPoint x="350" y="520" as="targetPoint"/></mxGeometry></mxCell>'
    
    # 8. Output
    xml += '<mxCell id="n8" value="&lt;b&gt;输出结果&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;柔性调度方案 + 净成本分布曲线 + 脱碳生态红利&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F0E8;strokeColor=#5A8A5A;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="160" y="520" width="380" height="42" as="geometry"/></mxCell>'
    
    # 9. Tools (侧边栏工具说明加入 CCER)
    xml += '<mxCell id="tools" value="&lt;b&gt;工具与方法&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;线性规划(LP)&lt;br&gt;CCER基准线法&lt;br&gt;连续功率调节&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0ECF5;strokeColor=#C8BCD8;strokeWidth=1.5;fontSize=10;fontStyle=1;verticalAlign=top;spacingTop=2;" vertex="1" parent="1"><mxGeometry x="620" y="150" width="140" height="90" as="geometry"/></mxCell>'
    
    xml += '</root></mxGraphModel></diagram></mxfile>'
    write_file("fig_flow_q3.drawio", xml)

def q4_flow_fixed():
    xml = '<mxfile host="draw.io"><diagram name="Q4" id="fq4"><mxGraphModel dx="900" dy="750" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="900" pageHeight="750" background="none" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
    # Start
    xml += '<mxCell id="n1" value="&lt;b&gt;离网运行模式&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;断开外部电网，仅靠风光发电&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="220" y="15" width="280" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e1" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="360" y="57" as="sourcePoint"/><mxPoint x="360" y="80" as="targetPoint"/></mxGeometry></mxCell>'
    # Compute available power
    xml += '<mxCell id="n2" value="&lt;b&gt;计算可用风光功率&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;每时段可用电力 = 风电 + 光伏 - 常规负荷&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7AAA7A;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="180" y="80" width="360" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e2" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="360" y="122" as="sourcePoint"/><mxPoint x="360" y="150" as="targetPoint"/></mxGeometry></mxCell>'
    # Decision: enough power?
    xml += '<mxCell id="n3" value="&lt;b&gt;可用功率 &amp;gt;&lt;br&gt;最低运行功率(10%)?&lt;/b&gt;" style="rhombus;whiteSpace=wrap;html=1;fillColor=#F5F0E8;strokeColor=#B0A080;strokeWidth=1.5;fontSize=10;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="290" y="150" width="140" height="80" as="geometry"/></mxCell>'
    # Yes - produce
    xml += '<mxCell id="e3y" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#7AAA7A;endArrow=block;endFill=1;exitX=0;exitY=0.5;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="290" y="190" as="sourcePoint"/><mxPoint x="160" y="260" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="lb3y" value="&lt;font style=&quot;font-size:10px;color:#7AAA7A;&quot;&gt;&lt;b&gt;是&lt;/b&gt;&lt;/font&gt;" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;strokeColor=none;fillColor=none;" vertex="1" parent="1"><mxGeometry x="230" y="180" width="30" height="18" as="geometry"/></mxCell>'
    # No - curtail
    xml += '<mxCell id="e3n" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#B08080;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="430" y="190" as="sourcePoint"/><mxPoint x="560" y="260" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="lb3n" value="&lt;font style=&quot;font-size:10px;color:#B08080;&quot;&gt;&lt;b&gt;否&lt;/b&gt;&lt;/font&gt;" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;strokeColor=none;fillColor=none;" vertex="1" parent="1"><mxGeometry x="440" y="180" width="30" height="18" as="geometry"/></mxCell>'
    # Left: produce at available power
    xml += '<mxCell id="n4a" value="&lt;b&gt;按可用功率生产&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;电解槽功率 = min(可用, 额定)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#7AAA7A;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="60" y="260" width="200" height="42" as="geometry"/></mxCell>'
    # Right: curtailment
    xml += '<mxCell id="n4b" value="&lt;b&gt;停机/弃电&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;该时段不生产，风光弃电&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5EDED;strokeColor=#B08080;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="460" y="260" width="200" height="42" as="geometry"/></mxCell>'
    # Merge
    xml += '<mxCell id="e4a" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.25;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="160" y="302" as="sourcePoint"/><mxPoint x="280" y="335" as="targetPoint"/></mxGeometry></mxCell>'
    xml += '<mxCell id="e4b" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.75;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="560" y="302" as="sourcePoint"/><mxPoint x="440" y="335" as="targetPoint"/></mxGeometry></mxCell>'
    # Calculate daily production
    xml += '<mxCell id="n5" value="&lt;b&gt;统计24场景日产量与弃电量&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;全年制氨总量 + 年平均产能利用率&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F4FA;strokeColor=#7B9FC0;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="180" y="335" width="360" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e5" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="360" y="377" as="sourcePoint"/><mxPoint x="360" y="405" as="targetPoint"/></mxGeometry></mxCell>'
    # Storage optimization
    xml += '<mxCell id="n6" value="&lt;b&gt;储能容量优化配置&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;最大弃电场景，最小化弃电 + SOC约束&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0ECF5;strokeColor=#9A8AB0;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="180" y="405" width="360" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e6" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="360" y="447" as="sourcePoint"/><mxPoint x="360" y="475" as="targetPoint"/></mxGeometry></mxCell>'
    # Economic comparison
    xml += '<mxCell id="n7" value="&lt;b&gt;经济性对比分析&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;离网 vs 联网：全年吨氨成本 + 系统支撑成本&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#E8B860;strokeWidth=1.5;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="180" y="475" width="360" height="42" as="geometry"/></mxCell>'
    xml += '<mxCell id="e7" edge="1" parent="1" style="rounded=1;html=1;strokeWidth=1.5;strokeColor=#999999;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"><mxGeometry relative="1" as="geometry"><mxPoint x="360" y="517" as="sourcePoint"/><mxPoint x="360" y="545" as="targetPoint"/></mxGeometry></mxCell>'
    # Output
    xml += '<mxCell id="n8" value="&lt;b&gt;输出综合结果&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;储能配置 + 经济性分析 + 运行模式建议&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F0E8;strokeColor=#5A8A5A;strokeWidth=2;fontSize=11;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="180" y="545" width="360" height="42" as="geometry"/></mxCell>'
    # Tools
    xml += '<mxCell id="tools" value="&lt;b&gt;工具与方法&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888;&quot;&gt;线性规划(LP)&lt;br&gt;储能 SOC 模型&lt;br&gt;经济性对比分析&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F0E8;strokeColor=#DDD4C0;strokeWidth=1.5;fontSize=10;fontStyle=1;verticalAlign=top;spacingTop=2;" vertex="1" parent="1"><mxGeometry x="620" y="260" width="150" height="90" as="geometry"/></mxCell>'
    xml += '</root></mxGraphModel></diagram></mxfile>'
    write_file("fig_flow_q4.drawio", xml)

if __name__ == "__main__":
    q3_flow_fixed()
    q4_flow_fixed()
    print("Fixed Q3 and Q4 with diamond decision nodes!")
