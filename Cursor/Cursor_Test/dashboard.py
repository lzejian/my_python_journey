import random
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

# -------------------------------
# 【网页组件：浏览器标签页标题 + 页面整体宽度布局】
# 这一段代码会控制你的 Streamlit 页面“最外层配置”：
# 1) page_title 会显示在浏览器标签页上，让用户一眼知道这个页面是什么；
# 2) layout="wide" 会让页面采用宽屏布局，图表和表格更舒展，视觉上更像专业 BI 看板；
# 3) 这段配置必须尽量靠前执行，属于页面“初始化阶段”的全局设置。
# -------------------------------
st.set_page_config(
    page_title="跨界跃迁：我的第一个 AI 数据看板",
    layout="wide",
)

# -------------------------------
# 【网页组件：主标题（页面顶部大字标题）】
# 这一段会在主界面最上方渲染一个大标题：
# - 用户进入页面第一眼看到的就是它；
# - 对应你要求的标题文案“跨界跃迁：我的第一个 AI 数据看板”；
# - 这是整个看板的“门面组件”，负责建立主题和识别度。
# -------------------------------
st.title("跨界跃迁：我的第一个 AI 数据看板")

# -------------------------------
# 【网页组件：轻量视觉美化（渐变背景 + 卡片圆角）】
# 这一段通过 st.markdown 注入少量 CSS，让页面观感更“惊艳”：
# 1) 主体背景使用柔和渐变色，提升科技感与层次感；
# 2) 对图表/表格外层容器做圆角与半透明背景，形成“卡片式仪表盘”风格；
# 3) 不改变业务逻辑，只增强视觉表现，保持代码仍然极简。
# -------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f6f9ff 0%, #eef4ff 45%, #f8fbff 100%);
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 14px;
        padding: 10px 14px;
        border: 1px solid #e6ecff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# 【网页组件：数据源（内存中的模拟业务数据）】
# 这一段是“看板背后的数据引擎”，不会直接显示为单独控件，但会决定图表和表格展示什么：
# 1) 生成过去 30 天日期；
# 2) 每天为每个商品分类（电子、服装、食品）随机生成一条销售记录；
# 3) 最终得到一个 DataFrame，列包含 日期、商品分类、销售额；
# 4) 这份数据完全在内存中构建，无需读文件，适合教学和快速演示。
# -------------------------------
categories = ["电子", "服装", "食品"]
today = datetime.today().date()
records = []

for i in range(30):
    day = today - timedelta(days=29 - i)
    for category in categories:
        records.append(
            {
                "日期": day,
                "商品分类": category,
                "销售额": random.randint(2000, 12000),
            }
        )

df = pd.DataFrame(records)

# -------------------------------
# 【网页组件：左侧边栏 Sidebar + 多选框 Multiselect】
# 这一段会在页面左边创建一个交互区域（Sidebar）：
# 1) st.sidebar.header 是边栏的小标题，告诉用户“这里是筛选器”；
# 2) st.sidebar.multiselect 是多选框，允许用户同时选择多个商品分类；
# 3) default=categories 表示首次打开页面时默认全选，用户不会看到空图；
# 4) 用户每次勾选变化，页面会自动重算并刷新图表与表格（Streamlit 的响应式机制）。
# -------------------------------
st.sidebar.header("筛选条件")
selected_categories = st.sidebar.multiselect(
    "选择要查看的商品分类",
    options=categories,
    default=categories,
)

# -------------------------------
# 【网页组件：左侧边栏 Sidebar + 日期范围选择器】
# 这一段在侧边栏追加 date_input 日期区间组件：
# 1) 用户可以拖动起止日期，查看任意时间窗口的销售变化；
# 2) 默认范围就是最近 30 天全量数据，首次打开即有完整图表；
# 3) 该控件会与分类多选组合生效，形成“多维筛选”体验。
# -------------------------------
date_range = st.sidebar.date_input(
    "选择日期范围",
    value=(df["日期"].min(), df["日期"].max()),
    min_value=df["日期"].min(),
    max_value=df["日期"].max(),
)

