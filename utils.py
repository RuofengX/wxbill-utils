from datetime import datetime, timedelta

DATE_FORMAT = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y.%m.%d",
    "%Y年%m月%d日",
    "%Y.%m",
    "%Y年%m月",
    "%b-%y",
]


def format_date(date_string: datetime | str | int):
    if isinstance(date_string, datetime):
        return date_string

    if isinstance(date_string, int):
        # 将1900年1月1日转换为datetime对象
        base_date = datetime(1900, 1, 1)
        # 计算int天后的日期
        return base_date + timedelta(days=date_string)

    if isinstance(date_string, float):
        date_string = str(date_string)

    assert isinstance(date_string, str), TypeError(f"错误的输入值{date_string}")
    if date_string == "":
        return None
    rtn = None
    for df in DATE_FORMAT:
        try:
            rtn = datetime.strptime(date_string, df)
        except ValueError:
            continue
    if rtn is None:
        raise ValueError(f"无效的数据格式{date_string}")
    return rtn
