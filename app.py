import streamlit as st
from PIL import Image
import requests
from io import BytesIO

#import logging

#logging.basicConfig(level=logging.DEBUG)

from agent import InteriorConsultantAgent

if 'history' not in st.session_state:
    st.session_state.history = []
if 'agent' not in st.session_state:
    st.session_state.agent = InteriorConsultantAgent()

initial_message = """
## インテリアコーディネートAI
### 機能
- インテリアコーディネートの相談
- ヒアリング内容に基づく画像の生成
- 関連商品の検索
### インストラクション
ユーザーのインテリアコーディネートの希望をヒアリングした上で、画像と共にコーディネートの提案をします。例えば次のような項目など、希望する事項を自由に相談してみてください。
- ベースとなる部屋について（広さ、壁や床の質感、部屋の用途など）
- インテリアスタイル（モダン、ミッドセンチュリー、ナチュラルなど）
- テーマカラー、アクセントカラー
- 配置したい家具

画像を見たい、関連商品を見たい場合はリクエストしてみてください。
"""
st.sidebar.markdown(initial_message)

user_input = st.sidebar.text_area(label="入力", key="user_input")

if user_input:
    value = user_input
    st.session_state.history.append(("You", value))
    st.write(f"You: {value}\n")
    result = st.session_state.agent.invoke(f"ユーザーの希望: {value}")
    st.session_state.history.append(("Assistant", result["output"]))
    st.write(f"Assistant: {result['output']}\n")
    if result["image_url"]:
        generated_img_res = requests.get(result["image_url"])
        generated_img = Image.open(BytesIO(generated_img_res.content))
        st.image(generated_img, caption='出力された画像', use_column_width=True)
    if result["products"]:
        print(result["products"])
    with st.sidebar.expander("会話履歴"):
        history_str = ''
        for role, text in reversed(st.session_state.history):
            history_str += f"{role}: {text}\n\n"
        st.write(history_str)
    st.sidebar.json(st.session_state.agent.plan.json())
