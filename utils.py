import os
import pathlib


import requests

NASA_API_KEY = 'GZtHmyRFjwZcpO6XIKa1jO8u9gRTtGRRaLfbx44i'

def get_file_ext(filename):
    return pathlib.Path(filename).suffix


def fetch_image(url, filename, params):
    headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        file.write(response.content)
