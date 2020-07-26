from aiogram.types import Message

from utils import dp, bot
from filters import is_admin, is_num
import messages as msg
import markups
import db


@dp.message_handler(commands=['start'])
async def start_(message: Message):
    user = db.get_user(message.from_user.id)
    user.reset_state()
    await message.answer(msg.start_msg, reply_markup=markups.main_markup)


@dp.message_handler(commands=['admin'])
@is_admin
async def admin_(message: Message):
    await message.answer(msg.start_msg, reply_markup=markups.admin_markup)


@dp.message_handler(lambda m: m.text in msg.templates)
@is_admin
async def add_template(message: Message):
    admin = db.get_user(message.from_user.id)
    admin.set_state(msg.templates_dict[message.text])
    await message.answer(msg.admin_states_0)


@dp.message_handler(lambda m: (state := db.get_user(m.from_user.id).state in msg.templates_dict.values()),
                    content_types=['photo', 'text'])
@is_admin
async def admin_state(message: Message):
    admin = db.get_user(message.from_user.id)
    if admin.state == 'add_template':
        items, name = message.caption.split(';')
        font_size, width, x, y = list(map(int, items.split()))
        photo = message.photo[-1]
        file_name = db.Template.next_file_name()
        await bot.download_file_by_id(
            photo.file_id, destination=file_name
        )
        db.set_template(photo.file_id, file_name,
                        font_size, width, x, y, name)
    admin.reset_state()
    await message.answer(msg.admin_states_1)


@dp.message_handler(lambda m: db.get_user(m.from_user.id).state.startswith('quote_'))
async def quote_1(message: Message):
    user = db.get_user(message.from_user.id)
    temp_id = int(user.state[6:])
    template = db.get_template(temp_id)
    await template.send(message.text, user.id)
    user.reset_state()