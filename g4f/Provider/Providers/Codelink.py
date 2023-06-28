import os
import requests, re
from ...typing import sha256, Dict, get_type_hints
import json

class Model:
    def __init__(self, model):
        self.url = "https://ava-alpha-api.codelink.io/api/chat"
        self.headers = {
            "content-type": "application/json"
        }
        self.payload = {
            "model": model,
            "temperature": 0.6,
            "stream": True
        }
        self.accumulated_content = ""

    def _process_line(self, line):
        line_text = line.decode("utf-8").strip()
        if line_text.startswith("data:"):
            data = line_text[len("data:"):]
            try:
                data_json = json.loads(data)
                if "choices" in data_json:
                    choices = data_json["choices"]
                    for choice in choices:
                        if "finish_reason" in choice and choice["finish_reason"] == "stop":
                            break
                        if "delta" in choice and "content" in choice["delta"]:
                            content = choice["delta"]["content"]
                            self.accumulated_content += content
            except json.JSONDecodeError as e:
                return

    def ChatCompletion(self, messages):
        self.payload["messages"] = messages

        with requests.post(self.url, headers=self.headers, data=json.dumps(self.payload), stream=True) as response:
            for line in response.iter_lines():
                self._process_line(line)

        accumulated_content = self.accumulated_content
        self.accumulated_content = ""

        return accumulated_content

params = f’g4f.Providers.{os.path.basename(file)[:-3]} supports: ’ +
… ‘(%s)’ % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].name}" for name in _create_completion.code.co_varnames[:_create_completion.code.co_argcount]]) params ‘g4f.Providers.<stdin> supports: (model: str, messages: list, stream: bool)’