from argparse import ArgumentParser
import os
from random import shuffle
from time import sleep

from environs import Env
import telegram

from fetch_nasa_epic_images import fetch_nasa_epic_images
from fetch_nasa_images_of_the_day import fetch_nasa_images_of_the_day
from fetch_spacex_images import fetch_spacex_images


def main(token, chat_name, interval):
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
    parser = ArgumentParser()
    parser.add_argument('interval', nargs='?', default=4 * 60 * 60)
    args = parser.parse_args()

    env = Env()
    env.read_env()
    TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHANNEL_NAME = env.str('TELEGRAM_CHANNEL_NAME')

    main(token=TELEGRAM_BOT_TOKEN, chat_name=TELEGRAM_CHANNEL_NAME, interval=int(args.interval))
