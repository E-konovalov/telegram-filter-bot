import re
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# ============================================
# ⚡ ВАШИ ДАННЫЕ (прописаны жестко)
# ============================================
BOT_TOKEN = "8652870745:AAFXQtLcw6DF1_AtWjWNhOml-9bE29-6spc"
YOUR_USER_ID = 8392355618
TARGET_GROUP_IDS = [5019228585, 4878911483]
# ============================================

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Простой старт"""
    await update.message.reply_text(
        "✅ Бот работает!\n"
        f"Отслеживаю групп: {len(TARGET_GROUP_IDS)}\n"
        "Ищу числа: 3000..."
    )
    logger.info(f"Start от {update.effective_user.id}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Поиск чисел 3000+"""
    try:
        # Проверяем, что это группа
        if not update.message or not update.message.text:
            return
            
        if update.message.chat.type not in ['group', 'supergroup']:
            return
            
        # Проверяем, наша ли группа
        if update.message.chat.id not in TARGET_GROUP_IDS:
            return
            
        # Ищем число 3000...
        text = update.message.text
        if re.search(r'3000\d*', text):
            # Отправляем уведомление
            await context.bot.send_message(
                chat_id=YOUR_USER_ID,
                text=f"🔔 Найдено: {text[:100]}"
            )
            logger.info("Уведомление отправлено")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")

def main():
    """Запуск"""
    logger.info("🚀 Запуск бота...")
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    logger.info("✅ Бот готов!")
    app.run_polling()

if __name__ == "__main__":
    main()
