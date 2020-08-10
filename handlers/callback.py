from aiogram.types import CallbackQuery

from utils import dp, bot
from filters import is_admin
import messages as msg
import markups
import db


@dp.callback_query_handler(lambda call: call.data.startswith('quote_'))
async def quote_0(call: CallbackQuery):
    user = db.get_user(call.from_user.id)
    user.set_state(call.data)
    await bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=None)
    await bot.send_message(call.from_user.id, msg.quote_0)


@dp.callback_query_handler(lambda call: call.data == 'main_menu')
async def main_menu(call: CallbackQuery):
    user = db.get_user(call.from_user.id)
    user.reset_state()
    await call.message.edit_text(msg.start_msg, reply_markup=markups.main_markup)


@dp.callback_query_handler(lambda call: call.data == 'suggest_template')
async def suggest_0(call: CallbackQuery):
    user = db.get_user(call.from_user.id)
    user.set_state('suggest_template')
    await call.message.edit_text(msg.suggest_0, reply_markup=markups.back_markup('main_menu'))
