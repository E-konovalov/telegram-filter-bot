import re
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# Данные бота
TOKEN = "8652870745:AAFXQtLcw6DF1_AtWjWNhOml-9bE29-6spc"
ADMIN_ID = 8392355618
GROUPS = [5019228585, 4878911483]

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда старт"""
    await update.message.reply_text("✅ Бот работает!")

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка сообщений"""
    try:
        # Проверяем что это группа
        if not update.message or not update.message.text:
            return
            
        if update.message.chat.type not in ['group', 'supergroup']:
            return
            
        # Проверяем что это наша группа
        if update.message.chat.id not in GROUPS:
            return
            
        # Ищем число 3000
        text = update.message.text
        if re.search(r'3000\d*', text):
            # Отправляем уведомление
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🔔 Найдено число 3000...\n\nСообщение: {text[:100]}"
            )
            logger.info(f"Уведомление отправлено для группы {update.message.chat.id}")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")

def main():
    """Запуск бота"""
    logger.info("🚀 Запуск бота...")
    
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
    
    logger.info("✅ Бот готов к работе")
    
    # Запускаем
    app.run_polling()

if __name__ == "__main__":
    main()
