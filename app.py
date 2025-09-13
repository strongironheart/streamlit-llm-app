from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
import os

# .envファイルの環境変数を読み込み
load_dotenv()

# OpenAIクライアントをグローバルで1回だけ生成
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def get_advice(role_message: str, user_message: str) -> str:
    if not client:
        return "APIキーが設定されていません。"
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": role_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.5
    )
    return completion.choices[0].message.content

# Streamlitアプリのタイトルと説明文
st.title("提出課題: 運動/食事アドバイスAIアプリ")

st.write("##### A: 運動アドバイスAI")
st.write("運動に関するアドバイスを提供します。")
st.write("##### B: 食事アドバイスAI")
st.write("食事に関するアドバイスを提供します。")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["運動アドバイス", "食事アドバイス"]
)

st.divider()

if selected_item == "運動アドバイス":
    input_message = st.text_input(label="運動に関する質問を入力してください。")
    role_message = "あなたは運動に関するエキスパートです。安全なアドバイスを提供してください。"
else:
    input_message = st.text_input(label="食事に関する質問を入力してください。")
    role_message = "あなたは食事に関するエキスパートです。安全なアドバイスを提供してください。"

if st.button("実行"):
    st.divider()
    if input_message:
        st.write(f"{selected_item}の質問: **{input_message}**")
        advice = get_advice(role_message, input_message)
        st.write(f"AIの回答: {advice}")
    else:
        st.error(f"{selected_item}の質問を入力してから「実行」ボタンを押してください。")


