import re
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from telegram.error import InvalidToken

# ============================================
# ДАННЫЕ БОТА
# ============================================
TOKEN = "8652870745:AAFXQtLcw6DF1_AtWjWNhOml-9bE29-6spc"
ADMIN_ID = 8392355618
GROUPS = [5019228585, 4878911483]
# ============================================

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start"""
    try:
        await update.message.reply_text(
            "✅ **Бот работает!**\n\n"
            f"📊 Отслеживаю групп: {len(GROUPS)}\n"
            "🔍 Ищу числа: 3000...\n"
            "📨 Уведомления отправляются администратору",
            parse_mode='Markdown'
        )
        logger.info(f"✅ Команда /start от {update.effective_user.id}")
    except Exception as e:
        logger.error(f"❌ Ошибка в start: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка сообщений на наличие чисел 3000+"""
    try:
        # Проверяем, что это сообщение из группы
        if not update.message or not update.message.text:
            return
            
        chat = update.message.chat
        if chat.type not in ['group', 'supergroup']:
            return
            
        # Проверяем, что это одна из наших групп
        if chat.id not in GROUPS:
            logger.info(f"Сообщение из чужой группы {chat.id}")
            return
            
        # Ищем числа, начинающиеся с 3000
        text = update.message.text
        if re.search(r'\b3000\d*\b', text):
            # Формируем ссылку на сообщение
            message_link = f"https://t.me/c/{str(chat.id)[4:]}/{update.message.message_id}" if str(chat.id).startswith('-100') else f"https://t.me/c/{chat.id}/{update.message.message_id}"
            
            # Отправляем уведомление
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"🔔 **Найдено число 3000+**\n\n"
                    f"📢 **Группа:** {chat.title}\n"
                    f"👤 **От:** {update.message.from_user.full_name}\n"
                    f"📝 **Сообщение:** {text[:200]}\n"
                    f"🔗 [Перейти к сообщению]({message_link})"
                ),
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
            logger.info(f"✅ Уведомление отправлено для группы {chat.title}")
            
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_message: {e}")

async def remove_webhook():
    """Очистка вебхука перед запуском"""
    try:
        from telegram import Bot
        bot = Bot(TOKEN)
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ Вебхук очищен")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка при очистке вебхука: {e}")
        return False

def main():
    """Запуск бота"""
    logger.info("🚀 Запуск бота...")
    
    # Создаем и запускаем событийный цикл для очистки вебхука
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Очищаем вебхук
    if not loop.run_until_complete(remove_webhook()):
        logger.warning("⚠️ Продолжаем, даже если вебхук не очищен")
    
    try:
        # Создаем приложение
        app = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info(f"✅ Бот готов к работе! Отслеживается групп: {len(GROUPS)}")
        
        # Запускаем бота (polling)
        app.run_polling()
        
    except InvalidToken:
        logger.error("❌ НЕВЕРНЫЙ ТОКЕН! Проверьте TOKEN в коде")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
