from argparse import ArgumentParser
from os import path

import requests

from utils import fetch_image, get_file_ext


def fetch_spacex_images(launch_id="latest"):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"

    response = requests.get(url)
    response.raise_for_status()

    images = response.json()["links"]["flickr"]["original"]

    for image_index, image in enumerate(images):
        filename = path.join("images", f"spacex_{image_index}{get_file_ext(image)}")

        fetch_image(image, filename, {})
        print(filename, " is downloaded")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("id", nargs="?", default="latest")
    args = parser.parse_args()
    fetch_spacex_images(args.id)
