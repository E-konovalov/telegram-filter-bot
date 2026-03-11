import re
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# Данные бота
TOKEN = "8652870745:AAFRSQFznHtvD3QQQdEombhjrpbTYGsJrTU"
ADMIN_ID = 8392355618
GROUPS = [5019228585, 4878911483]

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда старт"""
    await update.message.reply_text("✅ Бот работает! Слежу за 2 группами.")
    logger.info(f"Start от {update.effective_user.id}")

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка сообщений"""
    try:
        if not update.message or not update.message.text:
            return
            
        if update.message.chat.type not in ['group', 'supergroup']:
            return
            
        if update.message.chat.id not in GROUPS:
            return
            
        text = update.message.text
        if re.search(r'3000\d*', text):
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🔔 Найдено: {text[:100]}"
            )
            logger.info(f"Уведомление отправлено")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")

if __name__ == "__main__":
    logger.info("🚀 Запуск бота...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, check_message))
    logger.info("✅ Бот запущен!")
    app.run_polling()
