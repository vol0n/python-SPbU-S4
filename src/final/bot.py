import logging
import os
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters
from transformers import pipeline

logging.basicConfig(format="%(asctime)s | %(name)s | %(levelname)s : %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

generator = pipeline("text-generation", model="sshleifer/tiny-gpt2")


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = update.message
    if message is None:
        return None
    await message.reply_html(
        rf"Hi {user.mention_html() if user is not None else 'unknown user'}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None:
        return None
    await message.reply_text("This bot generates some text from your text using tiny-gpt2 model!\n")


async def generate(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    # todo: a better way to tell mypy these are non Nones
    if update.message is None or update.message.text is None:
        return
    generated_text = "\n".join(data["generated_text"] for data in generator(update.message.text))
    await update.message.reply_text(generated_text)


def main() -> None:
    application = ApplicationBuilder().token(os.environ["TG_API_TOKEN"]).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))

    application.run_polling()


if __name__ == "__main__":
    main()
