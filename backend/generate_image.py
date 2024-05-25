import requests
from env import settings


class GenerateImageService():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.AUTHORIZATION}"
    }

    model_url_mapper = {
        'AIServices': f'{settings.AI_CENTER_BE_URL}',
    }

    def gen_prompt_following_style(self, style: str):
        url = self.model_url_mapper['AIServices'] + "/text-to-image/gen-prompt"
        headers = self.headers

        body = {
            "style": style
        }
        # Request
        try:
            session = requests.Session()
            response = session.post(url=url,
                                    headers=headers,
                                    json=body)
            if response.status_code != 200:
                raise Exception(response.content)

            style, prompt, negative_prompt = response.json()['data']['style'], response.json()['data']['prompt'], response.json()['data']['negative_prompt']

            return style, prompt, negative_prompt

        except:
            session = requests.Session()
            response = session.post(url=url,
                                    headers=headers,
                                    json=body)
            if response.status_code != 200:
                raise Exception(response.content)

            style, prompt, negative_prompt = response.json()['data']['style'], response.json()['data']['prompt'], response.json()['data']['negative_prompt']

            return style, prompt, negative_prompt


    def text_to_image(self, host: str, model_name: str, prompt: str, negative_prompt: str, config: dict):
        url = self.model_url_mapper['AIServices'] + "/text-to-image"
        headers = self.headers

        config["image_content_type"] = "image/png"

        body = {
            "host": host,
            "model_name": model_name,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "config": config,
        }
        # Request
        try:
            session = requests.Session()
            response = session.post(url=url,
                                    headers=headers,
                                    json=body)
            if response.status_code != 200:
                raise Exception(response.content)

            url = response.json()['data']['file_url']['url']

            return url
        except:
            session = requests.Session()
            response = session.post(url=url,
                                    headers=headers,
                                    json=body)
            if response.status_code != 200:
                raise Exception(response.content)

            url = response.json()['data']['file_url']['url']

            return url
