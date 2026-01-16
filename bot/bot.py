import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import settings
from bot.handlers import start, payment, admin, lottery, common

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main bot function"""
    
    # Initialize bot
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Initialize dispatcher
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Register handlers
    dp.include_router(start.router)
    dp.include_router(payment.router)
    dp.include_router(lottery.router)
    dp.include_router(admin.router)
    dp.include_router(common.router)
    
    # Set bot commands
    await set_bot_commands(bot)
    
    # Start polling
    logger.info("Starting bot...")
    await dp.start_polling(bot)

async def set_bot_commands(bot: Bot):
    """Set bot commands menu"""
    from aiogram.types import BotCommand, BotCommandScopeDefault
    
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="buy", description="Bilet sotib olish"),
        BotCommand(command="my_tickets", description="Mening biletlarim"),
        BotCommand(command="balance", description="Balans"),
        BotCommand(command="winners", description="G'oliblar"),
        BotCommand(command="help", description="Yordam"),
    ]
    
    await bot.set_my_commands(commands, BotCommandScopeDefault())

if __name__ == "__main__":
    asyncio.run(main())
