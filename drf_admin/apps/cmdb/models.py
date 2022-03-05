from django.db import models

# Create your models here.

class ServerData(models.Model):
    name = models.CharField(max_length=30, verbose_name='实例名称')
    instance_id = models.CharField(max_length=30, unique=True,verbose_name='实例id')
    memory = models.IntegerField( verbose_name='内存')
    cpu = models.IntegerField( verbose_name='CPU')
    ipv4 = models.CharField(max_length=32, null=True, blank=True,verbose_name='ipv4地址')
    ipv6 = models.CharField(max_length=64, null=True, blank=True, verbose_name='ipv4地址')
    pub_ip= models.CharField(max_length=64, null=True, blank=True, verbose_name='公网地址')
    status = models.CharField(max_length=30,null=True, blank=True, verbose_name='状态')
    os = models.CharField(max_length=256, null=True, blank=True,verbose_name='操作系统')
    create_date = models.CharField(max_length=30, null=True, blank=True, verbose_name='创建时间')
    expired_date = models.CharField(max_length=30,null=True, blank=True, verbose_name='过期时间')
    tags = models.CharField(max_length=256,verbose_name='tags',null=True, blank=True)
    belong_flag = models.CharField(max_length=64, null=True, blank=True, verbose_name='归属标识')
    zone = models.CharField(max_length=32, null=True, blank=True,verbose_name='地区')
    cloud = models.CharField(max_length=32, null=True, blank=True,verbose_name='云平台')