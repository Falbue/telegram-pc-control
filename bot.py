from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot import types
import telebot
import config
import os


BOT_API = config.API
ID_ADMIN = config.ADMIN
DIR = script_directory = os.path.dirname(os.path.abspath(__file__))

bot = telebot.TeleBot(BOT_API)


# кнопки
btn_menu_music = InlineKeyboardButton(text="Мультимедиа", callback_data="munu_music")
btn_music_back = InlineKeyboardButton(text="⬅️", callback_data="music_back")
btn_music_pause = InlineKeyboardButton(text="⏯️", callback_data="music_pause")
btn_music_next = InlineKeyboardButton(text="➡️", callback_data="music_next")
btn_back_main = InlineKeyboardButton(text="< Назад", callback_data="back_main")

btn_shutdown = InlineKeyboardButton(text="Выключить", callback_data="shutdown")


# клавиатуры
keyboard_main = InlineKeyboardMarkup(row_width=2)
keyboard_main.add(btn_menu_music)
keyboard_main.add(btn_shutdown)

keyboard_music = InlineKeyboardMarkup(row_width=3)
keyboard_music.add(btn_music_back, btn_music_pause, btn_music_next, btn_back_main)


# КОМАНДЫ
@bot.message_handler(commands=['start'])  # обработка команды start
def start(message):
    if message.chat.id == ID_ADMIN:
        with open(f'{DIR}/config.py', 'w') as f:
            f.write(f"API = '{config.API}'\n")
            f.write(f"ADMIN = {config.ADMIN}\n")
            f.write(f"MESSAGE = {message.message_id+1}\n")
        bot.send_message(message.chat.id, text="Выбрите действие", reply_markup=keyboard_main)
    else:
        bot.send_message(call.message.chat.id, "У вас нет прав для использования этого бота.")
    bot.delete_message(message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "shutdown":
        bot.edit_message_text(chat_id=user_id, message_id=message_id, text="Выключение...")
        os.system("shutdown /s /t 1")  # Команда для выключения Windows
        bot.edit_message_text(chat_id=user_id, message_id=message_id, text="Компьютер выключен")


    if call.data == "munu_music":
        bot.edit_message_text(chat_id=ID_ADMIN, message_id=config.MESSAGE, text="Управление мультимедиа", reply_markup=keyboard_music)


    if call.data == 'music_next':
        os.system('powershell -command "(New-Object -ComObject wscript.shell).SendKeys([char]176)"')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Следующий трек ")

    if call.data == 'music_pause':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Пауза не работает")

    if call.data == 'music_back':
        os.system('powershell -command "(New-Object -ComObject wscript.shell).SendKeys([char]177)"')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Предыдущий трек")


    if call.data == 'back_main':
        bot.edit_message_text(chat_id=ID_ADMIN, message_id=config.MESSAGE, text="Выбрите действие", reply_markup=keyboard_main)



            

try:
    bot.edit_message_text(chat_id=ID_ADMIN, message_id=config.MESSAGE, text="Выбрите действие", reply_markup=keyboard_main)
except:
    pass
bot.polling(none_stop=True)


