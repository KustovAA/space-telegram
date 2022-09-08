from datetime import datetime
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


def fetch_spacex_last_launch():
    url = 'https://api.spacexdata.com/v5/launches/5eb87d46ffd86e000604b388'

    response = requests.get(url)
    response.raise_for_status()

    images = response.json()['links']['flickr']['original']

    for i in range(len(images)):
        filename = f'images/spacex_{i}{get_file_ext(images[i])}'
        fetch_image(images[i], filename)
        print(filename, ' is downloaded')


def fetch_nasa_images_of_the_day(count = 30):
    url = 'https://api.nasa.gov/planetary/apod'

    response = requests.get(url, params={'api_key': NASA_API_KEY, 'count': count})
    response.raise_for_status()

    images = response.json()

    for i in range(len(images)):
        image_url = images[i]['url']
        filename = f'images/nasa_{i}{get_file_ext(image_url)}'
        fetch_image(image_url, filename)
        print(filename, ' is downloaded')


def fetch_nasa_epic_images():
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
