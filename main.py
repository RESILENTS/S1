from  config import *
from  keyboard import *

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.from_user.id
    username = message.from_user.username
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS user(username TEXT, user_id INTEGER);""")
        cur.execute("SELECT * FROM user WHERE `user_id` = '{}'".format(chat_id))
        row = cur.fetchall()
        if len(row) == 0:
            cur.execute("INSERT INTO `user` (`username`, `user_id`) VALUES(?,?)",
                        (username, chat_id,))
    bot.send_message(chat_id, f'Добро пожаловать!', reply_markup=main_keyboard())

@bot.message_handler(commands=['admin'])
def admin(message):
    chat_id = message.from_user.id
    if chat_id in admins:
        bot.send_message(chat_id, '🛠️ Добро пожаловать в Админ панель.', reply_markup=admin_keyboard())


@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.from_user.id

bot.polling()
