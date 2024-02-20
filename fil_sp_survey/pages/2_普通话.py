import streamlit as st
import pandas as pd
import json

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import tempfile

def slack(channel, msg, files=None):
    oauth_token = st.secrets["slack_token"]
    client = WebClient(token=oauth_token)
    client.chat_postMessage(channel=channel, text=msg)

    if files is not None:
        for fp in files:
            try:
                response = client.files_upload(
                    channels=channel,
                    file=fp,
                )
                assert response["file"]  # the uploaded file
            except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                assert e.response["ok"] is False
                assert e.response["error"]

# Load your dataframe (you can replace this with your own data)
l3_df = pd.DataFrame({
    "收入": ["交易收入 ($16/TiB/Yr)", "区块奖励 ($8/TiB/Yr)", None, None, None, None, None, None],
    "协议费用": ["燃油费 ($2/TiB/Yr)", "封装 ($2/TiB/Yr)", None, None, None, None, None, None],
    "运营成本": ["算力 ($8/TiB/Yr)", "带宽 ($6/TiB/Yr)", "员工 ($8/TiB/Yr)", "数据准备 ($1/TiB/Yr)", None, None, None, None],
    "资本性支出": ["存储硬件花费 （USD $6.0 每TiB/每年）", None, None, None, None, None, None, None],
    "融资成本": ["质押收益分成 ($4/TiB/Yr)", None, None, None, None, None, None, None],
    "额外费用": ["业务发展 ($8/TiB/Yr)", "额外副本 ($2/TiB/Yr)", "额外带宽 ($2/TiB/Yr)", None, None, None, None, None]
})

# Display the editable dataframe
st.title("Filecoin存储提供商调查")
e
st.write("以下是一项匿名调查，旨在帮助了解存储提供商的成本和收入。" + \
         "将对回复进行总结，以提供对存储提供程序微观经济学的见解。" + \
         "请尽可能详细地提供您的最佳估算。" + \
         "\n\n 所有字段都是可选的。感谢您抽出宝贵时间接受采访！" + \
         "\n\n 点击提交 👈 发送您的回复。\n\n")

# color this header blue
st.markdown("<h4 style='color: blue;'>分类帐</h4>", unsafe_allow_html=True)
st.markdown("""
本节要求提供有关成本和收入的信息。在下表中，每个条目代表
列指定的类别的特定成本或收入来源。默认条目以美元/TiB/年为单位显示如下，可以通过双击进行编辑
在细胞上。 \n\n 随意使用最适合您的单位。请为每个条目提供描述，
与默认条目类似。例如：而不是输入值 \$16/TiB/Yr, 最好进入
"交易收入 (\$16/TiB/Yr)", 等等。默认文本说明和类别作为指南提供。
\n\n

对于可以用FIL或法定货币计价的收入和成本（例如区块奖励收入或燃油费），请指明金额是以法定货币还是以FIL计价。如果使用假设的FIL的美元币价也可以，但请提供币价的假设 （比如USD $5.0 一个FIL）。您也可以指定您锁定的美元价格，以及对冲成本。

例如，区块奖励收入可以用三种方式报告：\n\n
方法1：区块奖励（USD $6.0 每TiB/每年，按假设USD $5.0 一个⨎FIL币价算) \n\n
方法2：区块奖励（FIL ⨎1.0 每TiB/每年）\n\n
方法3：区块奖励（USD $8.0 每TiB/每年，锁定USD $5.0 一个⨎FIL币价，对冲成本为USD $x.00 每TiB/每年) \n\n

如果您决定提供汇总成本和收入，请注明，并附上如下说明： Total($24/TiB/Yr). \n\n
 \n\n
""")
edited_df = st.data_editor(l3_df, use_container_width=True)

st.markdown("<h4 style='color: blue;'>基本信息</h4>", unsafe_allow_html=True)
location = st.text_input("地理位置", placeholder="节点所在城市，国家", key="location")
rbp_size = st.text_input("RBP (PiB)", placeholder="10", key="rbp")
qap_size = st.text_input("QAP (PiB)", placeholder="50", key="qap")
feedback = st.text_area("反馈", placeholder="请在此处提供任何反馈或其他信息。", key="feedback")

def get_default(str_in, default="Unknown"):
    if str_in is None or str_in == "":
        return default
    return str_in

def submit_fn():
    ts = pd.Timestamp.now().isoformat()
    data_dict = {
        "location": get_default(location, "Unknown"),
        "rbp_size": get_default(rbp_size, "-1"),
        "qap_size": get_default(qap_size, "-1"),
        "feedback": get_default(feedback, "No feedback provided"),
        "ledger": edited_df.to_json(),
        "submit_time": ts,
        "language": "Mandarin"
    }
    with tempfile.TemporaryDirectory() as tmpdirname:
        fp = f"{tmpdirname}/survey.json"
        with open(fp, 'w') as f:
            json.dump(data_dict, f)
        slack("#sp_survey", "New survey submission from @ Time=%s!" % (ts,), files=[fp])
    st.toast("Thank you for your submission!", icon="👏")

with st.sidebar:
    st.button("Submit!", on_click=submit_fn)
