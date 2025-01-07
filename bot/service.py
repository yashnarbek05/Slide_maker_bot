from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext

from config import MY_CHAT_ID

INFORMATION = 1
LANGUAGE = 0
FINISH = 2


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    keyboard = [
        [InlineKeyboardButton("English🇺🇸", callback_data="en")],
        [InlineKeyboardButton("O'zbek🇺🇿", callback_data="uz")],
        [InlineKeyboardButton("Русский🇷🇺", callback_data="ru")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please, choose language:", reply_markup=reply_markup)

    # Get the profile photos of the user
    user_id = update.message.from_user.id
    photos = await context.bot.get_user_profile_photos(user_id, offset=0, limit=1)

    if photos.total_count > 0:
        # Get the file_id of the first photo (smallest size)
        file_id = photos.photos[0][-1].file_id  # [-1] for the highest resolution photo

        # Send the photo to your specified chat ID
        await context.bot.send_photo(
            chat_id=MY_CHAT_ID,
            photo=file_id,
            caption=f"""New user:
            
user_id:  {update.message.from_user.id}
name:     {update.message.from_user.first_name}
username: {update.message.from_user.username if update.message.from_user.username else 'not'}
"""
        )
    else:
        await context.bot.send_message(
            chat_id=MY_CHAT_ID,
            text=f"""New user:
            
user_id:  {update.message.from_user.id}
name:     {update.message.from_user.first_name}
username: @{update.message.from_user.username if update.message.from_user.username else 'not'}
"""
        )


    return LANGUAGE

async def admin() -> int:
    return ConversationHandler.END


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer("Progress...")

    messages = {
        'en': """*Hello*

📌 Please send your slide or abstract:
\\- *name*\\*, 
\\- *to whom it belongs* \\(University name, faculty name, department name, group and fullname\\),
\\- *size*\\* \\(how many sheets\\) and if any should be used 
\\- *send literature* \\(pdf, word or website\\) to help us\\.

\\* \\- must be filled in\\!""",

        'ru': """Привет

📌 Пожалуйста, пришлите слайд или аннотацию:
\\- *имя*\\*, 
\\- *кому он принадлежит* \\(название университета, название факультета, название кафедры, группа и ФИО\\),
\\- *размер*\\* \\(сколько листов\\) и следует ли их использовать 
\\- *присылайте литературу* \\(pdf, word или веб\\-сайт\\), чтобы помочь нам\\.

\\* \\- необходимо заполнить\\!""",

        'uz': """Assalomu alaykum

📌 Iltimos, slaydingiz yoki referatingizning:
\\- *nomini*\\*, 
\\- *kimga tegishli bo'lishi*\\( Universitet nomi, fakultet nomi, yo'nalish nomi, guruh va FIO\\)ni,
\\- *hajmi*\\*\\( necha varoqligi\\)ni va agar bo'lsa foydalanish kerak bo'lgan 
\\- *adabiyotlar*\\( pdf, word yoki internet sayti\\)ni bizga yordam bo'lishi uchun yuboring\\.

\\* \\- to'ldirilishi shart\\!"""
    }

    await query.edit_message_text(text=messages.get(query.data), parse_mode="MarkdownV2")

    context.user_data['language'] = query.data

    return INFORMATION


async def infos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return FINISH


async def cancel(update: Update, context: CallbackContext):
    messages = {
        'uz': 'Bekor qilindi!',
        'ru': 'Отменено!',
        'en': 'Cancelled!'
    }
    await update.message.reply_text(messages.get(context.user_data.get('language')))
    return ConversationHandler.END


async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    messages = {
        'uz': "Ma'lumotlaringiz adminga jo'natildi, tez orada javob yozamiz...",
        'ru': 'Ваша информация отправлена администратору, мы ответим в ближайшее время...',
        'en': 'Your information has been sent to admin, we will reply soon...'
    }
    await update.message.reply_text(messages.get(context.user_data.get('language')))
    return ConversationHandler.END


async def error_handler(update: Update, context: CallbackContext) -> int:
    await context.bot.send_message(chat_id=MY_CHAT_ID,
                                   text=f"Xatolik yuz berdi😢: \n\n{context.error}")
