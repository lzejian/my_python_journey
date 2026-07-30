"""
AWS Lambda - 统一每日监控系统
====================================================================
模块 A：TQQQ LRS (Leverage Rotation Strategy) 杠杆轮动策略监控
模块 B：QDII 基金公告监控（限额/放假/定投通知）

功能：每日触发一次，顺序执行两个独立监控模块，各自通过 Bark 推送。
      即使其中一个模块失败，也不会影响另一个模块的运行。

触发方式：AWS EventBridge 定时规则 (cron)
推荐触发时间：UTC 05:00 (北京时间 13:00)

环境变量：
  - BARK_TOKEN: Bark 推送 Token (必须)
  - FRED_API_KEY: FRED API 密钥 (默认已内置)
  - ALIYUN_APPCODE: 阿里云市场 AppCode (默认已内置)
  - S3_BUCKET: 存储 QDII 历史记录的 S3 桶名 (必须)
  - S3_STATE_KEY: S3 中状态文件的 key (默认: fund_notice_state_v2.json)
"""

import json
import os
import logging
from datetime import datetime, timedelta

import boto3
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests

# ============================================================
# 全局配置
# ============================================================
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Bark 推送
BARK_TOKEN = os.environ.get("BARK_TOKEN", "WWBFmjRYERrAUBDRskK3Gn")
BARK_BASE_URL = f"https://api.day.app/{BARK_TOKEN}/"

# FRED API
FRED_API_KEY = os.environ.get("FRED_API_KEY", "749812e69e99644cfd562b14b57461aa")
FRED_T10Y2Y = "T10Y2Y"
FRED_FED_RATE = "DFEDTARU"

# LRS 技术面参数
SMA_PERIOD = 200
ATR_PERIOD = 14
ATR_MULTIPLIER = 1.5
LOOKBACK_DAYS = 300

# QDII 基金监控配置
QDII_API_URL = "https://lhjjhqsjcx.market.alicloudapi.com/fund/notice"
ALIYUN_APPCODE = os.environ.get("ALIYUN_APPCODE", "cad000d1ad8a4b35a17a5825a9b3d4ab")
S3_BUCKET = os.environ.get("S3_BUCKET", "")
S3_STATE_KEY = os.environ.get("S3_STATE_KEY", "fund_notice_state_v2.json")
CUTOFF_DATE = "2026-05-19 00:00:00"

QDII_FUNDS = {
    "002891": "华夏移动互联混合",
    "006373": "国富全球科技互联混合",
    "539002": "建信新兴市场混合",
    "012920": "易方达全球成长精选混合",
    "501225": "景顺长城全球半导体芯片股票A",
    "006555": "浦银安盛全球智能科技(QDII)A",
    "160213": "国泰纳斯达克100指数",
}

s3_client = boto3.client("s3")


