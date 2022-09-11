import os
from random import shuffle
from time import sleep

from environs import Env
import telegram

from fetch_nasa_epic_images import fetch_nasa_epic_images
from fetch_nasa_images_of_the_day import fetch_nasa_images_of_the_day
from fetch_spacex_images import fetch_spacex_images


def call_with_retry(fn, delay = 0):
    try:
        sleep(delay)
        fn()
    except:
        call_with_retry(fn, 1 + 2 ** delay)


def main(token, chat_name, nasa_api_key, interval=14400):
    fetch_spacex_images()
    fetch_nasa_epic_images(api_key=nasa_api_key)
    fetch_nasa_images_of_the_day(api_key=nasa_api_key)

    bot = telegram.Bot(token=token)
    chat_id = bot.get_chat(chat_name)['id']

    def post_photo(chat_id, photo, interval):
        bot.send_photo(chat_id=chat_id, photo=photo)
        sleep(interval)

    while True:
        files = os.listdir('images')
        shuffle(files)

        for filename in files:
            filepath = os.path.join('images', filename)
            with open(filepath, 'rb') as photo:
                call_with_retry(
                    lambda: post_photo(chat_id=chat_id, photo=photo, interval=interval)
                )


if __name__ == '__main__':
    env = Env()
    env.read_env()
    nasa_api_key = env.str('NASA_API_KEY', default='DEMO_KEY')
    token = env.str('TELEGRAM_BOT_TOKEN')
    chat_name = env.str('TELEGRAM_CHANNEL_NAME')
    interval = env.int('PUBLICATION_INTERVAL', 14400)

    main(token=token, chat_name=chat_name, nasa_api_key=nasa_api_key, interval=interval)
