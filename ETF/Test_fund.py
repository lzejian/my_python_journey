import akshare as ak
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_average_amplitude(ticker, name):
    # 获取ETF历史日K线数据 (前复权)
    df = ak.fund_etf_hist_em(symbol=ticker, adjust="qfq")
    df['日期'] = pd.to_datetime(df['日期'])
    
    # 计算每日振幅：(最高 - 最低) / 昨收 * 100
    df['昨收'] = df['收盘'].shift(1)
    df['日振幅(%)'] = (df['最高'] - df['最低']) / df['昨收'] * 100
    df = df.dropna()
    
    # 截取不同时间段
    now = datetime.now()
    periods = {
        "3个月": now - relativedelta(months=3),
        "半年": now - relativedelta(months=6),
        "1年": now - relativedelta(years=1)
    }
    
    print(f"--- {name} ({ticker}) 平均日振幅 ---")
    for period_name, start_date in periods.items():
        df_slice = df[df['日期'] >= start_date]
        avg_amp = df_slice['日振幅(%)'].mean()
        print(f"{period_name}: {avg_amp:.2f}%")
    print("\n")

# 运行测算
calculate_average_amplitude("515880", "通信ETF")
calculate_average_amplitude("588380", "双创50")