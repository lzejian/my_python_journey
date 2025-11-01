"""
演示pyecharts的基本入门
"""

# 导包 
from pyecharts.charts import Line
from pyecharts.options import TitleOpts,LegendOpts,ToolboxOpts,VisualMapOpts


# 创建一个直线图对象
line = Line()      # 这一步的目的是为了做一个坐标系

# 给折线图添加x轴数据
line.add_xaxis(["China","America","Japan"])

# 给折线图添加x轴数据
line.add_yaxis("GDP",[30,20,10])
line.add_yaxis("population",[1400,350,150])

# 没有这一串代码也可以运行，但是不够完美，只有最最基本的折线图
# 通过全局配置set_global_opts来为图像添砖加瓦
line.set_global_opts(title_opts = TitleOpts(title = "GDP and Population show",pos_left = "37%",pos_bottom= "2%"),
                     legend_opts = LegendOpts(is_show = True),
                     toolbox_opts = ToolboxOpts(is_show=True),
                     visualmap_opts = VisualMapOpts(is_show = True))

# 通过render方法，将代码生成为图像
line.render()