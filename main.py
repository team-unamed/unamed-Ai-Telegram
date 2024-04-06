import requests
import os
import dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


dotenv.load_dotenv()

token = os.getenv("TOKEN")
username = "@UnamedAiBot"



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I'm UnamedAiBot.  for more info use /help")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ask me about the blockchain. I can provide data about a lot of diffrent blockchains and how they work(+ more info on the Ton blockchain).")





# Responses

def handel_response(text: str, model: str) -> str:
    e = get_answers(text, model)
    return e["answer"]



def get_answers(question, model):
    headers  = {
        "Content-Type": "application/json"
    }

    payload = {
        "question": question,
        "model": model,
        "master_key": os.getenv("master_key"),

    }
    r = requests.post("https://unamed-ai-k7ml7hype-aaravatgits-projects.vercel.app/ask", params=payload, headers=headers)
    print(r.json(), r.status_code)
    return r.json()



async def handel_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    message_type = update.message.chat.type

    if message_type == "group":
        if username in text:
            text = text.replace(username, "").strip()
            response = handel_response(text, "ton")
        else:
            return
    else:
        response = handel_response(text, "ton")

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} causes error {context.error}")



if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(token).build()

    # COMMANDS
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))

    # MESSAGES
    app.add_handler(MessageHandler(filters.TEXT, handel_message))

    # ERRORS
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=2)


