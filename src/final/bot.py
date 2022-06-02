import logging
from math import inf
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters
from transformers import pipeline

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s : %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

generator = pipeline('text-generation', model='gpt2')
max_len = 30
num_of_sentences = 1


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    await update.message.reply_text("This bot generates some text from your text using gp2 model!\n" +
                                    "You can set the length of the generated text using \\len command."
                                    "You can set the number of the generated text using \\num command.")


async def generate(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    generated_text = "\n".join(
        data['generated_text'] for data in generator(update.message.text, max_length=max_len + len(update.message.text),
                                                     num_return_sequences=num_of_sentences))
    await update.message.reply_text(generated_text)


def check_str_to_int(value: str, left: int = 1, right = inf) -> bool:
    try:
        converted: int = int(value)
        return left <= converted < right
    except ValueError:
        return False


async def set_num(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    global num_of_sentences
    if check_str_to_int(context.args[0]):
        num_of_sentences = context.args[0]
        await update.message.reply_text(f"Set number of generated sentences to {num_of_sentences}")
    else:
        await update.message.reply_text("Please provide a positive number!")


async def set_len(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    global max_len
    if check_str_to_int(context.args[0]):
        max_len = context.args[0]
        await update.message.reply_text(f"Set length of the generated message to {max_len}")
    else:
        await update.message.reply_text("Please provide a positive number!")


def main() -> None:
    application = ApplicationBuilder().token("5526805334:AAE7iEwmQyEiP70z6USCb1WSRKL03ek14CI").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler('len', set_len))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))

    application.run_polling()


if __name__ == "__main__":
    main()
