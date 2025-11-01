"""
演示可视化需求:折线图1
"""

# 处理数据
f_cn = open(r"F:\visual studio code\python\python self learning\day 8 作图/中国.txt","r",encoding="utf-8")
cn_data = f_cn.read()
from pyecharts.charts import Line
from pyecharts.options import TitleOpts, LegendOpts, ToolboxOpts, VisualMapOpts,LabelOpts

# 去掉不合规的开头
new_cn_data = cn_data.replace("#45dsa","")

# 去掉不合规的结尾
new_cn_data1 = new_cn_data[:-3]

# json转python字典
import json
cn_dict = json.loads(new_cn_data1)  # 想想为什么要把json转成字典？json本身是什么类型？

# 获取trend key
trend_data = cn_dict["data"]["trend"] # trend_data的结构是一个字典，包含了日期和确诊人数等信息

# 创建一个直线图对象
line = Line()  # 这一步的目的是为了做一个坐标系

# 获取日期数据，用于x轴，取到2020年结尾
x_data = trend_data["dates"][:trend_data["dates"].index("2021-02-10")]
line.add_xaxis(x_data)

# 获取确诊数据，用于y轴
y_data = trend_data["diagnosed"][:trend_data["dates"].index("2021-02-10")]
line.add_yaxis("确诊人数", y_data,label_opts = LabelOpts(is_show=False))

# 全局配置 set_global_opts来为图像添砖加瓦
line.set_global_opts(
    title_opts=TitleOpts(title="美国疫情趋势图", pos_left="37%", pos_bottom="2%"),
    legend_opts=LegendOpts(is_show=True),
    toolbox_opts=ToolboxOpts(is_show=True),
    visualmap_opts=VisualMapOpts(is_show=True),
)

# 关闭文件，创造图标
f_cn.close()
line.render("美国疫情趋势图.html")  # 通过render方法，将代码生成为图像
                                   # 注意：render方法会覆盖同名文件，如果不想覆盖，可以改文件名



