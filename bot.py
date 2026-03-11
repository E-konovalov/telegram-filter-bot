import re
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters

# Настройки
TOKEN = "8652870745:AAFXQtLcw6DF1_AtWjWNhOml-9bE29-6spc"
ADMIN_ID = 8392355618
GROUPS = [5019228585, 4878911483]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    """Обработка команды /start"""
    await update.message.reply_text("✅ Бот запущен и работает!")
    logger.info(f"Start от пользователя {update.effective_user.id}")

async def check_message(update: Update, context):
    """Проверка сообщений на наличие чисел 3000+"""
    try:
        # Проверяем, что это сообщение из группы
        if not update.message or not update.message.text:
            return
            
        chat_type = update.message.chat.type
        if chat_type not in ['group', 'supergroup']:
            return
            
        chat_id = update.message.chat.id
        if chat_id not in GROUPS:
            return
            
        # Ищем числа, начинающиеся с 3000
        text = update.message.text
        if re.search(r'3000\d*', text):
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🔔 Найдено сообщение с числом 3000+\n\n{text[:200]}"
            )
            logger.info(f"Уведомление отправлено для группы {chat_id}")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")

def main():
    """Запуск бота"""
    logger.info("🚀 Запуск бота...")
    
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, check_message))
    
    logger.info("✅ Бот готов к работе")
    
    # Запускаем бота
    app.run_polling()

if __name__ == "__main__":
    main()
