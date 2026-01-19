from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    await message.answer("Admin paneli tez orada ishga tushadi.")
