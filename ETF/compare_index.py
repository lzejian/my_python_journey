import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 0. 自动获取当前脚本所在的绝对路径 (解决找不到文件的问题)
# ==========================================
# __file__ 代表当前代码文件，这行代码能精准抓取到它所在的文件夹路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 拼凑出绝对路径：比如 f:\my_python_journey\ETF\sox_data.csv
sox_path = os.path.join(current_dir, 'sox_data.csv')
ndx_path = os.path.join(current_dir, 'ndx_data.csv')

# ==========================================
# 1. 读取并清洗 SOX 数据 (半导体指数)
# ==========================================
print("正在读取本地 SOX 数据...")
df_sox = pd.read_csv(sox_path) # 这里使用刚才拼好的绝对路径变量

df_sox = df_sox[['日期', '收盘']].rename(columns={'日期': 'Date', '收盘': 'SOX_Close'})
df_sox['Date'] = pd.to_datetime(df_sox['Date'])
df_sox = df_sox.sort_values('Date').reset_index(drop=True)

if df_sox['SOX_Close'].dtype == 'object':
    df_sox['SOX_Close'] = df_sox['SOX_Close'].astype(str).str.replace(',', '').astype(float)

# ==========================================
# 2. 读取并清洗 NDX 数据 (纳指 100)
# ==========================================
print("正在读取本地 NDX 数据...")
df_ndx = pd.read_csv(ndx_path) # 这里使用刚才拼好的绝对路径变量

df_ndx = df_ndx[['日期', '收盘']].rename(columns={'日期': 'Date', '收盘': 'NDX_Close'})
df_ndx['Date'] = pd.to_datetime(df_ndx['Date'])
df_ndx = df_ndx.sort_values('Date').reset_index(drop=True)

if df_ndx['NDX_Close'].dtype == 'object':
    df_ndx['NDX_Close'] = df_ndx['NDX_Close'].astype(str).str.replace(',', '').astype(float)

# ===== 后面的合并数据和画图代码保持不变 =====


# ==========================================
# 3. 合并数据并进行“归一化”计算
# ==========================================
print("正在对齐两组数据并计算...")
# 按照 'Date' (日期) 将两个表合并。
# 使用 how='inner' 可以确保只保留两个指数同时开盘的交易日数据，自动剔除节假日错位
df_merged = pd.merge(df_sox, df_ndx, on='Date', how='inner')

# 核心计算：归一化（将第一天的价格强行设为 1.0）
df_merged['SOX_Normalized'] = df_merged['SOX_Close'] / df_merged['SOX_Close'].iloc[0]
df_merged['NDX_Normalized'] = df_merged['NDX_Close'] / df_merged['NDX_Close'].iloc[0]


# ==========================================
# 4. 可视化绘图
# ==========================================
print("正在生成对比图表...")
plt.figure(figsize=(14, 7))

# 画线
plt.plot(df_merged['Date'], df_merged['SOX_Normalized'], label='SOX (PHLX Semiconductor)', color='red', alpha=0.8)
plt.plot(df_merged['Date'], df_merged['NDX_Normalized'], label='NDX (Nasdaq 100)', color='blue', alpha=0.8)

# 标注与美化
plt.title('10-Year Performance Comparison: SOX vs NDX (Normalized to 1.0)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Cumulative Return Multiple (1.0 = Starting Price)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# 显示图表
plt.tight_layout()
plt.show()