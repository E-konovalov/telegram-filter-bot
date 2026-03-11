import re
import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# ============================================
# ⚠️ ВАШИ ДАННЫЕ (уже вставлены)
# ============================================
BOT_TOKEN = "8652870745:AAETPuETnDXcIt7qN38bAkdqRraq92YRoRY" 
YOUR_USER_ID = 8392355618 

# ID групп для отслеживания
TARGET_GROUP_IDS = [
    5019228585,  # ID первой группы
    4878911483   # ID второй группы
]
# ============================================

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    logger.info(f"Получена команда /start от пользователя {update.effective_user.id}")
    
    # Проверяем, что бот добавлен в группы
    groups_info = []
    for group_id in TARGET_GROUP_IDS:
        try:
            chat = await context.bot.get_chat(group_id)
            groups_info.append(f"✅ {chat.title} (ID: {group_id})")
        except Exception as e:
            logger.error(f"Ошибка получения группы {group_id}: {e}")
            groups_info.append(f"❌ Группа с ID {group_id} (бот не добавлен или не админ)")
    
    groups_text = "\n".join(groups_info)
    
    await update.message.reply_text(
        f"👋 **Бот запущен и работает!**\n\n"
        f"📋 **Статус групп:**\n{groups_text}\n\n"
        f"🔍 Отслеживаются числа, начинающиеся с 3000\n"
        f"📨 Уведомления будут приходить сюда",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает сообщения и ищет числа, начинающиеся с 3000"""
    
    # Проверяем, что это сообщение из группы
    if not update.message or not update.message.text:
        return
    
    if update.message.chat.type not in ['group', 'supergroup']:
        return
    
    chat_id = update.message.chat.id
    
    # Проверяем, что группа в списке отслеживаемых
    if chat_id not in TARGET_GROUP_IDS:
        return
    
    text = update.message.text
    pattern = r'\b3000\d*\b'
    
    # Ищем числа, начинающиеся с 3000
    if re.search(pattern, text):
        chat_name = update.message.chat.title or "Без названия"
        sender = update.message.from_user.full_name
        message_id = update.message.message_id
        
        # Формируем ссылку на сообщение
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
    print("🚀 Запуск бота...")
    print(f"✅ Токен: {BOT_TOKEN[:10]}...")
    print(f"✅ Ваш ID: {YOUR_USER_ID}")
    print(f"✅ Группы: {TARGET_GROUP_IDS}")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    print("✅ Бот запущен и готов к работе!")
    application.run_polling()

if __name__ == "__main__":
    main()
