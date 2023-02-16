from django.test import TestCase

# Create your tests here.
from reports.models import Report
from utils.process import process_date


class WXtestCase(TestCase):
    symbol = '*'
    msg = '15014424054*440803195801242921'
    text = msg.split(symbol, 1)
    query_set = Report.objects.filter(phone=text[0], idCard=text[1]).order_by('-id')[:1]
    if query_set.exists():
        # 有数据
        template = "【新型冠状病毒(COVID-19)核酸检测结果】\n" \
                   "姓名：%s\n" \
                   "采样机构：%s\n" \
                   "检测机构：湛江市坡头区人民医院\n" \
                   "检测日期：%s\n" \
                   "检测结果：%s\n" \
                   "此报告仅对所检验标本负责，如有疑议请在三天内与检验科联系！\n" \
                   "PDF版报告：【%s】, 请复制至浏览器打开。"
        for report in query_set:
            if not report.zjg:
                zjg = '阴性(-)'
            else:
                zjg = report.zjg
            print(report.inspection_date)
            break
            str_ss = report.inspection_date.split(' ', 1)
            folder = process_date(report.inspection_date)
            pdfUrl = "https://image.zhonghefull.com/pdf/%s/%s.pdf" % (folder, report.idCard)
            result = template % (report.name, report.hospital, str_ss[0], zjg, pdfUrl)
    print(result)
