from os import path

import requests
from environs import Env

from utils import fetch_image, get_file_ext


def fetch_nasa_images_of_the_day(api_key, count=30):
    url = "https://api.nasa.gov/planetary/apod"

    response = requests.get(url, params={"api_key": api_key, "count": count})
    response.raise_for_status()

    images = response.json()

    for image_index, image in enumerate(images):
        image_url = image["url"]
        filename = path.join("images", f"nasa_{image_index}{get_file_ext(image_url)}")
        fetch_image(image_url, filename, {})
        print(filename, " is downloaded")


if __name__ == "__main__":
    env = Env()
    env.read_env()
    api_key = env.str("NASA_API_KEY", default="DEMO_KEY")

    fetch_nasa_images_of_the_day(api_key=api_key)
