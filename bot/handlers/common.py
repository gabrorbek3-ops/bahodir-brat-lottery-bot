from aiogram import Router, types

router = Router()

@router.message()
async def fallback(message: types.Message):
    await message.answer("Buyruq topilmadi. /start yoki /help ni bosing.")
