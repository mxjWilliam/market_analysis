from django.db import models

# Create your models here.
class UpDonwNumber(models.Model):
    # 交易日期
    trading_date = models.DateField('交易日期', primary_key=True)
    # 上涨家数
    up_number = models.IntegerField('上涨家数', default=0)
    # 下跌家数
    down_number = models.IntegerField('下跌家数', default=0)
    # 涨停家数
    up_floor_number = models.IntegerField('涨停家数', default=0)
    # 非一字涨停家数
    up_floor_number2 = models.IntegerField('非一字涨停家数', default=0)
    # 跌停家数
    down_floor_number = models.IntegerField('跌停家数', default=0)
    # 炸板家数
    floor_explosion_number = models.IntegerField('炸板家数', default=0)
    # 二连板
    up_twenty_number = models.IntegerField('二连板', default=0)
    # 三连板
    up_thirty_number = models.IntegerField('三连板', default=0)
    # 四连板
    up_fourty_number = models.IntegerField('四连板', default=0)
    # 四连板以上
    up_gt_fourty_number = models.IntegerField('四连板以上', default=0)
    # 更新时间
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '短线情绪数据'
        verbose_name_plural = '短线情绪数据'