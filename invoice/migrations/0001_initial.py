# Generated by Django 3.0.8 on 2021-01-25 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=32, unique=True, verbose_name='发票号码')),
                ('code', models.CharField(max_length=32, verbose_name='发票代码')),
                ('seller', models.CharField(max_length=256, verbose_name='销售方名称')),
                ('amount', models.CharField(max_length=32, verbose_name='发票金额')),
                ('purchaser', models.CharField(max_length=256, verbose_name='受票方名称')),
                ('date', models.CharField(max_length=20, verbose_name='开票日期')),
            ],
            options={
                'verbose_name': '发票列表',
                'verbose_name_plural': '发票列表',
            },
        ),
    ]
