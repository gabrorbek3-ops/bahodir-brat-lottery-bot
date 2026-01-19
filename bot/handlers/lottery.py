from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("my_tickets"))
async def cmd_my_tickets(message: types.Message):
    await message.answer("Sizning biletlaringiz haqida ma'lumot tez orada qo'shiladi.")

@router.message(Command("balance"))
async def cmd_balance(message: types.Message):
    await message.answer("Balansni ko'rish funksiyasi tez orada qo'shiladi.")
