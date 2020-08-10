import os

from aiogram.types import Message

from config import CREATOR
from utils import dp, bot, font_pic
from filters import is_admin
import messages as msg
import markups
import db


@dp.message_handler(commands=['start'])
async def start_(message: Message):
    user = db.get_user(message.from_user.id)
    user.reset_state()
    await message.answer(msg.start_msg, reply_markup=markups.main_markup)


@dp.message_handler(commands=['suggest'])
async def suggest_command(message: Message):
    user = db.get_user(message.from_user.id)
    user.set_state('suggest_template')
    await message.answer(msg.suggest_0, reply_markup=markups.back_markup('main_menu'))


@dp.message_handler(commands=['reset'])
async def reset(message: Message):
    user = db.get_user(message.from_user.id)
    user.reset_state()
    await message.answer(msg.reset_0, reply_markup=markups.back_markup('main_menu'))


@dp.message_handler(lambda m: db.get_user(m.from_user.id).state == 'suggest_template',
                    content_types=['photo', 'document'])
async def suggest_1(message: Message):
    user = db.get_user(message.from_user.id)
    user.reset_state()
    caption = msg.suggest_template.format(
        message.from_user.url, message.from_user.full_name, message.caption or ''
    )
    if message.photo:
        await bot.send_photo(CREATOR, message.photo[-1].file_id, caption)
    else:
        await bot.send_document(CREATOR, message.document.file_id, caption=caption)
    await message.answer(msg.suggest_1)


@dp.message_handler(commands=['admin'])
@is_admin
async def admin_(message: Message):
    await message.answer(msg.start_msg, reply_markup=markups.admin_markup)


@dp.message_handler(lambda m: m.text == msg.check_fonts)
@is_admin
async def check_fonts(message: Message):
    font_pic()
    with open('fonts.jpg', 'rb') as file:
        await message.answer_photo(file)
    os.remove('fonts.jpg')


@dp.message_handler(lambda m: m.text in msg.templates)
@is_admin
async def add_template(message: Message):
    admin = db.get_user(message.from_user.id)
    admin.set_state(msg.templates_dict[message.text])
    await message.answer(msg.templates[message.text])


@dp.message_handler(lambda m: db.get_user(m.from_user.id).state == 'add_template',
                    content_types=['photo'])
@is_admin
async def admin_state(message: Message):
    admin = db.get_user(message.from_user.id)
    args = message.caption.split(';')
    if len(args) == 6:
        args.extend([None, None])
    items, name, font_name, font_color, rectangle_color, align, offset, shadow_color = args
    if offset:
        offset = int(offset)
    font_size, width, left_x, left_y, right_x, right_y = list(map(int, items.split()))
    photo = message.photo[-1]
    file_name = db.Template.next_file_name()
    await bot.download_file_by_id(
        photo.file_id, destination=file_name
    )
    template = db.set_template(
        photo.file_id, file_name, font_size, width,
        left_x, left_y, right_x, right_y, name,
        'fonts/'+font_name, font_color, rectangle_color,
        align, offset, shadow_color,
    )
    await template.save_template()
    admin.reset_state()
    await message.answer(msg.admin_states_1)


@dp.message_handler(lambda m: db.get_user(m.from_user.id).state == 'add_font',
                    content_types=['document'])
async def font_0(message: Message):
    await bot.download_file_by_id(
        message.document.file_id, destination=f'fonts/{message.document.file_name}'
    )
    await message.answer(msg.admin_states_3)


@dp.message_handler(lambda m: db.get_user(m.from_user.id).state.startswith('quote_'))
async def quote_1(message: Message):
    user = db.get_user(message.from_user.id)
    temp_id = int(user.state[6:])
    template = db.get_template(temp_id)
    await template.send(message.text, user.id)
    user.reset_state()