# -------------------------------
# 【网页组件：筛选后的数据（供图表和表格共同使用）】
# 这一段不是直接可视控件，而是“图表和表格的共同数据输入层”：
# - 根据 Sidebar 多选结果过滤数据；
# - 只保留用户选择的商品分类；
# - 后续折线图与明细表都基于这个 filtered_df，保证视图一致性。
# -------------------------------
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = df["日期"].min(), df["日期"].max()

filtered_df = df[
    (df["商品分类"].isin(selected_categories))
    & (df["日期"] >= start_date)
    & (df["日期"] <= end_date)
].copy()

# -------------------------------
# 【网页组件：核心图表区（st.line_chart 折线趋势图）】
# 这一段负责在主界面中部绘制“销售趋势折线图”：
# 1) 先按“日期 + 商品分类”聚合，确保每天每类只有一个销售额点；
# 2) 再 pivot 成宽表：行是日期，列是商品分类，值是销售额；
# 3) st.line_chart 会把每个分类画成一条线，直观展示 30 天走势变化；
# 4) subheader 是图表小标题，帮助用户快速理解这个区域。
# -------------------------------
st.subheader("销售趋势（按商品分类）")

if filtered_df.empty:
    st.warning("当前没有可展示的数据，请在左侧至少选择一个商品分类。")
else:
    # -------------------------------
    # 【网页组件：KPI 指标卡（主界面顶部三列数字卡片）】
    # 这一段使用 st.columns + st.metric 生成 BI 常见“指标卡”：
    # 1) 总销售额：帮助用户先看全局规模；
    # 2) 日均销售额：快速感知业务稳定性；
    # 3) 记录条数：知道当前筛选后覆盖了多少明细数据；
    # 4) 这组卡片位于图表上方，属于“先总览、后下钻”的经典看板结构。
    # -------------------------------
    total_sales = float(filtered_df["销售额"].sum())
    day_count = max(1, filtered_df["日期"].nunique())
    avg_daily_sales = total_sales / day_count

    c1, c2, c3 = st.columns(3)
    c1.metric("总销售额", f"¥ {total_sales:,.0f}")
    c2.metric("日均销售额", f"¥ {avg_daily_sales:,.0f}")
    c3.metric("筛选后记录数", f"{len(filtered_df)}")

    trend_df = (
        filtered_df.groupby(["日期", "商品分类"], as_index=False)["销售额"]
        .sum()
        .pivot(index="日期", columns="商品分类", values="销售额")
        .sort_index()
    )
    st.line_chart(trend_df)

    # -------------------------------
    # 【网页组件：分类占比条形图（辅助洞察）】
    # 这一段新增一个“按分类汇总销售额”的可视化补充：
    # 1) 线图回答“趋势怎么变”，条形图回答“谁贡献最大”；
    # 2) 使用 Streamlit 原生 st.bar_chart，保持实现简洁、零额外依赖；
    # 3) 帮助用户快速比较电子/服装/食品的总量差异。
    # -------------------------------
    st.subheader("分类销售额对比")
    category_sales = (
        filtered_df.groupby("商品分类", as_index=True)["销售额"].sum().sort_values(ascending=False)
    )
    st.bar_chart(category_sales)

    # -------------------------------
    # 【网页组件：数据明细表（主界面下方漂亮表格）】
    # 这一段会在图表下方渲染“可滚动、可排序感知更强”的数据表：
    # 1) subheader 用于明确该区域是“明细数据”；
    # 2) st.dataframe 是 Streamlit 的交互式表格组件，比纯文本表更美观；
    # 3) use_container_width=True 让表格自动铺满容器宽度，视觉更整洁；
    # 4) hide_index=True 隐藏默认索引列，减少视觉噪音，让业务字段更突出。
    # -------------------------------
    st.subheader("筛选后数据明细")
    st.dataframe(
        filtered_df.sort_values(["日期", "商品分类"]),
        use_container_width=True,
        hide_index=True,
    )

    # -------------------------------
    # 【网页组件：下载按钮（交付能力）】
    # 这一段在表格下方放置 st.download_button：
    # 1) 用户可以一键下载“当前筛选结果”CSV；
    # 2) 下载内容与页面筛选完全一致，便于汇报和二次分析；
    # 3) 这是看板从“看数据”到“带走数据”的关键闭环组件。
    # -------------------------------
    csv_data = filtered_df.sort_values(["日期", "商品分类"]).to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="下载当前筛选数据（CSV）",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )
