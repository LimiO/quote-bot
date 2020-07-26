from config import ADMINS


def is_admin(admin_func):
    async def wrapper(message):
        if message.from_user.id in ADMINS:
            await admin_func(message)
    return wrapper