# ============================================================
# 公共工具函数
# ============================================================
def send_bark(title: str, body: str, group: str = "量化监控") -> bool:
    """通过 Bark API 推送消息到手机"""
    try:
        payload = {"title": title, "body": body, "group": group}
        resp = requests.post(BARK_BASE_URL, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info(f"Bark 推送成功: [{group}] {title}")
        return True
    except Exception as e:
        logger.error(f"Bark 推送失败: {e}")
        return False


# ============================================================
# 模块 A：TQQQ LRS 策略监控
# ============================================================
def get_fred_series_latest(series_id: str) -> float | None:
    """从 FRED API 获取指定序列的最新数值"""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 10,
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    observations = resp.json().get("observations", [])
    for obs in observations:
        value = obs.get("value", ".")
        if value != ".":
            return float(value)
    return None


def is_market_closed(latest_date: pd.Timestamp) -> bool:
    """判断今天是否为美股休市日"""
    today = pd.Timestamp.now(tz="America/New_York").normalize()
    diff = (today - latest_date).days
    weekday = today.weekday()
    if weekday == 0:
        return diff > 3
    elif weekday in (5, 6):
        return True
    else:
        return diff > 1


def run_lrs_strategy() -> str:
    """执行 LRS 策略分析，返回完整报告文本"""
    logger.info("[LRS] 正在获取 QQQ 数据...")
    ticker = yf.Ticker("QQQ")
    df = ticker.history(period=f"{LOOKBACK_DAYS}d")

    if df.empty or len(df) < SMA_PERIOD:
        raise ValueError(f"QQQ 数据不足: 仅获取 {len(df)} 条，需要至少 {SMA_PERIOD} 条")

    latest_date = df.index[-1]
    if isinstance(latest_date, pd.Timestamp) and latest_date.tzinfo:
        latest_date = latest_date.tz_localize(None)

    if is_market_closed(pd.Timestamp(latest_date, tz="America/New_York")):
        return "MARKET_CLOSED"

    close = df["Close"].iloc[-1]
    sma200 = df["Close"].rolling(window=SMA_PERIOD).mean().iloc[-1]
    atr_series = ta.atr(df["High"], df["Low"], df["Close"], length=ATR_PERIOD)
    atr14 = atr_series.iloc[-1]
    trigger = sma200 - (ATR_MULTIPLIER * atr14)

    if close > sma200:
        trend_status = "🟢 正常上升趋势"
        trend_level = "GREEN"
    elif close >= trigger:
        trend_status = "🟡 进入震荡缓冲带，暂不操作，观察是否发生有效跌破"
        trend_level = "YELLOW"
    else:
        trend_status = "🔴 有效跌破动态防守线，触发卖出信号！"
        trend_level = "RED"

    logger.info("[LRS] 正在获取 FRED 宏观数据...")
    yield_spread = get_fred_series_latest(FRED_T10Y2Y)
    fed_rate = get_fred_series_latest(FRED_FED_RATE)

    spread_warning = ""
    if yield_spread is not None and yield_spread < 0:
        spread_warning = " ⚠️ 收益率曲线倒挂！"

    rate_comment = ""
    if fed_rate is not None:
        if fed_rate >= 5.0:
            rate_comment = "（高利率紧缩周期）"
        elif fed_rate >= 3.0:
            rate_comment = "（中性偏紧周期）"
        elif fed_rate >= 1.0:
            rate_comment = "（温和宽松周期）"
        else:
            rate_comment = "（极度宽松/零利率周期）"

    if trend_level == "RED":
        conclusion = "⚡ 立刻将 TQQQ 轮动至 SGOV（短期美债 ETF）进行避险！跌破动态防守线，风险极高。"
    elif trend_level == "YELLOW" and yield_spread is not None and yield_spread < -0.5:
        conclusion = "⚠️ 技术面进入缓冲带且利差严重倒挂，建议减仓 TQQQ 50%，密切关注后续走势。"
    else:
        conclusion = "✅ 继续全仓持有 TQQQ，趋势完好，无需操作。"

    report_date = latest_date.strftime("%Y-%m-%d")
    spread_str = f"{yield_spread:.2f}%" if yield_spread is not None else "数据暂不可用"
    rate_str = f"{fed_rate:.2f}%" if fed_rate is not None else "数据暂不可用"
    safety_margin = ((close - trigger) / close) * 100

    report = f"""📊【LRS 策略复盘报告】日期：{report_date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

一、技术面与动态防守线计算
• QQQ 最新收盘价：${close:.2f}
• 200日均线 (SMA200)：${sma200:.2f}
• 14日 ATR：${atr14:.2f}
• 动态防守触发价：${trigger:.2f}
• 距防守线安全距离：{safety_margin:.1f}%
• 当前趋势状态：{trend_status}

二、宏观面监控
• 10Y-2Y 美债利差：{spread_str}{spread_warning}
• 联邦基金利率上限：{rate_str} {rate_comment}

三、今日操作结论
💡 {conclusion}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 LRS Monitor v2.0 | Powered by yfinance + FRED"""

    return report


# ============================================================
# 模块 B：QDII 基金公告监控
# ============================================================
def load_qdii_history() -> list | None:
    """从 S3 读取 QDII 公告推送历史"""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_STATE_KEY)
        return json.loads(response["Body"].read().decode("utf-8"))
    except s3_client.exceptions.NoSuchKey:
        return []
    except Exception as e:
        logger.error(f"[QDII] S3 读取历史记录失败: {e}")
        send_bark("⚠️ QDII 系统异常", f"S3 读取失败，为防止消息轰炸已切断本次监控。\n错误: {e}", "基金监控")
        return None


def save_qdii_history(history: list):
    """将 QDII 公告历史保存到 S3"""
    try:
        if len(history) > 500:
            history = history[-500:]
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=S3_STATE_KEY,
            Body=json.dumps(history, ensure_ascii=False, indent=2).encode("utf-8"),
            ContentType="application/json",
        )
    except Exception as e:
        logger.error(f"[QDII] S3 保存历史记录失败: {e}")


