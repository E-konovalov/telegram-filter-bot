import re
import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Настройки из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
YOUR_USER_ID = int(os.environ.get("YOUR_USER_ID", "0"))

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает сообщения и ищет числа, начинающиеся с 3000"""
    if update.message and update.message.text:
        text = update.message.text
        pattern = r'\b3000\d*\b'
        
        if re.search(pattern, text):
            chat_name = update.message.chat.title or "личные сообщения"
            sender = update.message.from_user.full_name
            
            alert_text = (
                f"🔔 Найдено сообщение с числом 3000...\n"
                f"Чат: {chat_name}\n"
                f"От: {sender}\n"
                f"Текст: {text[:200]}...\n"
                f"Ссылка: {update.message.link if update.message.link else 'нет ссылки'}"
            )
            
            try:
                await context.bot.send_message(chat_id=YOUR_USER_ID, text=alert_text)
                logger.info(f"Уведомление отправлено пользователю {YOUR_USER_ID}")
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение: {e}")

def main():
    """Запуск бота"""
    if not BOT_TOKEN or YOUR_USER_ID == 0:
        logger.error("Не заданы BOT_TOKEN или YOUR_USER_ID!")
        return
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчик
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Для Bothost.ru используем вебхуки
    port = int(os.environ.get("PORT", "8080"))
    webhook_url = os.environ.get("WEBHOOK_URL", None)
    
    if webhook_url:
        logger.info(f"Запуск с вебхуком на порту {port}")
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=BOT_TOKEN,
            webhook_url=f"{webhook_url}/{BOT_TOKEN}"
        )
    else:
        logger.warning("WEBHOOK_URL не задан, запускаю polling (только для теста!)")
        application.run_polling()

if __name__ == "__main__":
    main()