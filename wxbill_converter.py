from uuid import uuid4
from io import BytesIO

import pandas
import streamlit as st
from stqdm import stqdm as tqdm

from converter import wxbill_to_df

session_id = str(uuid4().hex)[:6]

# Page is like:
# TITLE
# caption
# []guide
# []result

st.set_page_config(
    page_title="微信PDF账单转换",
    page_icon=":cd:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🤙微信PDF账单转换")
st.markdown(
    """
    将微信导出的用于个人证明文件的PDF账单内容转换为`.xlsx`格式
    """
)

st.caption(f"若枫 用:heart:出品 | Session ID: {session_id.upper()}")
st.divider()

(result,) = st.columns(1)
guide = st.sidebar

guide.caption("操作指南")
result.caption("预览")
if "df" not in st.session_state:
    result.text(
        """
        请先上传文件
        """
    )

guide.subheader("第一步 设置参数")
add_meta = guide.checkbox(
    "添加元信息",
    value=False,
    help="添加记录归属人和微信号的信息，对混合多人账单的上传会很有用",
)
drop_dup = guide.checkbox("去重", value=True, help="对账单以交易订单号为字段去重，对重复选择一个人的账单文件很有用")


guide.subheader("第二步 上传文件")

wxbill = guide.file_uploader(
    "选择或拖动上传微信账单的PDF文件",
    "pdf",
    help="可以上传一份也可以上传全部，如果上传多人的微信账单，建议开启“添加元信息”以防止混淆。",
    accept_multiple_files=True,
    # label_visibility="hidden",
)


def get_df(wxbill, add_meta, drop_dup):
    df = pandas.DataFrame()
    if wxbill == []:
        result.error("请完成第一步上传文件", icon="🚨")
    else:
        for i in tqdm(wxbill, desc="批量转换文件", total=len(wxbill), st_container=result):
            df = pandas.DataFrame()
            df = pandas.concat(
                [df, wxbill_to_df(i, add_meta=add_meta, processor_container=result)],
                ignore_index=True,
            )
        if drop_dup:
            df.drop_duplicates(["交易单号"], inplace=True)

        buffer = BytesIO()
        with pandas.ExcelWriter(buffer) as w:
            df.to_excel(w, index=False)

        st.session_state["df"] = df
        st.session_state["buffer"] = buffer


guide.subheader("第三步 读取PDF并转换为表格")
guide.button(":arrows_clockwise:转换", on_click=get_df, args=(wxbill, add_meta, drop_dup))

guide.subheader("第四步 下载表格文件")
if "df" in st.session_state:
    result.dataframe(st.session_state["df"], height=620, use_container_width=True)
    guide.download_button(
        ":arrow_double_down:下载",
        st.session_state["buffer"],
        file_name=f"{session_id}-微信账单转换结果.xlsx",
    )
else:
    guide.caption("还没有上传文件")
