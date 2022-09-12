from datetime import datetime
from os import path

from environs import Env
import requests

from utils import fetch_image


def fetch_nasa_epic_images(api_key):
    url = 'https://api.nasa.gov/EPIC/api/natural'

    response = requests.get(url, params={'api_key': api_key})
    response.raise_for_status()

    images = response.json()

    for image_index, image in enumerate(images):
        date = datetime.fromisoformat(image['date'])
        year = date.year
        month = date.month
        day = date.day
        ext = 'png'
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02}/{day:02}/{ext}/{image['image']}.{ext}"
        filename = path.join('images', f'nasa_epic_{image_index}.{ext}')
        fetch_image(image_url, filename, {'api_key': api_key})
        print(filename, ' is downloaded')


if __name__ == '__main__':
    env = Env()
    env.read_env()
    api_key = env.str('NASA_API_KEY', default='DEMO_KEY')

    fetch_nasa_epic_images(api_key=api_key)
