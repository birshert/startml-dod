import json
import re
import sys

import requests
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(layout="wide")

st.sidebar.markdown("# Main page")


def get_bytes_size_in_mb(bytes_object):
    size_in_bytes = sys.getsizeof(bytes_object)
    size_in_mb = size_in_bytes / (1024 * 1024)  # Convert bytes to megabytes
    return size_in_mb


def whitespace_handler(k):
    return re.sub("\\s+", " ", re.sub("\n+", " ", k.strip()))


HEADERS = {"Content-Type": "application/json"}

st.title("Транскрибация и анализ записей")

URL = "http://172.16.238.10:55555/"

uploaded_file = st.file_uploader("Выберите аудио:")
if uploaded_file is not None:
    if get_bytes_size_in_mb(uploaded_file.getvalue()) >= 25:
        st.error("Файл не должен превышать 25 МБ")
        st.stop()

    st.audio(uploaded_file.getvalue())

if "data" not in st.session_state:
    st.session_state["data"] = {}

if st.button("Получить краткое содержание текста"):
    if uploaded_file is None:
        st.error("Выберите файл")
    else:
        files = {"file": uploaded_file}

        response = requests.post(URL, files=files)
        if response.ok:
            st.session_state["data"] = response.json()
        else:
            st.error("Ошибка с сервера")

st.subheader("Транскрипт")
html(st.session_state["data"].get("original_transcript", ""), height=100, scrolling=True)
st.subheader("Транскрипт на английском")
html(st.session_state["data"].get("transcript", ""), height=100, scrolling=True)
st.subheader("Краткое содержание")
html(st.session_state["data"].get("summary", ""), height=100, scrolling=True)

questions = st.text_area("Задайте вопросы по транскрипту", height=100)

json_questions = {
    "transcript": whitespace_handler(st.session_state["data"].get("transcript", "")),
    "question": f"{questions}",
}

if st.button("Получить ответ"):
    json_answers_on_questions = requests.post(URL + "ask_question", data=json.dumps(json_questions), headers=HEADERS)
    if json_answers_on_questions.ok:
        answers_on_questions = json_answers_on_questions.json()
        st.subheader("Ответ")
        html(answers_on_questions["answer"], height=100, scrolling=True)
    else:
        st.error("Ошибка с сервера")
        st.stop()
