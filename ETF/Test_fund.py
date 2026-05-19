import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 基础参数配置
# ==========================================
NUM_SIMULATIONS = 10000  # 蒙特卡洛模拟路径数
YEARS_INVEST = 10        # 前10年每月定投
YEARS_HOLD = 20          # 修改为后20年纯持有不动
TOTAL_YEARS = YEARS_INVEST + YEARS_HOLD # 修复：定义总年份
TOTAL_MONTHS = TOTAL_YEARS * 12         # 总计360个月

MONTHLY_INVEST = 2000    # 每月定投本金
ETF_PREMIUM = 0.025      # 场内买入时承受的真实溢价率（2.5%）
OTC_FEE_ANNUAL = 0.0100  # 场外满仓型基金年化费率（1.00%）
ETF_FEE_ANNUAL = 0.0065  # 场内ETF年化费率（0.65%）

# ==========================================
# 2. 美股纳指特性与黑天鹅参数
# ==========================================
ANNUAL_RETURN_NORMAL = 0.18  # 正常年份的预期年化收益率
ANNUAL_VOLATILITY = 0.20     # 年化波动率
CRASH_FREQ_YEARS = 4.5       # 黑天鹅平均发生周期（年）
CRASH_MIN = -0.50            # 黑天鹅极端跌幅下限
CRASH_MAX = -0.40            # 黑天鹅极端跌幅上限

CRASH_PROB_MONTHLY = 1 / (CRASH_FREQ_YEARS * 12)

# ==========================================
# 3. 矩阵化生成 10,000 种独立市场的月度收益率
# ==========================================
np.random.seed(42)  

mu_monthly = (ANNUAL_RETURN_NORMAL - 0.5 * ANNUAL_VOLATILITY**2) / 12
sigma_monthly = ANNUAL_VOLATILITY / np.sqrt(12)

normal_returns = np.exp(np.random.normal(mu_monthly, sigma_monthly, size=(TOTAL_MONTHS, NUM_SIMULATIONS))) - 1
crash_mask = np.random.rand(TOTAL_MONTHS, NUM_SIMULATIONS) < CRASH_PROB_MONTHLY
crash_returns = np.random.uniform(CRASH_MIN, CRASH_MAX, size=(TOTAL_MONTHS, NUM_SIMULATIONS))

market_returns = np.where(crash_mask, crash_returns, normal_returns)

# ==========================================
# 4. 模拟资产演化 (记录每月历史轨迹用于绘图)
# ==========================================
# 初始化历史记录矩阵：记录每个月的金额
otc_history = np.zeros((TOTAL_MONTHS, NUM_SIMULATIONS))
etf_history = np.zeros((TOTAL_MONTHS, NUM_SIMULATIONS))

otc_current = np.zeros(NUM_SIMULATIONS)
etf_current = np.zeros(NUM_SIMULATIONS)

otc_fee_monthly = OTC_FEE_ANNUAL / 12
etf_fee_monthly = ETF_FEE_ANNUAL / 12

for month in range(TOTAL_MONTHS):
    r_m = market_returns[month]
    
    # 现有资产随市场波动，并扣除当月资产管理费
    otc_current = otc_current * (1 + r_m) * (1 - otc_fee_monthly)
    etf_current = etf_current * (1 + r_m) * (1 - etf_fee_monthly)
    
    # 如果在前10年，每月追加定投
    if month < YEARS_INVEST * 12:
        otc_current += MONTHLY_INVEST
        etf_current += MONTHLY_INVEST / (1 + ETF_PREMIUM)
        
    # 记录本月状态
    otc_history[month] = otc_current
    etf_history[month] = etf_current

# ==========================================
# 5. 数据统计与输出
# ==========================================
otc_final = otc_history[-1]
etf_final = etf_history[-1]

total_invested = MONTHLY_INVEST * 12 * YEARS_INVEST
print(f"【定投模拟实验报告】")
print(f"总计观察周期: {TOTAL_YEARS} 年 ({YEARS_INVEST}年定投 + {YEARS_HOLD}年死扛)")
print(f"累计总投入本金: {total_invested:,} 元")
print("=" * 60)

print(f"👉 策略 A：场外高费率基金 (1.00% 费率 / 0% 溢价)")
print(f"   最终资产中位数: {int(np.median(otc_final)):,} 元")
print("-" * 60)

print(f"👉 策略 B：场内低费率 ETF (0.65% 费率 / 顶着 2.5% 高溢价买入)")
print(f"   最终资产中位数: {int(np.median(etf_final)):,} 元")
print("=" * 60)

diff_median = np.median(etf_final) - np.median(otc_final)
win_rate = np.mean(etf_final > otc_final) * 100

print(f"📊 统计学最终结论：")
print(f"1. 场内低费率策略相比场外，最终能帮你【多赚】的中位数为: {int(diff_median):,} 元")
print(f"2. 在 1万 种包含暴跌的平行宇宙中，场内策略最终获胜的概率为: {win_rate:.2f}%")

# ==========================================
# 6. Matplotlib 可视化呈现
# ==========================================
# 解决中文显示问题（优先使用微软雅黑，备用黑体）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 提取中位数轨迹（除以10000以便于纵坐标显示“万元”）
otc_median_path = np.median(otc_history, axis=1) / 10000
etf_median_path = np.median(etf_history, axis=1) / 10000
diff_median_path = etf_median_path - otc_median_path

months_axis = np.arange(1, TOTAL_MONTHS + 1)
years_axis = months_axis / 12

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]})

# 图1：两者的绝对资产规模对比
ax1.plot(years_axis, otc_median_path, label='场外 (1.00%费率 / 无溢价)', color='#1f77b4', linewidth=2)
ax1.plot(years_axis, etf_median_path, label='场内 (0.65%费率 / 2.5%溢价)', color='#d62728', linewidth=2, linestyle='--')
ax1.axvline(x=YEARS_INVEST, color='grey', linestyle=':', label='停止定投点 (第10年)')
ax1.set_title(f'纳指定投 {TOTAL_YEARS} 年资产中位数演化路径 (单位：万元)', fontsize=14)
ax1.set_ylabel('总资产 (万元)', fontsize=12)
ax1.legend(fontsize=12)
ax1.grid(True, alpha=0.3)

# 图2：场内策略的“净胜额”演化（即 场内 - 场外）
ax2.plot(years_axis, diff_median_path, color='purple', linewidth=2, label='场内领先金额')
ax2.axhline(y=0, color='black', linestyle='-')
ax2.axvline(x=YEARS_INVEST, color='grey', linestyle=':')
ax2.fill_between(years_axis, diff_median_path, 0, where=(diff_median_path < 0), color='red', alpha=0.3, label='场内亏损期 (溢价惩罚)')
ax2.fill_between(years_axis, diff_median_path, 0, where=(diff_median_path > 0), color='green', alpha=0.3, label='场内盈利期 (费率优势兑现)')

ax2.set_title('场内策略 VS 场外策略 的【差额】变化 (单位：万元)', fontsize=14)
ax2.set_xlabel('时间 (年)', fontsize=12)
ax2.set_ylabel('差额 (万元)', fontsize=12)
ax2.legend(fontsize=10, loc='upper left')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()