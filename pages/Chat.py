import base64
import uuid
from copy import deepcopy
from io import BytesIO

import requests
from PIL import Image
import streamlit as st

from backend.chat import ChatBotService, ChatVisionService, parse_message

st.set_page_config(page_title="Chat", page_icon="📄")

st.markdown("""# <center>Chatbot & Chat-Vision</center>""", unsafe_allow_html=True)

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []
if "img_url" not in st.session_state:
    st.session_state.img_url = None
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = str(uuid.uuid4())

# Display chat messages from history on app rerun
for message in st.session_state.chat:
    if message["role"] == "user":
        chat_mess = st.chat_message(message["role"], avatar="🧑🏻")
    else:
        chat_mess = st.chat_message(message["role"], avatar="🤖")
    with chat_mess:
        if isinstance(message["content"], str):
            st.markdown(message["content"])
        elif isinstance(message["content"], list):
            st.image(message["content"][1]['image_url']['url'])
            st.markdown(message["content"][0]['text'])
        else:
            print(type(message["content"]))


def reset_messages():
    st.session_state.chat = []
    pass


def get_model_name(pa_mode: str, pa_host: str):
    if pa_mode == "GPTs":
        pa_mode = "Chat"
    key_name = pa_host + " " + pa_mode
    dict_model = {
        "OpenAI Chat": ("gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"),
        "OpenAI Chat-Vision": ("gpt-4o", "gpt-4-turbo"),
        "Fireworks Chat": ("dbrx-instruct", "mixtral-8x22b-instruct", "llama-v3-70b-instruct", "llama-v3-70b-instruct-hf"),
        "Fireworks Chat-Vision": ("firellava-13b", "llava-yi-34b"),
    }
    return dict_model[key_name]


def get_max_tokens_value(model: str):
    dict_token = {
        # OpenAI (Output limit is 4096 token)
        "gpt-4o": 128000,
        "gpt-4-turbo": 128000,
        "gpt-3.5-turbo": 16385,
        # Fireworks
        # # Chat
        "dbrx-instruct": 32768,
        "mixtral-8x22b-instruct": 65536,
        "llama-v3-70b-instruct": 8192,
        "llama-v3-70b-instruct-hf": 8192,
        # # ChatVision
        "firellava-13b": 4096,
        "llava-yi-34b": 4096,
    }
    return dict_token[model]


def chat_bot(messages: list, chat_model: dict, store_name: str = ""):
    message_placeholder = st.empty()
    full_response = ""
    message_placeholder.markdown(full_response + "▌")
    chunks = ChatBotService().get_chunks(messages, chat_model, store_name)
    try:
        for chunk in chunks.iter_content(decode_unicode=True, chunk_size=4096):
            try:
                response = parse_message(chunk)
                if isinstance(response, dict):
                    print(response)
                elif isinstance(response, str):
                    if not response:
                        continue
                    full_response += response
                    message_placeholder.markdown(full_response)

            except requests.exceptions.ChunkedEncodingError:
                continue
    except requests.exceptions.ChunkedEncodingError:
        pass

    return full_response


def chat_vision(messages: list, chat_model: dict):
    message_placeholder = st.empty()
    full_response = ""
    message_placeholder.markdown(full_response + "▌")
    chunks = ChatVisionService().get_chunks(messages, chat_model)
    try:
        for chunk in chunks.iter_content(decode_unicode=True, chunk_size=4096):
            try:
                response = parse_message(chunk)
                if isinstance(response, dict):
                    print(response)
                elif isinstance(response, str):
                    if not response:
                        continue
                    full_response += response
                    message_placeholder.markdown(full_response)

            except requests.exceptions.ChunkedEncodingError:
                continue
    except requests.exceptions.ChunkedEncodingError:
        pass

    return full_response


st.sidebar.header("Parameters")
img_url = None
with st.sidebar:
    # Mode
    mode = st.selectbox("Mode", ("Chat", "GPTs", "Chat-Vision"), on_change=reset_messages)
    if mode == "Chat":
        system_prompt = st.text_area(label="System Prompt", value="You are an assistant.")
    elif mode == "GPTs":
        store_name = st.selectbox("Store Name", ("Write For Me", "Humanizer Pro", "Canva", "Diagrams: Show Me", "Quality Raters SEO Guide", "AI PDF",
    "Video Script Generator", "Whimsical Diagrams", "ScholarAI", "ResearchGPT",
    "Assistente AI per CEO marketing oriented", "Math Mentor", "Universal Primer",
    "The Greatest Computer Science Tutor", "Astrology Fortune Teller", "The Rizz Game", "DeepGame", "Books",)
                                  , on_change=reset_messages)
    elif mode == "Chat-Vision":
        system_prompt = st.text_area(label="System Prompt", value="You are an assistant.")
        image_type = st.selectbox("Image Type", ("Upload File", "url"), )
        if image_type == "url":
            st.session_state.img_url = st.text_area(label="Image URL", value=st.session_state.img_url)
        elif image_type == "Upload File":
            img_uploader = st.file_uploader(label="Upload file", type=["jpg", "png", "tiff"],
                                            key=st.session_state.uploader_key)
            if img_uploader is not None:
                img_bytes = img_uploader.read()
                img = Image.open(BytesIO(img_bytes))
                img_format = img.format.lower()
                img_base64 = base64.b64encode(img_bytes).decode("utf-8")
                st.session_state.img_url = f"data:image/{img_format};base64,{img_base64}"
        if st.session_state.img_url:
            try:
                st.image(st.session_state.img_url)
            except:
                raise ValueError("Undified Image")
    # LLMs Param
    host = st.selectbox("Host Model", ("OpenAI", "Fireworks"), on_change=reset_messages)
    model_name = st.selectbox("Model", get_model_name(mode, host), on_change=reset_messages)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
    max_tokens = st.slider("Max_tokens", min_value=256, max_value=get_max_tokens_value(model_name), value=4096, step=2)
    max_messages = st.slider("Max Messages History Chat", min_value=4, max_value=100, value=40, step=2)
    st.session_state.chat = st.session_state.chat[-max_messages:]
    st.button('Clear History Chat', on_click=reset_messages)


# Chat
if prompt := st.chat_input("Text..."):
    # Display user message
    if st.session_state.img_url:
        content = [
            {"type": "text", "text": prompt},
            { "type": "image_url", "image_url": {"url": st.session_state.img_url}}
        ]
        st.session_state.chat.append({"role": "user", "content": content})
        with st.chat_message("user", avatar="🧑🏻️"):
            st.image(st.session_state.img_url)
            st.markdown(prompt)
        st.session_state.img_url = None
        st.session_state.uploader_key = str(uuid.uuid4())
    else:
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑🏻️"):
            st.markdown(prompt)

    # Display assistant message
    with st.chat_message("assistant", avatar="🤖"):
        messages = deepcopy(st.session_state.chat)
        if 'system_prompt' in globals():
            messages.insert(0, {"role": "system", "content": system_prompt})
        config = {
            "platform": host,
            "model_name": model_name,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if mode == "Chat-Vision":
            full_response = chat_vision(messages, config)
        else:
            if "store_name" in globals():
                full_response = chat_bot(messages, config, store_name)
            else:
                full_response = chat_bot(messages, config, "")

    # Add assistant response to chat history
    st.session_state.chat.append({"role": "assistant", "content": full_response})
