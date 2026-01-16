from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

from bot.services.api_client import APIClient

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Start command handler"""
    
    # Create Web App button
    web_app = WebAppInfo(url=f"https://yourdomain.com/app?tg={message.from_user.id}")
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎫 Bilet sotib olish",
                    web_app=web_app
                )
            ],
            [
                InlineKeyboardButton(text="📊 G'oliblar", callback_data="winners"),
                InlineKeyboardButton(text="ℹ️ Yordam", callback_data="help")
            ]
        ]
    )
    
    welcome_text = f"""
👋 Assalomu alaykum, {message.from_user.first_name}!

🎲 *BAHODIR BRAT LOTEREYA BOT* ga xush kelibsiz!

📺 YouTube jonli efirlarida g'oliblar aniqlanadi va sovg'alar topshiriladi!

💎 *Imkoniyatlar:*
• Bilet sotib olish va lotereyada ishtirok etish
• Jonli efirlarda g'olib bo'lish
• Katta sovg'alarni yutib olish
• Do'stlarni taklif qilish

👇 Botdan to'liq foydalanish uchun pastdagi tugmani bosing:
    """
    
    await message.answer(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@router.callback_query(lambda c: c.data == "winners")
async def show_winners(callback: types.CallbackQuery):
    """Show winners list"""
    
    # Fetch winners from API
    try:
        winners = await APIClient.get_winners(limit=10)
        
        if not winners:
            text = "📭 Hozircha g'oliblar yo'q. Birinchi bo'ling!"
        else:
            text = "🏆 *Oxirgi 10 ta g'olib:*\n\n"
            for i, winner in enumerate(winners, 1):
                text += f"{i}. {winner['user_name']} - {winner['prize']}\n"
        
        await callback.message.answer(text, parse_mode="Markdown")
        
    except Exception as e:
        await callback.message.answer("Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")
    
    await callback.answer()

@router.callback_query(lambda c: c.data == "help")
async def show_help(callback: types.CallbackQuery):
    """Show help information"""
    
    help_text = """
❓ *Yordam va Ko'p Beriladigan Savollar*

1️⃣ *Qanday qilib ishtirok etaman?*
- "Bilet sotib olish" tugmasini bosing
- Bilet turini tanlang
- To'lov qiling va chekni yuklang
- Admin tomonidan tasdiqlangandan so'ng, bilet olasiz

2️⃣ *To'lov qanday amalga oshiriladi?*
- Faqat RUS bank kartalariga (Sberbank, Tinkoff, VTB)
- Karta raqamini ko'rsatamiz
- O'zingiz to'lov qilasiz
- Chekni rasmga olib yuklaysiz
- Admin tekshiradi va tasdiqlaydi

3️⃣ *G'olib qanday aniqlanadi?*
- YouTube jonli efirida tasodifiy tanlanadi
- Faqat tasdiqlangan biletlar ishtirok etadi
- O'yin halol va shaffof o'tkaziladi

4️⃣ *Sovg'alarni qanday olaman?*
- G'olib bo'lganingizda siz bilan bog'lanamiz
- Yetkazib berish yoki pul o'tkazma usuli
- Barcha yutuqlar topshiriladi

📞 *Aloqa:* @bahodir_brat_admin
    """
    
    await callback.message.answer(help_text, parse_mode="Markdown")
    await callback.answer()
