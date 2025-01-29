
from aiogram.types import Message
from aiogram import Router


order_route =Router()

@order_route.message()
async def pushOrderTg(msg:Message):
    await msg.answer_document(document="./order.xlsx")