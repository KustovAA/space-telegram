from environs import Env
import telegram


if __name__ == '__main__':
    env = Env()
    env.read_env()
    TELEGRAM_API_KEY = env.str('TELEGRAM_API_KEY')
    bot = telegram.Bot(token=TELEGRAM_API_KEY)
    chat_id = bot.get_chat('@space_7e1bf756_images')['id']
    
    bot.send_message(chat_id=chat_id, text="Первый пост!")
