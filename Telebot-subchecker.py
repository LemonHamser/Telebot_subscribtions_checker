import os
import telebot
from telebot.apihelper import ApiTelegramException

bot = telebot.TeleBot(os.getenv("TOKEN"))
photo = open("XOWMtjt.png", 'rb')

CHAT_ID = -1001741609743

button_pikatchu = telebot.types.InlineKeyboardButton('Send a picture', callback_data='button_pressed')
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.add(button_pikatchu)

@bot.message_handler(commands=['start'])
def start(message):
    mess = f"Hello,<b>{message.from_user.first_name} <u>{message.from_user.last_name}!</u> </b>\n use this " \
           f"bot to check if you subscribed to speciffic telegram channel or not by /help "
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=keyboard)


def is_subscribed(CHAT_ID, user_id):
    try:
        bot.get_chat_member(CHAT_ID, user_id)
        return True
    except ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: user not found':
            return False

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data == 'button_pressed':
        if not is_subscribed(CHAT_ID, call.message.from_user.id):
            bot.send_message(call.message.chat.id, "please join @ai_drawing to continue",
                             parse_mode='html')
        else:
            bot.send_photo(call.message.chat.id,photo,"here you are" )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "/user_id to see your user id \n /group_id to check the id of group you reposted",
                     parse_mode='html')


@bot.message_handler(commands=['user_id'])
def get_user_id(message):
    bot.send_message(message.chat.id, message.from_user.id, parse_mode='html')


@bot.message_handler(commands=['group_id'])
def repost_waiting_state(repost_message):
    bot.send_message(repost_message.chat.id, "Please repost something")

    @bot.message_handler(content_types=['photo', 'text'])
    def get_group_id(message):
        if message.forward_from_chat is not None:
            bot.send_message(message.chat.id, f"Id of {message.forward_from_chat.type} is"
                                              f" {message.forward_from_chat.id}", parse_mode='html')
        else:
            if message.forward_from is not None:
                bot.send_message(message.chat.id, f"Id of bot is {message.forward_from.id}", parse_mode='html')
            else:
                bot.send_message(message.chat.id, f"Please send repost from channel, current message is {message}",
                                 parse_mode='html')


bot.polling(none_stop=True)
