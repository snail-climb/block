# coding=utf8
from datetime import datetime


# 日期格式校验(%Y-%m-%d)
def is_valid_year_month_day(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# 日期格式校验(%Y-%m)
def is_valid_year_month(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m")
        return True
    except ValueError:
        return False