def run_qdii_monitor():
    """执行 QDII 基金公告监控"""
    logger.info("[QDII] 开始扫描基金公告...")

    history = load_qdii_history()
    if history is None:
        return "S3 读取故障，QDII 模块终止"

    headers = {
        "Authorization": f"APPCODE {ALIYUN_APPCODE}",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    new_notices_found = []

    for fund_code, fund_name in QDII_FUNDS.items():
        logger.info(f"[QDII] 正在查询: {fund_name} ({fund_code})")
        payload = {"fundCode": fund_code, "pageNo": "1", "pageSize": "10"}

        try:
            response = requests.post(QDII_API_URL, headers=headers, data=payload, timeout=10)
            if response.status_code != 200:
                logger.error(f"[QDII] 接口 HTTP 错误，状态码: {response.status_code}")
                continue

            try:
                result = response.json()
            except ValueError:
                logger.error(f"[QDII] 数据解析失败，接口返回非法内容")
                continue

            notices = result.get("data", {}).get("list", [])
            if not notices:
                continue

            for notice in notices:
                title = notice.get("title")
                date_str = notice.get("date")

                if not title or not date_str:
                    continue

                title = str(title)
                date_str = str(date_str)

                if date_str < CUTOFF_DATE:
                    continue
                if "提示性公告" in title:
                    continue

                unique_id = f"{fund_code}_{date_str}_{title}"
                if unique_id in history:
                    continue

                is_trigger = False
                emoji = "📢"

                if "定期定额" in title:
                    is_trigger = True
                    emoji = "💴"
                elif "季度报告" in title or "年度报告" in title:
                    is_trigger = True
                    emoji = "📄"
                elif fund_code == "160213" and ("非交易日" in title or "节假日" in title):
                    is_trigger = True
                    emoji = "☀️"

                if is_trigger:
                    new_notices_found.append({
                        "fund_name": fund_name,
                        "title": title,
                        "date": date_str,
                        "emoji": emoji,
                        "unique_id": unique_id,
                    })

        except Exception as e:
            logger.error(f"[QDII] 查询 {fund_code} 时发生错误: {e}")

    if new_notices_found:
        success_count = 0
        for notice in new_notices_found:
            msg_title = f"{notice['emoji']} {notice['fund_name']}"
            msg_body = f"{notice['title']}\n发布日期：{notice['date']}"
            if send_bark(msg_title, msg_body, "基金监控"):
                history.append(notice["unique_id"])
                success_count += 1
        save_qdii_history(history)
        logger.info(f"[QDII] 发现 {len(new_notices_found)} 条公告，成功推送 {success_count} 条")
    else:
        logger.info("[QDII] 平安无事，没有发现符合条件的公告")

    return f"QDII 监控完毕，推送 {len(new_notices_found)} 条"


# ============================================================
# Lambda 入口函数
# ============================================================
def lambda_handler(event, context):
    """
    AWS Lambda 标准入口
    顺序执行两个监控模块，各自独立，互不影响。
    """
    logger.info("====== 统一监控系统启动 ======")
    results = {}

    # ---- 模块 A：LRS TQQQ 策略 ----
    try:
        report = run_lrs_strategy()
        if report == "MARKET_CLOSED":
            send_bark("📊 LRS 策略监控", "今日为美股休息日，暂停报告生成。", "量化监控")
            results["lrs"] = "market_closed"
        else:
            send_bark("📊 LRS 策略复盘报告", report, "量化监控")
            results["lrs"] = "success"
    except Exception as e:
        error_msg = f"⚠️ LRS 监控异常\n\n错误类型: {type(e).__name__}\n错误详情: {str(e)}"
        logger.error(f"[LRS] 运行异常: {e}", exc_info=True)
        send_bark("⚠️ LRS 监控异常", error_msg, "量化监控")
        results["lrs"] = f"error: {e}"

    # ---- 模块 B：QDII 基金公告 ----
    try:
        qdii_result = run_qdii_monitor()
        results["qdii"] = qdii_result
    except Exception as e:
        error_msg = f"⚠️ QDII 监控异常\n\n错误类型: {type(e).__name__}\n错误详情: {str(e)}"
        logger.error(f"[QDII] 运行异常: {e}", exc_info=True)
        send_bark("⚠️ QDII 监控异常", error_msg, "基金监控")
        results["qdii"] = f"error: {e}"

    logger.info(f"====== 监控完毕: {results} ======")
    return {
        "statusCode": 200,
        "body": json.dumps(results, ensure_ascii=False)
    }