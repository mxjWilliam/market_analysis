from django.shortcuts import redirect
from django.urls import reverse


def admin_calendar(request):
    """管理入口：跳转到 SimpleUI 后台的 TradingCalendar 列表（需登录后台）"""
    return redirect(reverse('admin:common_tradingcalendar_changelist'))