import os, requests, uuid
from ...typing import sha256, Dict, get_type_hints
import json

url = 'https://mflsf.aitianhu.fun'
model = ['gpt-4']
supports_stream = True

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5,zh;q=0.4',
        'Content-Type': 'application/json'
    }
    data = {
        'model': model,
        'promt': messages,
        'systemMessage': 'You are ChatGPT, a large language model trained by OpenAI. Follow the user\'s instructions carefully. Respond using markdown.',
        'temperature': 0.8,
        'top_p':1,
    }
    response = requests.post(url + '/api/chat-process', headers=headers, json=data)
    decoder = json.JSONDecoder() # create a JSON decoder object
    index = 0 # initialize the index to zero
    for token in response.iter_content(chunk_size=2046):
        if b'always respond in english' not in token:
            s = token.decode('utf-8') # decode the token to a string
            while index < len(s): # loop until the end of the string
                obj, end = decoder.raw_decode(s, index) # parse an object from the string
                yield obj['text'] # get the text part of the object and yield it
                index = end # update the index to the end of the object
            

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f'{name}: {get_type_hints(_create_completion)[name].__name__}' for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
