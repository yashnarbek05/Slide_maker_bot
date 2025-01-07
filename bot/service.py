from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler

INFORMATION = 1
LANGUAGE = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    keyboard = [
        [InlineKeyboardButton("English🇺🇸", callback_data="en")],
        [InlineKeyboardButton("O'zbek🇺🇿", callback_data="uz")],
        [InlineKeyboardButton("Русский🇷🇺", callback_data="ru")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please, choose language:", reply_markup=reply_markup)

    return LANGUAGE


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer("Progress...")

    messages = {
        'en': """Hello

📌 Please send your slide or abstract:
- name*, 
- to whom it belongs (University name, faculty name, department name, group and IFO),
- size* (how many sheets) and if any should be used 
- send literature (pdf, word or website) to help us.

* - must be filled in!""",

        'ru': """Привет

📌 Пожалуйста, пришлите слайд или аннотацию:
- имя*, 
- кому он принадлежит (название университета, название факультета, название кафедры, группа и IFO),
- размер* (сколько листов) и следует ли их использовать 
- присылайте литературу (pdf, word или веб-сайт), чтобы помочь нам.

* - необходимо заполнить!""",

        'uz': """Assalomu alaykum

📌 Iltimos, slaydingiz yoki referatingizning:
- nomini*, 
- kimga tegishli bo'lishi( Universitet nomi, fakultet nomi, yo'nalish nomi, guruh va IFO)ni,
- hajmi*( necha varoqligi)ni va agar bo'lsa foydalanish kerak bo'lgan 
- adabiyotlar( pdf, word yoki internet sayti)ni bizga yordam bo'lishi uchun yuboring.

* - to'ldirilishi shart!"""
    }

    await query.edit_message_text(text=messages.get(query.data))

    context.user_data['language'] = query.data

    return INFORMATION


async def infos() -> int:
    pass


async def cancel(update: Update, context: CallbackContext):
    messages = {
        'uz': 'Bekor qilindi!',
        'ru': 'Отменено!',
        'en': 'Cancelled!'
    }
    await update.message.reply_text(messages.get(context.user_data.get('language')))
    return ConversationHandler.END


async def finish() -> int:
    pass


async def error_handler() -> int:
    pass
