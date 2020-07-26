from aiogram import Bot, Dispatcher
from playhouse.postgres_ext import PostgresqlExtDatabase
import requests

from config import TOKEN, DB_HOST, DB_PASSWORD, DB_USER, DB_NAME


bot = Bot(TOKEN, parse_mode='html')
bot_username = requests.post(f'https://api.tlgr.org/bot{TOKEN}/getMe').json().get('result').get('username')
dp = Dispatcher(bot)


db = PostgresqlExtDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD,
                           host=DB_HOST, autocommit=True, autoconnect=True)