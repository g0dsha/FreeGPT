import os
import time
import json
import random
import threading
import re
import g4f
from g4f import ChatCompletion
from googletrans import Translator
from flask import request
from datetime import datetime
from requests import get
from server.auto_proxy import get_random_proxy, update_working_proxies
from server.config import special_instructions


class Backend_Api:
    def __init__(self, app, config: dict) -> None:
        
        self.app = app
        self.use_auto_proxy = config['use_auto_proxy']
        self.routes = {
            '/backend-api/v2/conversation': {
                'function': self._conversation,
                'methods': ['POST']
            }
        }

        if self.use_auto_proxy:
            update_proxies = threading.Thread(
                target=update_working_proxies, daemon=True)
            update_proxies.start()

    def _conversation(self):

        try:
            streaming = request.json.get('stream', True)
            jailbreak = request.json['jailbreak']
            model = request.json['model']
            messages = build_messages(jailbreak)

            #random_proxy = get_random_proxy() # получаем случайный прокси
            #proxies = {"http": random_proxy, "https": random_proxy} # создаем словарь с прокси


            # Generate response
            response = ChatCompletion.create(model=model,
                                             messages=messages)
            #if 'curl_cffi.requests.errors.RequestsError' in response:
            #        response = ChatCompletion.create(model=model, stream=False,
            #                                         messages=messages)

            return self.app.response_class(generate_stream(response, jailbreak), mimetype='text/event-stream')

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_next)
            return {
                '_action': '_ask',
                'success': False,
                "error": f"an error occurred {str(e)}"
            }, 400


def build_messages(jailbreak):

    _conversation = request.json['meta']['content']['conversation']
    internet_access = request.json['meta']['content']['internet_access']
    prompt = request.json['meta']['content']['parts'][0]

    # Generate system message
    current_date = datetime.now().strftime("%Y-%m-%d")
    system_message = (
        f'You are ChatGPT also known as ChatGPT, a large language model trained by OpenAI. '
        f'Strictly follow the users instructions. '
        f'Current date: {current_date}. '
        f'{set_response_language(prompt)}'
    )

    # Initialize the conversation with the system message
    conversation = [{'role': 'system', 'content': system_message}]

    # Add the existing conversation
    conversation += _conversation

    # Add web results if enabled
    conversation += fetch_search_results(
        prompt["content"]) if internet_access else []

    # Add jailbreak instructions if enabled
    if jailbreak_instructions := isJailbreak(jailbreak):
        conversation += jailbreak_instructions

    # Add the prompt
    conversation += [prompt]

    # Reduce conversation size to avoid API Token quantity error
    conversation = conversation[-13:] if len(conversation) > 12 else conversation

    return conversation


def fetch_search_results(query):

    search = get('https://ddg-api.herokuapp.com/search',
                 params={
                     'query': query,
                     'limit': 5,
                 })

    results = []
    snippets = ""
    for index, result in enumerate(search.json()):
        snippet = f'[{index + 1}] "{result["snippet"]}" URL:{result["link"]}.'
        snippets += snippet
    results.append({'role': 'system', 'content': snippets})
    
    return results


def generate_stream(response, jailbreak):

    if isJailbreak(jailbreak):
        response_jailbreak = ''
        jailbroken_checked = False
        for message in response:
            response_jailbreak += message
            if jailbroken_checked:
                yield message
            else:
                if response_jailbroken_success(response_jailbreak):
                    jailbroken_checked = True
                if response_jailbroken_failed(response_jailbreak):
                    yield response_jailbreak
                    jailbroken_checked = True
    else:
        yield from response


def response_jailbroken_success(response: str) -> bool:

    act_match = re.search(r'ACT:', response, flags=re.DOTALL)
    return bool(act_match)


def response_jailbroken_failed(response):

    return False if len(response) < 4 else not (response.startswith ("GPT:") or response.startswith("ACT:"))


def set_response_language(prompt):

    translator = Translator()
    detected_language = translator.detect(prompt['content']).lang
    return f"You will respond in the language: {detected_language}. "


def isJailbreak(jailbreak):

    if jailbreak != "Default":
        return special_instructions[jailbreak] if jailbreak in special_instructions else None
    else:
        return None
