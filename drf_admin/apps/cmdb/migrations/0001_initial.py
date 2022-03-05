# Generated by Django 3.1.7 on 2021-07-04 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServerData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='实例名称')),
                ('instance_id', models.CharField(max_length=30, unique=True, verbose_name='实例id')),
                ('memory', models.CharField(max_length=5, verbose_name='内存')),
                ('cpu', models.CharField(max_length=5, verbose_name='CPU')),
                ('ipv4', models.CharField(max_length=32, verbose_name='ipv4地址')),
                ('ipv6', models.CharField(blank=True, max_length=64, null=True, verbose_name='ipv4地址')),
                ('pub_ip', models.CharField(blank=True, max_length=64, null=True, verbose_name='公网地址')),
                ('status', models.CharField(max_length=30, verbose_name='状态')),
                ('os', models.CharField(max_length=30, verbose_name='操作系统')),
                ('create_date', models.CharField(max_length=30, verbose_name='创建时间')),
                ('expired_date', models.CharField(max_length=30, verbose_name='过期时间')),
                ('tags', models.CharField(blank=True, max_length=256, null=True, verbose_name='tags')),
            ],
        ),
    ]