import telebot
import random
import utils
import cherrypy
import os

from SQLighter import MusicManager, UserManager
from telebot import types
from os import listdir
from time import sleep

token = os.environ.get('token')
bot = telebot.TeleBot(token)

database_name = os.getenv('database_name')
shelve_name = os.getenv('shelve_name')


@bot.message_handler(commands=['json'])
def message_get(message):
    bot.send_message(message.from_user.id, message)


@bot.message_handler(commands=['stats'])
def get_stats(message):
    connect = UserManager(database_name)
    cursor = connect.cursor
    wins = cursor.execute('''SELECT win_count, loose_count FROM users WHERE user_id = ?''',
                          (message.from_user.id,)).fetchall()[0]
    print(wins, type(wins))
    bot.send_message(message.from_user.id, f'Вы угадали мелодию {wins[0]} раз :)\nИ обосрались {wins[1]} раз  ;)')
    connect.close()


@bot.message_handler(commands=['start'])
def init_user(message):
    utils.init_user(message.from_user.id, message.from_user.first_name)


@bot.message_handler(commands=['game'])
def game(message):
    db_worker = MusicManager(database_name)
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    markup = utils.generate_markup(row[2], row[3])
    # row[1] -> file_id
    bot.send_voice(message.from_user.id, row[1], reply_markup=markup, duration=20,
                   reply_to_message_id=message.message_id)
    utils.set_user_game(message.from_user.id, row[2])
    db_worker.close()


@bot.message_handler(commands=['test'])
def find_file_ids(message):
    for file in listdir('music/'):
        if file.split('.')[-1] == 'ogg':
            f = open('music/' + file, 'rb')
            res = bot.send_voice(message.from_user.id, f, None)
            bot.send_message(message.from_user.id, res.voice.file_id, reply_to_message_id=res.message_id)
            print(res.voice)
        sleep(2)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # print(message)
    answer = utils.get_answer_for_user(message.from_user.id, message.from_user.id)

    if not answer:
        bot.send_message(message.from_user.id, 'Чтобы начать игру, выберите команду /game')
    else:
        keyboard_hider = types.ReplyKeyboardRemove()
        if message.text == answer:
            bot.send_message(message.from_user.id, 'Верно!', reply_markup=keyboard_hider)
            utils.set_user_win(message.from_user.id)
        else:
            bot.send_message(message.from_user.id,
                             'Увы, Вы не угадали. Попробуйте ещё раз {}!'.format(message.chat.username),
                             reply_markup=keyboard_hider)
            utils.set_user_loose(message.from_user.id)

        utils.finish_user_game(message.from_user.id, message.from_user.id)


utils.count_rows()
random.seed()
bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}},)
