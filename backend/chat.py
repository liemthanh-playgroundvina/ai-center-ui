import requests
from env import settings


class ChatBotService():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.AUTHORIZATION}"
    }

    model_url_mapper = {
        'AIServices': f'{settings.AI_CENTER_BE_URL}/chat',
    }

    def get_chunks(self, messages: list, chat_model: dict, store_name: str = ""):
        url = self.model_url_mapper['AIServices']
        headers = self.headers
        body = {
            "messages": messages,
            "chat_model": chat_model,
        }
        if store_name:
            body['store_name'] = store_name
        # Request
        try:
            session = requests.Session()
            response = session.post(url=url,
                                    headers=headers,
                                    json=body,
                                    stream=True)
            if response.status_code != 200:
                raise Exception(response.content)

            return response
        except:
            session = requests.Session()
            response = session.post(url=url,
                                    headers=headers,
                                    json=body,
                                    stream=True)
            if response.status_code != 200:
                raise Exception(response.content)

            return response


class ChatVisionService():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.AUTHORIZATION}"
    }

    model_url_mapper = {
        'AIServices': f'{settings.AI_CENTER_BE_URL}/chat-vision',
    }

    def get_chunks(self, messages: list, chat_model: dict):
        url = self.model_url_mapper['AIServices']
        headers = self.headers
        body = {
            "messages": messages,
            "chat_model": chat_model,
        }
        # Request
        try:
            session = requests.Session()
            response = session.post(url=url,
                                    headers=headers,
                                    json=body,
                                    stream=True)
            if response.status_code != 200:
                raise Exception(response.content)

            return response
        except:
            session = requests.Session()
            response = session.post(url=url,
                                    headers=headers,
                                    json=body,
                                    stream=True)
            if response.status_code != 200:
                raise Exception(response.content)

            return response


def parse_message(input_text):
    lines = input_text.split('\n')
    message_dict = {}
    line_break = False
    key_break = None
    for line in lines:
        key_value = line.split(': ')
        if key_value.__len__() == 2:
            key, value = key_value
        else:
            key = key_value[0]
            value = "\n"
        value = value.replace("\r", "")
        if key in message_dict:
            message_dict[key] += value
            line_break = True
            key_break = key
        else:
            message_dict[key] = value
    if line_break:
        message_dict[key_break] += "\n"
    if "data" in message_dict:
        return (message_dict["data"].
                replace("[DATA_STREAMING]", "").
                replace("[DONE]", "").
                replace("[METADATA]", "").
                replace("<!<newline>!>", "\n")) if message_dict["data"] else ""
