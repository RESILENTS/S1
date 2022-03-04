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
    text = '<b>SORGENY</b> — Я помогу тебе получить скрытую информацию с разных интернет ресурсов.\n\nУ меня есть база данных слитых хайдов с разных интернет площадок. Более подробнее о боте вы сможете узнать в разделе информация.'
    img = open ('welc.webp', 'rb')
    bot.send_photo(chat_id, img, caption=text, reply_markup=main_keyboard(), parse_mode='html')

@bot.message_handler(commands=['admin'])
def admin(message):
    chat_id = message.from_user.id
    if chat_id in admins:
        bot.send_message(chat_id, '🛠️ Добро пожаловать в Админ панель.', reply_markup=admin_keyboard())


@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.from_user.id
    if message.text == '📥 Получить хайд':
        inline = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        btn = types.KeyboardButton(text='⭐IQOS 2.4+⭐')
        btn2 = types.KeyboardButton(text='🌟IQOS 3 DUO🌟')
        btn3 = types.KeyboardButton(text='🔥IQOS 3 Multi🔥')
        btn4 = types.KeyboardButton(text='🔙 Назад')
        btn5 = types.KeyboardButton(text='🔝 Главное Меню')
        inline.add(btn, btn2)
        inline.add(btn3)
        inline.add(btn4, btn5)
        bot.send_message(chat_id, '✨IQOS✨', reply_markup=inline)
    elif message.text == 'Рассылка' and chat_id in admins:
        message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *сообщение* для рассылки', parse_mode="Markdown")
        bot.register_next_step_handler(message, add_message)
    elif message.text == 'Кол-во пользователей' and chat_id in admins:
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM user")
            row = cur.fetchall()
            bot.send_message(message.from_user.id, 'Количество пользователей: ' + str(len(row)))
    elif message.text == 'Список всех пользователей' and chat_id in admins:
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * from `user`")
            row = cur.fetchall()
            w_file = open("users.csv", mode="w", encoding='utf-8')
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            for rows in row:
                file_writer.writerow(rows)
            w_file.close()
            with open(curdir + "/users.csv", "r") as file:
                bot.send_document(chat_id, file)

bot.polling()
