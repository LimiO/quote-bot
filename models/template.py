from typing import List, Tuple
from datetime import datetime
from hashlib import md5
import os

from PIL import Image, ImageDraw, ImageFont
from peewee import Model, PrimaryKeyField, IntegerField, CharField
from aiogram.types import InlineQueryResultCachedPhoto, InlineKeyboardMarkup, \
    InlineKeyboardButton

from utils import db, bot
from messages import quote, info_template, caption_template
from config import CHANNEL_ID


class Template(Model):
    id = PrimaryKeyField()
    name: str = CharField()
    pic_file_id: str = CharField()
    temp_file_id: str = CharField(null=True)
    file_path: str = CharField()
    font_path: str = CharField()
    font_size: int = IntegerField()
    font_color: str = CharField()
    width: int = IntegerField()
    left_x: int = IntegerField()
    left_y: int = IntegerField()
    right_x: int = IntegerField()
    right_y: int = IntegerField()
    rectangle_color: str = CharField()
    align: str = CharField()
    offset: int = IntegerField(null=True)
    shadow_color: str = CharField(null=True)

    @classmethod
    def items(cls) -> List[InlineQueryResultCachedPhoto]:
        return [temp.item for temp in list(cls.select())]

    async def save_template(self):
        image = Image.open(self.file_path)
        draw = ImageDraw.Draw(image)
        draw.rectangle(((self.left_x, self.left_y), (self.right_x, self.right_y)),
                       width=2, outline=self.rectangle_color)
        self.draw_text(draw, self.info)
        name, extension = self.file_path.split('.')
        new_name = name+'_temp.'+extension
        image.save(new_name)
        with open(new_name, 'rb') as file:
            msg = await bot.send_photo(CHANNEL_ID, file)
        self.temp_file_id = msg.photo[-1].file_id
        os.remove(new_name)
        self.save()

    def draw_text(self, draw, text: str):
        text = self.__formatted_text(text)
        font = self.image_font
        w, h = draw.textsize(text, font=font)
        x, y = self.cords(w, h)
        draw.text((x, y), text, font=font, fill=self.font_color, align=self.align)
        if self.offset:
            for off in range(self.offset):
                params = {"text": text, "font": font, "fill": self.shadow_color,
                          "align": self.align}
                draw.text((x - off, y), **params)
                draw.text((x + off, y), **params)
                draw.text((x, y + off), **params)
                draw.text((x, y - off), **params)
                draw.text((x - off, y + off), **params)
                draw.text((x + off, y + off), **params)
                draw.text((x - off, y - off), **params)
                draw.text((x + off, y - off), **params)

    @property
    def info(self) -> str:
        return info_template.format(self.name, self.font_size, self.width)

    @property
    def item(self) -> InlineQueryResultCachedPhoto:
        now = datetime.now()
        id_ = md5(bytes((str(now)+self.file_path+str(now)).encode())).hexdigest()
        return InlineQueryResultCachedPhoto(
            id=id_, photo_file_id=self.temp_file_id,
            title=self.name, caption=caption_template.format(self.name),
            reply_markup=self.markup
        )

    @staticmethod
    def next_file_name() -> str:
        dirs = os.listdir('templates')
        names = list()
        for item in dirs:
            name = item.split('.')[0]
            if name.isdigit():
                names.append(int(name))
        return f'templates/{max(names) + 1}.jpg'

    @property
    def markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(quote, callback_data=f'quote_{self.id}'))
        return markup

    @property
    def image_font(self) -> ImageFont.truetype:
        return ImageFont.truetype(self.font_path, size=self.font_size)

    async def send(self, text: str, user_id: int):
        image = Image.open(self.file_path)
        draw = ImageDraw.Draw(image)
        self.draw_text(draw, text)
        name = f'results/{user_id}.jpg'
        image.save(name)
        with open(name, 'rb') as file:
            await bot.send_photo(user_id, file)
        os.remove(name)

    def cords(self, w: int, h: int) -> Tuple[float, float]:
        return (self.left_x+self.right_x-w)/2, (self.left_y+self.right_y-h)/2

    def __formatted_line(self, text: str) -> str:
        words = text.split(' ')
        new_string, line = str(), str()
        for word in words:
            if len(line + word) > self.width:
                new_string += line + '\n'
                line = ''
            line += word + ' '
        new_string += line + '\n'
        return new_string

    def __formatted_text(self, text: str) -> str:
        result = str()
        for line in text.splitlines():
            result += self.__formatted_line(line)
        return result.strip()

    class Meta:
        database = db
