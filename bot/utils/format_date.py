from datetime import datetime
import locale


def format_ukrainian_date(date_str):
    """
    Format a date string in the format 'YYYY-MM-DDTHH:MM:SS.ssssssZ' to Ukrainian format.
    """
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    day_month = dt.strftime("%Y-%m-%d")
    weekday = weekdays[dt.weekday()]

    return f"{day_month} {weekday}"

def format_request_date(date_str):
    """
    Format a date for full_date string in the format 'YYYY-MM-DDTHH:MM:SS.ssssssZ' to request format.
    """
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    return dt.strftime("%Y-%m-%d")


