from django.db import models
from django_mysql.models import ListCharField
# Create your models here.
class Approve(models.Model):
    instance_name =  models.CharField(max_length=64, verbose_name='申请应用名称')
    apply_member = models.CharField(max_length=64, verbose_name='申请人')
    responsible_member = models.CharField(max_length=64, verbose_name='责任人')
    app = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),null=True, blank=True, verbose_name='申请应用')
    app_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='应用名称')
    # app = models.CharField(max_length=64, null=True, blank=True, verbose_name='申请应用')
    cache = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),null=True, blank=True, verbose_name='缓存')
    # cache = models.CharField( max_length=64,null=True, blank=True,verbose_name='缓存')
    msg_middleware = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),null=True, blank=True, verbose_name='消息中间件')
    # msg_middleware = models.CharField( max_length=64,null=True, blank=True,verbose_name='消息中间件')
    db = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),null=True, blank=True, verbose_name='数据库')
    # db = models.CharField(max_length=64, null=True, blank=True,verbose_name='数据库')
    zone = models.CharField(max_length=64, null=True, blank=True, verbose_name='云环境')
    env = models.CharField(max_length=64, verbose_name='环境')
    resources = models.JSONField(max_length=255, null=True, blank=True,verbose_name='资源')

    domain = models.JSONField(max_length=255, null=True, blank=True, verbose_name='域名')
    approve_check = models.BooleanField(verbose_name='审批确认完成' ,default=False)


class CheckApprove(models.Model):
    first = models.BooleanField(verbose_name='第一步' ,default=False)
    second = models.BooleanField(verbose_name='第二步' ,default=False)
    third = models.BooleanField(verbose_name='第三步' ,default=False)
    end = models.BooleanField(verbose_name='结束' ,default=False)
    approve_id = models.ForeignKey(Approve,on_delete=models.CASCADE)