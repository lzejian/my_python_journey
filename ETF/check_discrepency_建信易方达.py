import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ================= 配置区域 =================
FUND_CODE = "539002"       # 建信新兴市场混合
BENCHMARK_TICKER = ".SOX"  # 费城半导体指数 (新浪财经代码通常为 .SOX)
START_DATE = "2024-06-01"  # 起始时间
ROLLING_WINDOW = 20        # 滚动窗口
# ===========================================

print(f"正在获取数据... 基金代码: {FUND_CODE}, 基准: {BENCHMARK_TICKER}")

# 1. 获取基金净值 (使用akshare - 天天基金接口)
try:
    fund_df = ak.fund_open_fund_info_em(symbol=FUND_CODE, indicator="单位净值走势")
    
    # 数据清洗
    fund_df = fund_df[['净值日期', '单位净值']].rename(columns={'净值日期': 'Date', '单位净值': 'Fund_NAV'})
    fund_df['Date'] = pd.to_datetime(fund_df['Date'])
    fund_df['Fund_NAV'] = fund_df['Fund_NAV'].astype(float)
    fund_df.set_index('Date', inplace=True)
    
    # 计算日涨跌幅
    fund_df['Fund_Pct'] = fund_df['Fund_NAV'].pct_change()
    
    # 过滤掉非交易日（空值）
    fund_df.dropna(inplace=True)

except Exception as e:
    print(f"获取基金数据失败: {e}")
    print("提示：请检查 akshare 是否为最新版本 (pip install --upgrade akshare)")
    exit()

# 2. 获取基准数据 (只使用新浪财经)
try:
    print(f"正在尝试从新浪财经抓取 {BENCHMARK_TICKER} 数据...")
    
    # 新浪接口返回全部历史，无需指定开始日期，我们后面自己过滤
    # adjust="" 表示不复权，指数通常不需要复权
    benchmark = ak.stock_us_daily(symbol=BENCHMARK_TICKER, adjust="")
    
    if benchmark is None or benchmark.empty:
        raise ValueError(f"新浪财经接口未返回 {BENCHMARK_TICKER} 的数据。")
        
    print(f"成功获取基准数据 (来源: 新浪财经)")

    # 新浪列名处理: 通常是 ['date', 'close', ...] 或中文
    col_map = {'date': 'Date', 'close': 'Close', '日期': 'Date', '收盘': 'Close'}
    benchmark = benchmark.rename(columns=col_map)
    
    # 确保只取我们要的列
    if 'Date' in benchmark.columns and 'Close' in benchmark.columns:
        benchmark = benchmark[['Date', 'Close']]
    else:
        raise ValueError(f"数据列名不匹配: {benchmark.columns}")

    # 通用数据清洗
    benchmark['Date'] = pd.to_datetime(benchmark['Date'])
    benchmark.set_index('Date', inplace=True)
    
    # 按用户设定的开始时间过滤
    benchmark = benchmark[benchmark.index >= pd.to_datetime(START_DATE)]

    # 计算日涨跌幅
    benchmark_df = pd.DataFrame()
    benchmark_df['Bench_Pct'] = benchmark['Close'].astype(float).pct_change()

except Exception as e:
    print(f"获取指数数据失败: {e}")
    exit()

# 3. 合并数据 (取交集，确保只计算两边都有数据的日期)
# 基金净值日期对应的是当晚美股收盘，所以直接按日期对齐即可
merged_df = pd.merge(fund_df[['Fund_Pct']], benchmark_df[['Bench_Pct']], left_index=True, right_index=True, how='inner')

if len(merged_df) < ROLLING_WINDOW:
    print(f"错误：有效重叠数据不足 {ROLLING_WINDOW} 天，无法计算相关性。")
    print(f"基金数据截止: {fund_df.index[-1]}, 基准数据截止: {benchmark_df.index[-1]}")
    exit()

# 4. 计算滚动相关性
merged_df['Correlation'] = merged_df['Fund_Pct'].rolling(window=ROLLING_WINDOW).corr(merged_df['Bench_Pct'])

# 5. 分析与报警
# 去除因为 rolling 产生的 NaN
valid_corr = merged_df['Correlation'].dropna()

if valid_corr.empty:
    print("数据不足以计算滚动相关性。")
    exit()

latest_corr = valid_corr.iloc[-1]
latest_date = valid_corr.index[-1].strftime('%Y-%m-%d')

print("-" * 30)
print(f"分析报告日期: {latest_date}")
print(f"最近 {ROLLING_WINDOW} 个交易日与 {BENCHMARK_TICKER} 的相关系数: {latest_corr:.4f}")

if latest_corr > 0.8:
    print("✅ 状态：高度拟合。基金依然在紧密跟踪半导体指数。")
elif latest_corr > 0.6:
    print("⚠️ 状态：中度拟合。可能受到非美股（韩国/台湾）仓位影响，或有轻微调仓。")
else:
    print("❌ 警告：风格漂移！相关性过低，可能已换仓或受监管影响。")
print("-" * 30)

# 6. 绘图
plt.figure(figsize=(12, 6))
plt.plot(merged_df.index, merged_df['Correlation'], label='Rolling Correlation', color='blue')
plt.axhline(y=0.7, color='red', linestyle='--', label='High Correlation (0.7)')
plt.axhline(y=0.0, color='gray', linestyle=':', alpha=0.5)
plt.title(f'Fund {FUND_CODE} vs {BENCHMARK_TICKER} (Rolling {ROLLING_WINDOW} Days)')
plt.legend()
plt.grid(True)
plt.show()