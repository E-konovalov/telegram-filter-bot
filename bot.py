import re
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# ============================================
# ДАННЫЕ БОТА
# ============================================
TOKEN = "8652870745:AAFRSQFznHtvD3QQQdEombhjrpbTYGsJrTU"
ADMIN_ID = 8392355618

# Группы для отслеживания (включая тестовый канал)
GROUPS = [
    5019228585,  # Первая группа
    4878911483,  # Вторая группа
    8392355618   # Тестовый канал (ваш личный чат)
]
# ============================================

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда старт"""
    await update.message.reply_text(
        "✅ **Бот работает!**\n\n"
        f"📊 Отслеживаю чатов: {len(GROUPS)}\n"
        "🔍 Ищу числа от 6 до 12 цифр, начинающиеся с 300\n"
        "📨 Найденные сообщения пересылаются администратору",
        parse_mode='Markdown'
    )
    logger.info(f"Start от {update.effective_user.id}")

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка сообщений и пересылка найденных"""
    try:
        # Проверяем, что это сообщение из чата
        if not update.message or not update.message.text:
            return
            
        chat = update.message.chat
        
        # Проверяем, что это один из отслеживаемых чатов
        if chat.id not in GROUPS:
            return
            
        text = update.message.text
        sender = update.message.from_user
        sender_name = sender.full_name or sender.username or "Неизвестно"
        username = f"@{sender.username}" if sender.username else "нет username"
        
        # Ищем числа от 6 до 12 цифр, начинающиеся с 300
        # 6 цифр = 300xxx (300 + 3 цифры)
        # 12 цифр = 300xxxxxxxxx (300 + 9 цифр)
        pattern = r'\b300\d{3,9}\b'  # 300 + от 3 до 9 цифр = всего от 6 до 12 цифр
        
        found_numbers = re.findall(pattern, text)
        
        if found_numbers:
            # Формируем ссылку на сообщение
            if str(chat.id).startswith('-100'):
                message_link = f"https://t.me/c/{str(chat.id)[4:]}/{update.message.message_id}"
            else:
                message_link = f"https://t.me/c/{chat.id}/{update.message.message_id}"
            
            # Определяем тип чата для информации
            chat_type = "📢 Группа" if chat.type in ['group', 'supergroup'] else "💬 Личный чат"
            
            # Создаем пересланное сообщение
            forwarded_text = (
                f"📨 **Новая заявка!**\n\n"
                f"👤 **Отправитель:** {sender_name}\n"
                f"🆔 **Username:** {username}\n"
                f"{chat_type}: {chat.title or 'Личный чат'}\n"
                f"🔢 **Найденные числа:** {', '.join(found_numbers)}\n"
                f"📝 **Текст сообщения:**\n{text}\n\n"
                f"🔗 [Перейти к сообщению]({message_link})"
            )
            
            # Отправляем админу
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=forwarded_text,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
            
            logger.info(f"✅ Заявка переслана от {sender_name} из чата {chat.id}")
            logger.info(f"   Найденные числа: {found_numbers}")
            
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)

def main():
    """Запуск бота"""
    logger.info("🚀 Запуск бота...")
    logger.info(f"✅ ADMIN_ID: {ADMIN_ID}")
    logger.info(f"✅ Отслеживаемые чаты: {GROUPS}")
    
    try:
        # Создаем приложение
        app = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
        
        logger.info("✅ Бот запущен и готов к работе!")
        logger.info(f"🔍 Паттерн поиска: числа от 6 до 12 цифр, начинающиеся с 300")
        
        # Запускаем бота
        app.run_polling()
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)

if __name__ == "__main__":
    main()
