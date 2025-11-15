from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
from database import init_database, add_user, save_answer, get_user_score
from tasks import get_todays_task, check_answer
import datetime


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)
    
    welcome_text = f"""
🎉 Привет, {user.first_name}!

Я бот для ежедневных заданий по программированию и логике.

Каждый день я буду присылать тебе новое задание.
За правильный ответ ты получишь баллы!

📋 Команды:
/task - получить задание
/score - узнать свои баллы

Удачи! 🚀
"""
    await update.message.reply_text(welcome_text)

async def task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task = get_todays_task()
    
    if task:
        task_text = f"🎯 Задание на сегодня:\n\n{task['task_text']}"
        await update.message.reply_text(task_text)
    else:
        await update.message.reply_text("📭 На сегодня заданий нет. Загляни завтра!")

async def score_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    score = get_user_score(user_id)
    
    score_text = f"🏆 Твои баллы: {score}"
    await update.message.reply_text(score_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    task = get_todays_task()
    
    if not task:
        await update.message.reply_text("❌ Сегодня нет активных заданий")
        return
    
    is_correct, score = check_answer(today, user_message)
    
    if is_correct:
        save_answer(user_id, today, user_message, score)
        await update.message.reply_text(f"✅ Правильно! Ты получил {score} балл(ов)!")
    else:
        await update.message.reply_text("❌ Неправильно. Попробуй еще раз!")

def main():
    init_database()
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("task", task_command))
    app.add_handler(CommandHandler("score", score_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен! Ожидаю сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()