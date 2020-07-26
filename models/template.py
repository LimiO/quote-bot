from typing import List
from datetime import datetime
from hashlib import md5
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont
from peewee import Model, PrimaryKeyField, IntegerField, CharField
from aiogram.types import InlineQueryResultCachedPhoto, InlineKeyboardMarkup, \
    InlineKeyboardButton

from utils import db, bot
from config import FONT_PATH
from messages import quote, quote_1


class Template(Model):
    id = PrimaryKeyField()
    name: str = CharField()
    file_id: str = CharField()
    file_path: str = CharField()
    font_path: str = FONT_PATH
    font_size: int = IntegerField()
    width: int = IntegerField()
    x: int = IntegerField()
    y: int = IntegerField()

    @classmethod
    def items(cls) -> List[InlineQueryResultCachedPhoto]:
        return [temp.item for temp in list(cls.select())]

    @property
    def item(self) -> InlineQueryResultCachedPhoto:
        now = datetime.now()
        id_ = md5(bytes((str(now)+self.file_path+str(now)).encode())).hexdigest()
        return InlineQueryResultCachedPhoto(
            id=id_, photo_file_id=self.file_id,
            title=self.name, caption=self.name, reply_markup=self.markup
        )

    @property
    def markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(quote, callback_data=f'quote_{self.id}'))
        return markup

    @staticmethod
    def next_file_name() -> str:
        dirs = os.listdir('templates')
        names = list()
        for item in dirs:
            name = item.split('.')[0]
            if name.isdigit():
                names.append(int(name))
        return f'templates/{max(names)+1}.jpg'

    async def send(self, text: str, user_id: int):
        image = Image.open(self.file_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font_path, size=self.font_size)
        text = textwrap.fill(text, width=self.width)
        offset, shadow_color = 4, 'black'
        x, y = self.x, self.y
        for off in range(offset):
            params = {"text": text, "font": font, "fill": shadow_color}
            draw.text((x - off, y), **params)
            draw.text((x + off, y), **params)
            draw.text((x, y + off), **params)
            draw.text((x, y - off), **params)
            draw.text((x - off, y + off), **params)
            draw.text((x + off, y + off), **params)
            draw.text((x - off, y - off), **params)
            draw.text((x + off, y - off), **params)

        draw.text((x, y), text, font=font, fill="white")
        name = f'results/{user_id}.jpg'
        image.save(name)
        with open(name, 'rb') as file:
            await bot.send_photo(user_id, file, quote_1)
        os.remove(name)

    class Meta:
        database = db
