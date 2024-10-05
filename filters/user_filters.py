from aiogram.filters import BaseFilter
from aiogram.types import Message
from data import config

class UserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id not in config.ADMINS