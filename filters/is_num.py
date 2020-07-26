def is_num(function):
    async def wrapper(message):
        if not message.text.isdigit() or int(message.text) <= 0:
            await message.answer('Bad news')
            return
        await function(message)
    return wrapper
