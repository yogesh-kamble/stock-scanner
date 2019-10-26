"""Common utils
"""
from datetime import datetime


def get_datestr_to_date(date_str):
    """
    :param date_str:
    :return:
    """
    return datetime.strptime(date_str,'%Y-%m-%d').date()
