from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import textwrap
import string
import random
from telegram import error
from timetable.models import Event

YOGURT_PIC = 'https://sun9-12.userapi.com/impg/fEQSeBvO45TUdnhRItU0IUPaiphVOjtqfSgCTg/M-lCbu0B5BA.jpg?size=960x1280&quality=96&sign=664e83d8ba3957f55ddb95c7c1e676b4&type=album'
REPLICAS = [
    """Ишь черт картавый, а как тебе такой???""",
    """Чево все такое это самое да? ЧЕВО ТЕБЕ НЕ НРАВИТСЯ ТО?""",
    """*агрессивно шипит*""",
    """Либо убираишь за мной гавно, либо больше не создаю пароли :-/"""
]


def generate_password():

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = '!#$%&()[]{};:+-./'
    password = ''.join(random.sample((lower + upper + num + symbols), 20))
    return password


def send_password_menu(update, context):

    text = textwrap.dedent(
        """
        Хехе, никому не выдам твои паролики! Только моей мами, если не покормишь йогуртом :)))
        """
    )

    keyboard = [
        [InlineKeyboardButton('Я хочу создать новый пароль', callback_data='password#new')],
        [InlineKeyboardButton('Помоги вспомнить пароль', callback_data='password#old_choice')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')


def send_create_password_send_site(update, context):

    text = textwrap.dedent(
        """Ну ладно, шалунишка, отправляй ссылку на сайт, щас разберемся"""
    )

    query = update.callback_query
    context.bot.edit_message_text(text=text, message_id=query.message.message_id, chat_id=query.message.chat_id)


def send_create_password_send_site_alias(update, context):

    text = textwrap.dedent(
        """Хаха на порнхабе сидишь, ржекич!!! Шутка, давай теперь придумаем, как будем называть этот сайт между друг другом :3"""
    )

    update.message.reply_text(text=text)


def send_create_password_generate_password(update, context):

    password = generate_password()
    context.user_data['create_password']['password'] = password

    text = textwrap.dedent(
        f"""
        Ладно, ладно, теперь самое интересненькое. Тебе нравится этот пароль? Если да, то готовь гречневовый йогурт!!!!!!!!
        """
    )
    keyboard = [
        [InlineKeyboardButton('Мне нравится этот пароль', callback_data='good_password')],
        [InlineKeyboardButton('Сгенерируй новый пароль', callback_data='bad_password')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')
    message_for_delete = update.message.reply_text(text=password, parse_mode='Markdown')

    context.user_data['message_for_delete'] = message_for_delete['message_id']
    context.user_data['regenerate_password_message'] = message_for_delete['message_id']


def send_create_password_good_password(update, context):

    text = textwrap.dedent(
        """Я рад што оказался тебе полезен, но все еще требую гречневовый йогурт!!!!"""
    )
    keyboard = [
        [InlineKeyboardButton('Покормить греческим йогуртом', callback_data='feed')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    context.bot.edit_message_text(text=text, reply_markup=reply_markup, message_id=query.message.message_id,chat_id=query.message.chat_id)


def send_create_password_regenerate_password(update, context):

    password = generate_password()
    context.user_data['create_password']['password'] = password

    text = random.choice(REPLICAS)

    keyboard = [
        [InlineKeyboardButton('Мне нравится этот пароль', callback_data='good_password')],
        [InlineKeyboardButton('Сгенерируй новый пароль', callback_data='bad_password')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    context.bot.edit_message_text(text=text, reply_markup=reply_markup, message_id=query.message.message_id, chat_id=query.message.chat_id)
    context.bot.edit_message_text(text=password, message_id=context.user_data['regenerate_password_message'], chat_id=query.message.chat_id)


def send_remember_password_by_choice(update, context):

    text = 'Ага, так ты забывашка! Ну лана, давай определимся, будем вспоминать пароль по ссылке или кликухе?'

    keyboard = [
        [InlineKeyboardButton('По ссылке', callback_data='password#old_site_url')],
        [InlineKeyboardButton('По кликухе', callback_data='password#old_site_alias')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    context.bot.edit_message_text(text=text, message_id=query.message.message_id, chat_id=query.message.chat_id, reply_markup=reply_markup, parse_mode='Markdown')


def send_remember_password_by_site(update, context):

    text = textwrap.dedent(
        """Мурр, мурр, отправляй ссылочку :3"""
    )

    query = update.callback_query
    context.bot.edit_message_text(text=text, message_id=query.message.message_id, chat_id=query.message.chat_id)


def send_remember_password_by_site_alias(update, context):

    text = textwrap.dedent(
        """
        Хехе, у нас есть локальные приколы :))
        Отправляй кликуху!
        """
    )

    query = update.callback_query
    context.bot.edit_message_text(text=text, message_id=query.message.message_id, chat_id=query.message.chat_id)


def send_remember_password_error(update, context):

    text = textwrap.dedent(
        """
        Я не нашел пароля, прасти, мне так жаль...
        Попробуешь еще разок?
        """
    )

    update.message.reply_text(text=text)


def send_remember_password_success(update, context, password):

    text = 'Хехе, есть такой!!! Не забудь меня покормить гречевским йогуртом!'

    keyboard = [
        [InlineKeyboardButton('Покормить греческим йогуртом', callback_data='feed')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text=text, reply_markup=reply_markup)

    message = update.message.reply_text(text=password.password)
    context.user_data['message_for_delete'] = message['message_id']


def feed_shkontik(update, context):

    query = update.callback_query
    try:
        if context.user_data.get('message_for_delete'):
            context.bot.delete_message(message_id=context.user_data['message_for_delete'], chat_id=query.message.chat_id)
            context.user_data['message_for_delete'] = None

        if context.user_data.get('event_to_delete'):
            context.user_data['event_to_delete'].delete()

        context.bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat_id)
    except error.BadRequest:
        pass
    finally:
        context.bot.send_photo(photo=YOGURT_PIC, chat_id=query.message.chat_id)
