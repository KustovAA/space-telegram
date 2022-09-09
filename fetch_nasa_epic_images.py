from datetime import datetime

from environs import Env
import requests

from utils import fetch_image


def fetch_nasa_epic_images():
    env = Env()
    env.read_env()
    NASA_API_KEY = env.str('NASA_API_KEY', default='DEMO_KEY')

    url = 'https://api.nasa.gov/EPIC/api/natural'

    response = requests.get(url, params={'api_key': NASA_API_KEY})
    response.raise_for_status()

    images = response.json()

    for i in range(len(images)):
        year = datetime.fromisoformat(images[i]['date']).year
        month = datetime.fromisoformat(images[i]['date']).month
        day = datetime.fromisoformat(images[i]['date']).day
        ext = 'png'
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02}/{day:02}/{ext}/{images[i]['image']}.{ext}"
        filename = f'images/nasa_epic_{i}.{ext}'
        fetch_image(image_url, filename, {'api_key': NASA_API_KEY})
        print(filename, ' is downloaded')


if __name__ == '__main__':
    fetch_nasa_epic_images()
