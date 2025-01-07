
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler, \
    filters

from bot.service import start, cancel, infos, finish, error_handler, INFORMATION, LANGUAGE, language
from config import BOT_TOKEN


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).read_timeout(300).write_timeout(300).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [CallbackQueryHandler(language)],
            INFORMATION: [CommandHandler('cancel', cancel), MessageHandler(filters.TEXT, infos)],

        },
        fallbacks=[CommandHandler('finish', finish)]
    )

    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)