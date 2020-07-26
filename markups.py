from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

import messages as msg


admin_markup = ReplyKeyboardMarkup(resize_keyboard=True)
admin_markup.row(msg.add_template)


main_markup = InlineKeyboardMarkup()
main_markup.row(InlineKeyboardButton(
    text=msg.check, switch_inline_query_current_chat='templates')
)