from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

import messages as msg


admin_markup = ReplyKeyboardMarkup(resize_keyboard=True)
admin_markup.row(msg.add_template)
admin_markup.row(msg.add_font)
admin_markup.row(msg.check_fonts)


main_markup = InlineKeyboardMarkup()
main_markup.row(InlineKeyboardButton(text=msg.check, switch_inline_query_current_chat='templates'))
main_markup.row(InlineKeyboardButton(text=msg.suggest, callback_data='suggest_template'))


def back_markup(callback: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=msg.back, callback_data=callback))
    return markup
