import os
from random import shuffle
from time import sleep

from environs import Env
from retry import retry
import telegram

from fetch_nasa_epic_images import fetch_nasa_epic_images
from fetch_nasa_images_of_the_day import fetch_nasa_images_of_the_day
from fetch_spacex_images import fetch_spacex_images


def main(token, chat_name, nasa_api_key, interval=14400):
    fetch_spacex_images()
    fetch_nasa_epic_images(api_key=nasa_api_key)
    fetch_nasa_images_of_the_day(api_key=nasa_api_key)

    bot = telegram.Bot(token=token)
    chat_id = bot.get_chat(chat_name)['id']

    @retry(
        exceptions=telegram.error.TelegramError,
        delay=1,
        backoff=2,
        tries=10
    )
    def post_photo(chat_id, photo):
        bot.send_photo(chat_id=chat_id, photo=photo)

    while True:
        files = os.listdir('images')
        shuffle(files)

        for filename in files:
            filepath = os.path.join('images', filename)
            with open(filepath, 'rb') as photo:
                post_photo(chat_id=chat_id, photo=photo)
                sleep(interval)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    nasa_api_key = env.str('NASA_API_KEY', default='DEMO_KEY')
    token = env.str('TELEGRAM_BOT_TOKEN')
    chat_name = env.str('TELEGRAM_CHANNEL_NAME')
    interval = env.int('PUBLICATION_INTERVAL', 14400)

    main(token=token, chat_name=chat_name, nasa_api_key=nasa_api_key, interval=interval)
