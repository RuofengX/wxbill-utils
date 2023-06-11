import pathlib
from utils import format_date
from io import BufferedReader, BytesIO
from typing import Any

import pandas
import pdfplumber
from stqdm import stqdm as tqdm

TITLE = ["交易单号", "交易时间", "交易类型", "收/支/其他", "交易方式", "金额(元)", "交易对方", "商户单号"]


def _process_one_page(page) -> pandas.DataFrame:
    """处理除了第一页之后的所有页码"""
    return pandas.DataFrame(page.extract_table(), columns=TITLE)


def wxbill_to_df(
    file: str | pathlib.Path | BufferedReader | BytesIO,
    *,
    add_meta: bool = False,
    processor_container,
) -> pandas.DataFrame:
    """将微信PDF账单导出为DataFrame"""

    # 第一页的处理，第一页包含标题
    if isinstance(file, str):
        file = pathlib.Path(file)

    with pdfplumber.open(file) as pdf:
        # 添加身份信息
        _personal_line: str = pdf.pages[0].extract_text_lines()[2]["text"]
        personal_name: str = _personal_line[4 : _personal_line.find("(")]
        personal_wxid: str = _personal_line[
            _personal_line.find("在其微信号：") + 6 : _personal_line.find("中的交易明细信息如下：")
        ]

        # 获取表头
        first_table = pdf.pages[0].extract_table()
        assert first_table is not None, ValueError("微信账单的第一页中未找到表格")

        df = pandas.DataFrame(first_table[3:]).set_axis(TITLE, axis=1)

    if len(pdf.pages) > 1:  # 对后续页面进行提取、合并处理
        df = pandas.concat(
            [
                df,
                *tqdm(
                    map(_process_one_page, pdf.pages[1:]),
                    total=pdf.pages.__len__(),
                    initial=1,
                    # desc=f"微信账单转换://{file.parent.name}/{file.name}",
                    desc=f"正在转换'{personal_name}'的账单",
                    st_container=processor_container,
                ),
            ],
            ignore_index=True,
        )

    # 格式化内容
    df["交易时间"].replace("\n", " ", regex=True, inplace=True)  # 确保时间正确格式化
    df.replace("\n", "", regex=True, inplace=True)

    def slash_is_na(x: Any | pandas.Series):
        if isinstance(x, pandas.Series):
            rtn = []
            for i in x:
                rtn.append(slash_is_na(i))
            return rtn

        if x == "/":
            return pandas.NA
        else:
            return x

    df[["交易方式", "商户单号"]] = df[["交易方式", "商户单号"]].apply(
        slash_is_na,  # type:ignore[arg-type]
        axis=1,
        result_type="expand",  # type:ignore[arg-type]
    )

    # 格式化字段类型
    df["交易时间"] = df["交易时间"].apply(format_date)
    df["金额(元)"] = df["金额(元)"].astype("float64")

    # 添加metadata
    if add_meta:
        df["记录归属人"] = personal_name
        df["记录归属微信号"] = personal_wxid

    return df
