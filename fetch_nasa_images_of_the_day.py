from environs import Env
import requests

from utils import fetch_image, get_file_ext


def fetch_nasa_images_of_the_day(count = 30):
    env = Env()
    env.read_env()
    NASA_API_KEY = env.str('NASA_API_KEY', default='DEMO_KEY')

    url = 'https://api.nasa.gov/planetary/apod'

    response = requests.get(url, params={'api_key': NASA_API_KEY, 'count': count})
    response.raise_for_status()

    images = response.json()

    for i in range(len(images)):
        image_url = images[i]['url']
        filename = f'images/nasa_{i}{get_file_ext(image_url)}'
        fetch_image(image_url, filename, {})
        print(filename, ' is downloaded')


if __name__ == '__main__':
    fetch_nasa_images_of_the_day()
