from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

from bot.services.api_client import APIClient

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("buy"))
async def cmd_buy(message: types.Message):
    """Buy ticket command"""
    
    try:
        # Get available tickets
        tickets = await APIClient.get_tickets()
        
        if not tickets:
            await message.answer("Hozircha biletlar mavjud emas.")
            return
        
        # Create ticket buttons
        keyboard_buttons = []
        for ticket in tickets:
            button = InlineKeyboardButton(
                text=f"{ticket['name']} - {ticket['price']} RUB",
                callback_data=f"ticket_{ticket['id']}"
            )
            keyboard_buttons.append([button])
        
        # Add back button
        keyboard_buttons.append([
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="menu")
        ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        text = """
🎟️ *Bilet sotib olish*

Quyidagi biletlardan birini tanlang:

• *Oddiy Bilet* - 500 RUB (1x imkoniyat)
• *Oltin Bilet* - 1000 RUB (3x imkoniyat)
• *VIP Bilet* - 5000 RUB (10x imkoniyat)

⚠️ *Diqqat:* Har bir bilet faqat bitta lotereya uchun
        """
        
        await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f"Error in cmd_buy: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")

@router.callback_query(lambda c: c.data.startswith("ticket_"))
async def select_ticket(callback: types.CallbackQuery):
    """Handle ticket selection"""
    
    ticket_id = int(callback.data.split("_")[1])
    
    try:
        # Get payment card info
        card = await APIClient.get_payment_card()
        
        if not card:
            await callback.message.answer("To'lov tizimi hozircha ishlamayapti.")
            return
        
        # Create payment instructions
        text = f"""
💳 *To'lov ma'lumotlari*

Karta raqami: `{card['number']}`
Bank: {card['bank']}
Egasi: {card['holder']}

💰 *To'lov tartibi:*
1. Yuqoridagi karta raqamiga to'lov qiling
2. To'lov chekini rasmga oling
3. Web App orqali chekni yuklang
4. Admin tekshiruvini kuting (24 soat ichida)

⚠️ *Muhim:*
• Faqat RUS bank kartalari qabul qilinadi
• Chekda karta raqami va summa ko'rinishi kerak
• To'lovni o'zingiz amalga oshirishingiz kerak
        """
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🌐 Web App da davom etish",
                        web_app=types.WebAppInfo(url=f"https://yourdomain.com/payment?ticket={ticket_id}")
                    )
                ],
                [
                    InlineKeyboardButton(text="🔙 Orqaga", callback_data="buy")
                ]
            ]
        )
        
        await callback.message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error in select_ticket: {e}")
        await callback.message.answer("Xatolik yuz berdi.")
        await callback.answer()
