import matplotlib.pyplot as plt

# 模拟脚本里需要导入的变量
PALETTE = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
COLORS = PALETTE

def _lighten(color, amount=0.5):
    """简单的颜色提亮函数"""
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

def setup_style():
    """设置matplotlib的基础样式"""
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.style.use('seaborn-v0_8-whitegrid')

def save_fig(fig, path, dpi=300, bbox_inches='tight'):
    """保存图片的函数"""
    fig.savefig(path, dpi=dpi, bbox_inches=bbox_inches)