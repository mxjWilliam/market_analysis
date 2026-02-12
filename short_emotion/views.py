import logging
import pandas as pd
import akshare as ak
from django.shortcuts import HttpResponse, redirect
from django.db import IntegrityError
from django.http import JsonResponse
from datetime import date, timedelta

from common.utils import get_latest_trading_date

from .models import UpDonwNumber

logger = logging.getLogger(__name__)


# Create your views here.

def _get_spot_data():
    """获取A股行情数据（东方财富接口）"""
    try:
        return ak.stock_zh_a_spot_em()
    except Exception as e:
        logger.error(f"获取A股行情数据失败: {e}")
        return pd.DataFrame()


def _get_trading_date_str(dt):
    """将日期转为 YYYYMMDD 格式字符串"""
    return dt.strftime("%Y%m%d")


# 插入短线情绪数据
def add_short_emotion_data(request):
    # 获取最近的A股交易日
    today = get_latest_trading_date()
    date_str = _get_trading_date_str(today)
    try:
        # 初始化数据
        up_number = 0
        down_number = 0
        up_floor_number = 0
        down_floor_number = 0
        non_one_word_limit_up = 0
        floor_explosion_number = 0
        two_consecutive = 0
        three_consecutive = 0
        four_consecutive = 0
        gt_four_consecutive = 0
        
        # 获取A股市场数据（上涨/下跌家数）
        stock_zh_a_spot_df = _get_spot_data()
        if not stock_zh_a_spot_df.empty and '涨跌幅' in stock_zh_a_spot_df.columns:
            up_number = len(stock_zh_a_spot_df[stock_zh_a_spot_df['涨跌幅'] > 0])
            down_number = len(stock_zh_a_spot_df[stock_zh_a_spot_df['涨跌幅'] < 0])
        
        # 获取涨停数据
        try:
            stock_zt_pool_df = ak.stock_zt_pool_em(date=date_str)
            if not stock_zt_pool_df.empty:
                up_floor_number = len(stock_zt_pool_df)
                # 非一字涨停：不满足“最高价=最低价=涨停价”的涨停股。一字板=全天封死，最高与最低都等于涨停价
                # 优先用行情表的最高、最低 + 涨停池的最新价(作涨停价) 合并计算；无则用首次封板时间≠09:25 近似
                if (
                    not stock_zh_a_spot_df.empty
                    and '代码' in stock_zh_a_spot_df.columns
                    and '最高' in stock_zh_a_spot_df.columns
                    and '最低' in stock_zh_a_spot_df.columns
                    and '代码' in stock_zt_pool_df.columns
                    and '最新价' in stock_zt_pool_df.columns
                ):
                    pool = stock_zt_pool_df[['代码', '最新价']].copy()
                    pool.columns = ['代码', '涨停价']
                    pool['代码'] = pool['代码'].astype(str).str.zfill(6)
                    spot = stock_zh_a_spot_df[['代码', '最高', '最低']].copy()
                    spot['代码'] = spot['代码'].astype(str).str.replace(r'\.\w+$', '', regex=True).str.zfill(6)
                    merged = pool.merge(spot, on='代码', how='left')
                    high = pd.to_numeric(merged['最高'], errors='coerce')
                    low = pd.to_numeric(merged['最低'], errors='coerce')
                    limit = pd.to_numeric(merged['涨停价'], errors='coerce')
                    # 仅在有最高、最低且都接近涨停价时计为一字板
                    one_word = ((high >= limit * 0.999) & (low >= limit * 0.999) & high.notna() & low.notna()).sum()
                    non_one_word_limit_up = int(up_floor_number - one_word)
                elif '首次封板时间' in stock_zt_pool_df.columns:
                    first_seal = stock_zt_pool_df['首次封板时间'].astype(str).str.zfill(6)
                    non_one_word_limit_up = int((first_seal != '092500').sum())
                # 计算连板个数
                if '连板数' in stock_zt_pool_df.columns:
                    two_consecutive = len(stock_zt_pool_df[stock_zt_pool_df['连板数'] == 2])
                    three_consecutive = len(stock_zt_pool_df[stock_zt_pool_df['连板数'] == 3])
                    four_consecutive = len(stock_zt_pool_df[stock_zt_pool_df['连板数'] == 4])
                    gt_four_consecutive = len(stock_zt_pool_df[stock_zt_pool_df['连板数'] > 4]) # 四连板以上
        except Exception as e:
            logger.error(f"获取涨停数据失败: {str(e)}")
        
        # 获取跌停数据（从行情数据中筛选涨跌幅<=-9.9%的）
        if not stock_zh_a_spot_df.empty and '涨跌幅' in stock_zh_a_spot_df.columns:
            down_floor_number = len(stock_zh_a_spot_df[stock_zh_a_spot_df['涨跌幅'] <= -9.9])
        
        # 获取炸板家数（使用 stock_zt_pool_zbgc_em 炸板股池）
        try:
            stock_zbgc_df = ak.stock_zt_pool_zbgc_em(date=date_str)
            if not stock_zbgc_df.empty:
                floor_explosion_number = len(stock_zbgc_df)
        except Exception as e:
            logger.warning(f"获取炸板数据失败: {e}")
        
        # 更新或创建数据
        UpDonwNumber.objects.update_or_create(
            trading_date=today,
            defaults={
                'up_number': up_number,
                'down_number': down_number,
                'up_floor_number': up_floor_number,
                'down_floor_number': down_floor_number,
                'up_floor_number2': non_one_word_limit_up,
                'floor_explosion_number': floor_explosion_number,
                'up_twenty_number': two_consecutive,
                'up_thirty_number': three_consecutive,
                'up_fourty_number': four_consecutive,
                'up_gt_fourty_number': gt_four_consecutive,
            }
        )
        
    except IntegrityError:
        pass
    except Exception as e:
        logger.error(f"插入数据失败: {str(e)}")

    return HttpResponse(f"{today}短线情绪数据插入成功！")

