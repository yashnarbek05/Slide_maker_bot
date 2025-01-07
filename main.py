from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler, \
    filters

from bot.service import start, cancel, infos, finish, error_handler, INFORMATION, LANGUAGE, language, FINISH, admin
from config import BOT_TOKEN, MY_CHAT_ID


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).read_timeout(300).write_timeout(300).build()

    application.add_handler(MessageHandler(filters.Chat(MY_CHAT_ID), admin))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [CallbackQueryHandler(language)],
            INFORMATION: [CommandHandler('cancel', cancel), MessageHandler(filters.TEXT, infos)],
            FINISH: [CommandHandler('finish', finish)]

        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)


    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

