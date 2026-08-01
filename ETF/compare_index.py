import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import time

# 你的阿里云 API AppCode
APPCODE = "cad000d1ad8a4b35a17a5825a9b3d4ab"

def fetch_fund_data(symbol):
    """
    获取国内基金/ETF数据 (使用 fund/history POST 接口)
    支持场内和场外，解决公募基金净值获取问题
    """
    url = "https://lhjjhqsjcx.market.alicloudapi.com/fund/history" 
    headers = {
        "Authorization": f"APPCODE {APPCODE}"
    }
    
    print(f"正在获取国内基金/ETF [{symbol}] 的数据...")
    payload = {
        "fundCode": symbol,
        "period": "5" # period=5 代表获取近三年数据，足以覆盖2024-06-18至今
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        
        k_lines = data.get("data", {}).get("list", [])
        if not k_lines:
            print(f"[{symbol}] 未获取到数据。")
            return None
            
        df_temp = pd.DataFrame(k_lines)
        
        # 适应真实返回结构: 字段名为 'date' 和 'netValue'
        if 'date' in df_temp.columns and 'netValue' in df_temp.columns:
            df_temp = df_temp.rename(columns={'netValue': 'close'})
            df_temp['date'] = pd.to_datetime(df_temp['date']).dt.date
            df_temp['close'] = pd.to_numeric(df_temp['close'])
            df_temp = df_temp[['date', 'close']].drop_duplicates(subset=['date'])
            df_temp.set_index('date', inplace=True)
            df_temp.sort_index(inplace=True)
            return df_temp[['close']]
        else:
            print(f"[{symbol}] 数据解析失败，找不到 date 和 netValue 字段。")
            return None
    except Exception as e:
        print(f"获取 {symbol} 数据失败: {e}")
        return None

def fetch_global_data(symbol, start_date_str):
    """
    获取全球指数数据 (使用 comkm2 接口，加入分段请求逻辑突破500条限制)
    """
    url = "https://alirmcom2.market.alicloudapi.com/query/comkm2"
    headers = {
        "Authorization": f"APPCODE {APPCODE}"
    }
    
    print(f"正在获取海外标的 [{symbol}] 的数据 (含分段拉取逻辑)...")
    
    start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_dt = datetime.now()
    
    all_k_lines = []
    current_start = start_dt
    
    try:
        while current_start < end_dt:
            # 每次最多跨度约 400 天，确保不超过500天的API限制
            current_end = min(current_start + timedelta(days=400), end_dt)
            
            datest = current_start.strftime("%Y-%m-%d %H:%M:%S")
            dateed = current_end.strftime("%Y-%m-%d %H:%M:%S")
            
            params = {
                "symbol": symbol,
                "period": "D",
                "datest": datest,
                "dateed": dateed,
                "withlast": 1
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            chunk_data = data.get("Obj", [])
            if chunk_data:
                all_k_lines.extend(chunk_data)
                
            # 下一次循环的时间起点
            current_start = current_end + timedelta(days=1)
            time.sleep(0.5) # 稍微休眠，防止请求过快被限流
            
        if not all_k_lines:
            print(f"[{symbol}] 未获取到任何数据。")
            return None
            
        df_temp = pd.DataFrame(all_k_lines)
        if 'D' in df_temp.columns and 'C' in df_temp.columns:
            # D字段格式是 "2018-01-02 00:00:00"，截取日期部分
            df_temp['date'] = df_temp['D'].apply(lambda x: datetime.strptime(str(x).split()[0], "%Y-%m-%d").date())
            df_temp['close'] = pd.to_numeric(df_temp['C'])
            df_temp = df_temp[['date', 'close']].drop_duplicates(subset=['date'])
            df_temp.set_index('date', inplace=True)
            df_temp.sort_index(inplace=True)
            return df_temp[['close']]
        else:
            print(f"[{symbol}] 数据解析失败。")
            return None
    except Exception as e:
        print(f"获取 {symbol} 失败: {e}")
        return None

def analyze_portfolio(start_date_str):
    """
    核心分析函数：获取多标的数据、对齐时间轴、计算收益和直观的相关性
    """
    portfolio = {
        '539002': {'type': 'fund', 'name': '建信新兴(539002)'},
        '513310': {'type': 'fund', 'name': '中韩半导体(513310)'},
        '006373': {'type': 'fund', 'name': '国富科技(006373)'},
        '002891': {'type': 'fund', 'name': '华夏互联(002891)'},
        '006555': {'type': 'fund', 'name': '浦银智能(006555)'},
        '501225': {'type': 'fund', 'name': '景顺芯片(501225)'},
        '016664': {'type': 'fund', 'name': '天弘制造(016664)'},
        '017730': {'type': 'fund', 'name': '嘉实升级(017730)'},
        'NASDAQSOXX': {'type': 'global', 'name': '费城半导体(SOXX)'}
    }
    
    dfs = {}
    target_start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    
    # 1. 批量获取并截取数据
    print(f"\n--- 开始获取自 {start_date_str} 以来的数据 ---")
    for symbol, info in portfolio.items():
        if info['type'] == 'fund':
            df = fetch_fund_data(symbol)
        else:
            df = fetch_global_data(symbol, start_date_str)
            
        if df is not None and not df.empty:
            df = df[df.index >= target_start_date]
            if not df.empty:
                df.columns = [info['name']]
                dfs[symbol] = df

    if not dfs:
        print("所有数据获取失败！")
        return
        
    print("\n正在对齐多市场数据 (处理中美韩节假日休市差异)...")
    df_merged = pd.DataFrame()
    for symbol, df in dfs.items():
        if df_merged.empty:
            df_merged = df
        else:
            df_merged = pd.merge(df_merged, df, left_index=True, right_index=True, how='outer')
            
    # 【核心逻辑】前向填充：如果某天A国休市但B国开市，A国净值沿用前一天
    df_merged.fillna(method='ffill', inplace=True)
    # 为防止最初几天出现NaN，做一次后向填充兜底
    df_merged.fillna(method='bfill', inplace=True) 
    df_merged.dropna(inplace=True)

    # 3. 计算区间收益率
    print("\n" + "="*55)
    print(f"自 {start_date_str} 至今 区间累计收益率")
    print("="*55)
    returns = {}
    for col in df_merged.columns:
        ret = (df_merged[col].iloc[-1] / df_merged[col].iloc[0]) - 1
        returns[col] = ret
        print(f"【{col}】 区间收益率: {ret*100:>6.2f}%")
        
    # 4. 计算相关性并直观输出排行榜 (丢掉复杂的矩阵)
    correlation_matrix = df_merged.corr()
    soxx_col = '费城半导体(SOXX)'
    
    if soxx_col in correlation_matrix.columns:
        # 只取出各基金跟 SOXX 的相关性，去掉 SOXX 自己的 1.0，并从高到低排序
        soxx_corr = correlation_matrix[soxx_col].drop(soxx_col).sort_values(ascending=False)
        
        print("\n" + "="*55)
        print("🏆 【相关性排行榜】哪只基金最像美股半导体(SOXX)？")
        print("="*55)
        for fund, corr in soxx_corr.items():
            if corr >= 0.95:
                desc = "⭐⭐⭐⭐⭐ 极度相似 (完美平替)"
            elif corr >= 0.85:
                desc = "⭐⭐⭐⭐ 高度相似 (跟涨跟跌强)"
            elif corr >= 0.70:
                desc = "⭐⭐⭐ 中度相关 (有部分独立行情)"
            else:
                desc = "⭐ 弱相关 (走势差异很大)"
            print(f"{fund} | 相关系数: {corr:.4f} 👉 {desc}")
        print("="*55)
    
    # 5. 绘制可视化图表 (左侧走势主图 + 右侧相关性横向柱状图)
    df_normalized = df_merged.copy()
    for col in df_normalized.columns:
        df_normalized[col] = df_normalized[col] / df_normalized[col].iloc[0]
        
    fig = plt.figure(figsize=(18, 9))
    # 使用 GridSpec 将画面分为左右两部分 (宽度比例 3:1)
    gs = fig.add_gridspec(1, 2, width_ratios=[3, 1])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    
    # --- 画左图：净值走势 ---
    for col in df_normalized.columns:
        # 给 SOXX 加粗高亮显示作为“定海神针”基准线
        is_base = (col == soxx_col)
        ax1.plot(df_normalized.index, df_normalized[col], 
                 label=f'{col} ({returns[col]*100:.1f}%)', 
                 linewidth=4.0 if is_base else 1.5,
                 alpha=1.0 if is_base else 0.7)
                 
    ax1.set_title(f'全球半导体/科技核心基金走势对比 (起点: {start_date_str})', fontsize=14, fontweight='bold')
    ax1.set_ylabel('累计净值 (以 1.0 为起点)', fontsize=12)
    ax1.legend(fontsize=10, loc='upper left', frameon=True, shadow=True)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # --- 画右图：相关性排行榜柱状图 ---
    if soxx_col in correlation_matrix.columns:
        # 为了让最像的排在柱状图最上面，数据需要倒序
        soxx_corr_reversed = soxx_corr[::-1]
        
        # 颜色区分：高度相关用蓝色，否则用红色
        colors = ['#ff9999' if c < 0.85 else '#66b3ff' for c in soxx_corr_reversed.values]
        bars = ax2.barh(soxx_corr_reversed.index, soxx_corr_reversed.values, color=colors)
        
        ax2.set_title('各标的与 SOXX 的相似度', fontsize=14, fontweight='bold')
        ax2.set_xlabel('皮尔逊相关系数', fontsize=12)
        ax2.set_xlim(0, 1.05) # 相关系数最大是1
        
        # 在柱子顶端打上具体数字
        for i, bar in enumerate(bars):
            val = bar.get_width()
            ax2.text(val + 0.01, i, f"{val:.3f}", va='center', fontsize=11, fontweight='bold')
    
    # 处理系统字体问题以正常显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS'] 
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("环境准备完毕！开始执行智能分段拉取请求...")
    # 从 2024年6月18日开始计算
    analyze_portfolio("2024-06-18")