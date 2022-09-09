import os
from random import shuffle
from time import sleep

from environs import Env
import telegram

from fetch_nasa_epic_images import fetch_nasa_epic_images
from fetch_nasa_images_of_the_day import fetch_nasa_images_of_the_day
from fetch_spacex_images import fetch_spacex_images


def main(token, chat_name, interval=14400):
    fetch_spacex_images()
    fetch_nasa_epic_images()
    fetch_nasa_images_of_the_day()

    bot = telegram.Bot(token=token)
    chat_id = bot.get_chat(chat_name)['id']

    while True:
        files = os.listdir('images')
        shuffle(files)

        for filename in files:
            bot.send_photo(chat_id=chat_id, photo=open(f'images/{filename}', 'rb'))
            sleep(interval)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHANNEL_NAME = env.str('TELEGRAM_CHANNEL_NAME')
    PUBLICATION_INTERVAL = env.int('PUBLICATION_INTERVAL')

    main(token=TELEGRAM_BOT_TOKEN, chat_name=TELEGRAM_CHANNEL_NAME, interval=PUBLICATION_INTERVAL)
