"""
公共工具函数
"""
import logging
from datetime import date, time, timedelta

import akshare as ak
import pandas as pd

logger = logging.getLogger(__name__)

# A 股默认开盘、收盘时间
DEFAULT_OPEN_TIME = time(9, 30)
DEFAULT_CLOSE_TIME = time(15, 0)


def get_latest_trading_date(market='CN'):
    """
    获取指定市场最近交易日（<= 今日），非交易日则返回前一交易日。从 TradingCalendar 表读取。
    :param market: 交易市场，默认 'CN'（A股）
    :return: date
    """
    from .models import TradingCalendar

    today = date.today()
    try:
        obj = (
            TradingCalendar.objects.filter(
                market=market, date__lte=today, is_trading_day=True
            )
            .order_by('-date')
            .first()
        )
        if obj is not None:
            return obj.date
    except Exception as e:
        logger.warning("从 TradingCalendar 获取最近交易日失败，使用当前日期: %s", e)
    return today


def load_trading_calendar_for_year(year: int, market='CN'):
    """
    根据 akshare 读取的 A 股交易日历，将指定年份的日历数据写入 TradingCalendar。
    该年每一天都会有一条记录：在 akshare 返回的交易日中为交易日，否则为非交易日。
    开盘、收盘时间使用 A 股默认 09:30 / 15:00。
    :param year: 年份，如 2026
    :param market: 交易市场，默认 'CN'（A股）。当前 akshare 仅支持 A 股，其他市场需自行维护。
    :return: (新增或更新条数, 其中交易日条数)
    """
    from .models import TradingCalendar

    start = date(year, 1, 1)
    end = date(year, 12, 31)

    try:
        trade_date_df = ak.tool_trade_date_hist_sina()
        if trade_date_df.empty:
            logger.warning("akshare 返回交易日历为空")
            trade_dates_2026 = set()
        else:
            # 统一为 date 类型再筛选（akshare 可能返回 datetime64）
            col = pd.to_datetime(trade_date_df['trade_date']).dt.date
            in_year = (col >= start) & (col <= end)
            trade_dates_2026 = set(col.loc[in_year].tolist())
    except Exception as e:
        logger.exception("从 akshare 获取交易日历失败: %s", e)
        raise

    updated, trading_count = 0, 0
    d = start
    while d <= end:
        is_trading = d in trade_dates_2026
        _, created = TradingCalendar.objects.update_or_create(
            market=market,
            date=d,
            defaults={
                'open_time': DEFAULT_OPEN_TIME,
                'close_time': DEFAULT_CLOSE_TIME,
                'is_trading_day': is_trading,
            },
        )
        updated += 1
        if is_trading:
            trading_count += 1
        d += timedelta(days=1)

    logger.info(
        "交易日历加载完成: 市场=%s, 年份=%s, 总条数=%s, 其中交易日=%s",
        market, year, updated, trading_count,
    )
    return updated, trading_count

