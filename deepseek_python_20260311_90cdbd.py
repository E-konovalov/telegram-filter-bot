import re
import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# Настройки из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
YOUR_USER_ID = int(os.environ.get("YOUR_USER_ID", "0"))

# ID групп, за которыми следит бот (ваши реальные ID)
TARGET_GROUP_IDS = [
    5019228585,  # ID первой группы
    4878911483   # ID второй группы
]

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    groups_info = []
    for group_id in TARGET_GROUP_IDS:
        # Пытаемся получить информацию о группе
        try:
            chat = await context.bot.get_chat(group_id)
            groups_info.append(f"• {chat.title} (ID: {group_id})")
        except:
            groups_info.append(f"• Группа с ID {group_id} (недоступна - проверьте, добавлен ли бот в группу)")
    
    groups_text = "\n".join(groups_info) if groups_info else "• Группы не указаны"
    
    await update.message.reply_text(
        "👋 **Бот запущен и работает!**\n\n"
        f"📋 **Отслеживаемые группы:**\n{groups_text}\n\n"
        "🔍 Отслеживаются числа, начинающиеся с 3000\n"
        "📨 Уведомления отправляются администратору",
        parse_mode='Markdown'
    )
    logger.info(f"Команда /start от пользователя {update.effective_user.id}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает сообщения и ищет числа, начинающиеся с 3000"""
    
    # Проверяем, что сообщение из группы и есть текст
    if not update.message or not update.message.text:
        return
    
    # Проверяем, что это групповой чат
    if update.message.chat.type not in ['group', 'supergroup']:
        return
    
    chat_id = update.message.chat.id
    
    # Проверяем, что группа в списке отслеживаемых
    if chat_id not in TARGET_GROUP_IDS:
        logger.debug(f"Сообщение из группы {chat_id} (не в списке) проигнорировано")
        return
    
    text = update.message.text
    pattern = r'\b3000\d*\b'
    
    if re.search(pattern, text):
        chat_name = update.message.chat.title or "Без названия"
        sender = update.message.from_user.full_name
        message_id = update.message.message_id
        
        # Формируем ссылку на сообщение
        # Для групп с положительными ID ссылка формируется иначе
        if str(chat_id).startswith('-100'):
            # Для супергрупп
            message_link = f"https://t.me/c/{str(chat_id)[4:]}/{message_id}"
        else:
            # Для обычных групп
            message_link = f"https://t.me/c/{chat_id}/{message_id}"
        
        alert_text = (
            f"🔔 **Найдено сообщение с числом 3000...**\n"
            f"📢 **Группа:** {chat_name}\n"
            f"👤 **От:** {sender}\n"
            f"📝 **Сообщение:** {text[:200]}...\n"
            f"🔗 **Ссылка:** {message_link}"
        )
        
        try:
            await context.bot.send_message(
                chat_id=YOUR_USER_ID, 
                text=alert_text,
                parse_mode='Markdown'
            )
            logger.info(f"✅ Уведомление отправлено о сообщении из группы {chat_name}")
        except Exception as e:
            logger.error(f"❌ Не удалось отправить уведомление: {e}")

def main():
    """Запуск бота"""
    if not BOT_TOKEN or YOUR_USER_ID == 0:
        logger.error("❌ Не заданы BOT_TOKEN или YOUR_USER_ID!")
        return
    
    if not TARGET_GROUP_IDS:
        logger.error("❌ Не указаны ID групп для отслеживания!")
        return
    
    logger.info(f"🚀 Бот запускается. Будет отслеживать {len(TARGET_GROUP_IDS)} групп(ы)")
    for group_id in TARGET_GROUP_IDS:
        logger.info(f"   • Группа ID: {group_id}")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Для Bothost.ru используем вебхуки
    port = int(os.environ.get("PORT", "8080"))
    webhook_url = os.environ.get("WEBHOOK_URL", None)
    
    if webhook_url:
        logger.info(f"🌐 Запуск с вебхуком на порту {port}")
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=BOT_TOKEN,
            webhook_url=f"{webhook_url}/{BOT_TOKEN}"
        )
    else:
        logger.warning("⚠️ WEBHOOK_URL не задан, запускаю polling (только для теста!)")
        application.run_polling()

if __name__ == "__main__":
    main()
