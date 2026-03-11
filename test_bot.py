import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройки
TOKEN = "8652870745:AAFXQtLcw6DF1_AtWjWNhOml-9bE29-6spc"

# Логирование в файл
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Простая команда старт"""
    logger.info(f"Получена команда /start от {update.effective_user.id}")
    await update.message.reply_text("✅ Тестовый бот работает!")

def main():
    """Запуск"""
    logger.info("="*50)
    logger.info("ЗАПУСК ТЕСТОВОГО БОТА")
    logger.info("="*50)
    
    try:
        # Создаем приложение
        app = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчик
        app.add_handler(CommandHandler("start", start))
        
        logger.info("✅ Бот создан, запускаем polling...")
        
        # Запускаем
        app.run_polling()
        
    except Exception as e:
        logger.error(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}", exc_info=True)

if __name__ == "__main__":
    main()
