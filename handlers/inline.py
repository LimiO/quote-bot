from aiogram.types import InlineQuery

from utils import dp, bot
from filters import is_admin, is_num
import messages as msg
import markups
import db


@dp.inline_handler(lambda query: query.query == 'templates')
async def templates(query: InlineQuery):
    items = db.Template.items()
    await query.answer(results=items, cache_time=10)