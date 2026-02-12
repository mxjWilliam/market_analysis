from django.db import models

class TradingCalendar(models.Model):
    date = models.DateField(primary_key=True, verbose_name='交易日')
    open_time = models.TimeField(verbose_name='开盘时间')
    close_time = models.TimeField(verbose_name='收盘时间')
    is_trading_day = models.BooleanField(default=True, verbose_name='是否交易日')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '交易日历'
        verbose_name_plural = '交易日历'
        ordering = ['date']

    def __str__(self):
        return f'{self.date} ({"交易日" if self.is_trading_day else "非交易日"})'
