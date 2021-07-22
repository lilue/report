from django.db import models


# Create your models here.
class Report(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="姓名")
    gender = models.CharField(max_length=10, null=True, blank=True, verbose_name="性别")
    age = models.CharField(max_length=200, null=True, blank=True, verbose_name="年龄")
    barcode = models.CharField(max_length=200, null=True, blank=True, verbose_name="条码号")
    outpatient = models.CharField(max_length=200, null=True, blank=True, verbose_name="门诊号")
    bed = models.CharField(max_length=200, null=True, blank=True, verbose_name="病床")
    department = models.CharField(max_length=200, null=True, blank=True, verbose_name="送检科室")
    doctor = models.CharField(max_length=100, null=True, blank=True, verbose_name="送检医生")
    hospital = models.CharField(max_length=200, null=True, blank=True, verbose_name="送检医院")
    sampling_time = models.CharField(max_length=100, null=True, blank=True, verbose_name="采样时间")
    sample_num = models.CharField(max_length=200, null=True, blank=True, verbose_name="样本号")
    sample_type = models.CharField(max_length=200, null=True, blank=True, verbose_name="样本类型")
    sample_status = models.CharField(max_length=200, null=True, blank=True, verbose_name="样本状态")
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name="联系方式")
    idCard = models.CharField(max_length=50, null=True, blank=True, verbose_name="证件号")
    items = models.TextField(default=[], null=True, blank=True, verbose_name="检验项目")
    proposal = models.CharField(max_length=200, null=True, blank=True, verbose_name="检验结果")
    inspection_date = models.CharField(max_length=100, null=True, blank=True, verbose_name="检验日期")
    report_date = models.CharField(max_length=100, null=True, blank=True, verbose_name="报告日期")
    examiner = models.CharField(max_length=100, null=True, blank=True, verbose_name="检验者")
    reviewer = models.CharField(max_length=100, null=True, blank=True, verbose_name="审核者")
    remarks = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")
    zjg = models.CharField(max_length=200, null=True, blank=True, default='', verbose_name="总结果")
    ORFlab = models.CharField(max_length=200, null=True, blank=True, default='', verbose_name="ORFlab基因")
    N = models.CharField(max_length=200, null=True, blank=True, default='', verbose_name="N基因")
    sampling_agency = models.CharField(max_length=200, null=True, blank=True, default='', verbose_name="采样机构")
    # models.TextField
    # null = True, blank = True


class Subscription(models.Model):
    phone = models.CharField(max_length=50, verbose_name="联系方式")
    idCard = models.CharField(max_length=50, verbose_name="证件号")
    open_id = models.CharField(max_length=50, verbose_name="微信openid")

