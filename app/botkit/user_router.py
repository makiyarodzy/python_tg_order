from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router


user_router =Router()

@user_router.message(CommandStart())
async def start(msg:Message):
    await msg.answer("start")