# 返回短线情绪所有数据
def query_all(request):
    updonw_number = UpDonwNumber.objects.all()
    # books = UpDonwNumber.objects.filter(trading_date__gte=date.today()-timedelta(days=30))
    for num in updonw_number:
        print(num.trading_date, num.up_number, num.down_number)

    return HttpResponse("查找成功！")

# 查询总连板数
def total_floor_data(request):
    updonw_number = UpDonwNumber.objects.all()
    # 计算当前日期
    today = date.today()
    # 计算30天前的日期
    thirty_days_ago = today - timedelta(days=30)
    # 查询 trading_date 在近30天内的数据
    recent_data = UpDonwNumber.objects.filter(trading_date__gte=thirty_days_ago, trading_date__lte=today)
    xAxis = []
    up_floor_data = {'name': '连板总数', 'type': 'line', 'data': []}
    twenty_up_floor_data = {'name': '连板', 'type': 'line', 'data': []}
    thirty_up_floor_data = {'name': '2连板', 'type': 'line', 'data': []}
    fourty_up_floor_data = {'name': '3连板', 'type': 'line', 'data': []}
    up_gt_fourty_floor_data = {'name': '4连板及以上', 'type': 'line', 'data': []}
    for record in recent_data:
        xAxis.append(record.trading_date)
        total_floor_number = (record.up_twenty_number + record.up_thirty_number +
                              record.up_fourty_number + record.up_gt_fourty_number)
        up_floor_data['data'].append(total_floor_number)
        twenty_up_floor_data['data'].append(record.up_twenty_number)
        thirty_up_floor_data['data'].append(record.up_thirty_number)
        fourty_up_floor_data['data'].append(record.up_fourty_number)
        up_gt_fourty_floor_data['data'].append(record.up_gt_fourty_number)
    data = {
        'xAxis': xAxis,
        'series': [up_floor_data,
                   twenty_up_floor_data,
                   thirty_up_floor_data,
                   fourty_up_floor_data,
                   up_gt_fourty_floor_data
                   ]
    }
    return JsonResponse(data)

# 查询上涨家数和下跌家数
def up_down_data(request):
    # 计算当前日期
    today = date.today()
    # 计算30天前的日期
    thirty_days_ago = today - timedelta(days=30)
    # 查询 trading_date 在近30天内的数据
    recent_data = UpDonwNumber.objects.filter(trading_date__gte=thirty_days_ago, trading_date__lte=today)
    xAxis = []
    up_data = {'name': '上涨家数', 'type': 'line', 'data': []}
    down_data = {'name': '下跌家数', 'type': 'line', 'data': []}
    for record in recent_data:
        xAxis.append(record.trading_date)
        up_data['data'].append(record.up_number)
        down_data['data'].append(record.down_number)
    data = {
        'xAxis': xAxis,
        'series': [up_data, down_data]
    }
    return JsonResponse(data)

# 查询涨停家数、非一字涨停家数、炸板家数和跌停家数
def up_down_floor_data(request):
    # 计算当前日期
    today = date.today()
    # 计算30天前的日期
    thirty_days_ago = today - timedelta(days=30)
    # 查询 trading_date 在近30天内的数据
    recent_data = UpDonwNumber.objects.filter(trading_date__gte=thirty_days_ago, trading_date__lte=today)
    xAxis = []
    up_data = {'name': '涨停家数', 'type': 'line', 'data': []}
    up_twice_data = {'name': '非一字涨停家数', 'type': 'line', 'data': []}
    down_data = {'name': '跌停家数', 'type': 'line', 'data': []}
    explosion_floor_data = {'name': '炸板家数', 'type': 'line', 'data': []}

    for record in recent_data:
        xAxis.append(record.trading_date)
        up_data['data'].append(record.up_floor_number)
        up_twice_data['data'].append(record.up_floor_number2)
        down_data['data'].append(record.down_floor_number)
        explosion_floor_data['data'].append(record.floor_explosion_number)
    data = {
        'xAxis': xAxis,
        'series': [up_data, up_twice_data, explosion_floor_data, down_data]
    }
    return JsonResponse(data)


def admin_updown_number(request):
    """管理入口：跳转到 SimpleUI 后台的 UpDonwNumber 列表（需登录后台）"""
    from django.urls import reverse
    return redirect(reverse('admin:short_emotion_updonwnumber_changelist'))
