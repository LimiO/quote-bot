import os

from aiogram import Bot, Dispatcher
from playhouse.postgres_ext import PostgresqlExtDatabase
from PIL import Image, ImageDraw, ImageFont
import requests

from config import TOKEN, DB_HOST, DB_PASSWORD, DB_USER, DB_NAME, PIC_WIDTH,\
    FONT_HEIGHT, PF_HEIGHT, TOP_MARGIN, LEFT_MARGIN
from messages import test_template


bot = Bot(TOKEN, parse_mode='html')
bot_username = requests.post(f'https://api.tlgr.org/bot{TOKEN}/getMe').json().get('result').get('username')
dp = Dispatcher(bot)


db = PostgresqlExtDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD,
                           host=DB_HOST, autocommit=True, autoconnect=True)


def font_pic():
    fonts = os.listdir('fonts')
    image = Image.new('RGB', (PIC_WIDTH, len(fonts)*PF_HEIGHT), 'white')
    draw = ImageDraw.Draw(image)
    for num, font_ in enumerate(fonts):
        font = ImageFont.truetype(font=f'fonts/{font_}', size=FONT_HEIGHT)
        draw.text((LEFT_MARGIN, TOP_MARGIN+num*PF_HEIGHT),
                  test_template.format(font_), font=font, fill='black')
    image.save('fonts.jpg', 'JPEG')

