from django.db import models

# Create your models here.


#创建接收到的数据表，并且限制输入数据的长度
import os

from django.db import models

# Create your models here.
from django.db import models

from dwing.settings import BASE_DIR
from user.models import The_user


class The_antique(models.Model):
    """悬赏类别
    """
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name="发布悬赏时间")
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name="更新悬赏时间")
    name = models.CharField(max_length=10,
                            verbose_name='类别名称')

    class Meta:
        db_table = 'DDSC_GOODS_CATALOG'
        verbose_name = '悬赏类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Reward(models.Model):
    """
    悬赏
    """
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name="更新时间")
    name = models.CharField(max_length=20,
                            verbose_name='悬赏头名称')
    logo = models.ImageField(verbose_name='Logo需求图片')
    first_letter = models.CharField(max_length=1,
                                    verbose_name='悬赏头字母')#比如古风头字母为G

    class Meta:
        db_table = 'DDSC_BRAND'
        verbose_name = '悬赏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class For_the_category(models.Model):
    """
    悬赏类别
    """
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name="更新时间")
    name = models.CharField(max_length=1000,
                            verbose_name='名称')
    sales = models.IntegerField(default=0,
                                verbose_name='悬赏浏览量')
    comments = models.IntegerField(default=0,
                                   verbose_name='评价数量')
    praise = models.IntegerField(default=0,
                                 verbose_name="赞的数量")
    brand = models.ForeignKey(Reward,on_delete=models.PROTECT, verbose_name='悬赏')

    catalog = models.ForeignKey(The_antique,on_delete=models.PROTECT,
                                related_name='The_antique_goods',
                                verbose_name='悬赏类别')

    class Meta:
        db_table = 'DDSC_For_the_category'
        verbose_name = 'For_the_category'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class  The_user_to_collect(models.Model):
    #收藏
    #用户点击收藏的时候触发该数据库
    count = models.CharField(max_length=1500,
                             verbose_name = "收藏链接",)
    catalog = models.ForeignKey(The_user,on_delete=models.PROTECT,
                                verbose_name="用户收藏")






#用户数据界面显示
class Photo_user(models.Model):
    logo = models.ImageField(verbose_name='Logo图片')
    name = models.CharField(max_length=10,verbose_name="显示id")
    gender = models.CharField(max_length=4,verbose_name="性别")
    catalog = models.ForeignKey(The_user,on_delete=models.PROTECT,
                                verbose_name="用户属性")


