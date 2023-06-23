import os, requests, uuid
from ...typing import sha256, Dict, get_type_hints

url = 'http://47.236.17.67'
model = ['gpt-4']
supports_stream = True

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5,zh;q=0.4',
        'Accept-Encoding': 'gzip, deflate'
    }
    data = {
        'messages': messages,
        'model': model
    }
    response = requests.post('http://47.236.17.67:3000/api/v1/openai/chat/completions', headers=headers, json=data,stream=True)
    for token in response.iter_content(chunk_size=2046):
        if b'always respond in english' not in token:
            yield (token.decode('utf-8'))
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
