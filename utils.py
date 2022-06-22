import shelve
import logging

from telebot import types
from random import shuffle
from SQLighter import MusicManager, UserManager
from bot_config import database_name, shelve_name


logger = logging.getLogger('utils_module')


def count_rows():
    db = MusicManager(database_name)
    rows_num = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rows_num


def get_rows_count():
    with shelve.open(shelve_name) as storage:
        rows_num = storage['rows_count']
    return rows_num


def set_user_game(user_id, estimated_answer):
    with shelve.open(shelve_name) as storage:
        storage[str(user_id)] = estimated_answer
        storage[f'player - {user_id}'] = user_id


def finish_user_game(chat_id, user_id):
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]
        del storage[f'player - {user_id}']


def get_answer_for_user(chat_id, user_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        except KeyError:
            return None


def generate_markup(right_answer, wrong_answers):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, selective=True)
    all_answers = '{},{}'.format(right_answer, wrong_answers)
    list_items = []

    for item in all_answers.split(','):
        list_items.append(item)

    shuffle(list_items)

    for item in list_items:
        markup.add(item)
    return markup


# --------------------------------------------------------
def init_user(user_id, first_name):
    db = UserManager(database_name)
    db.init_user(user_id, first_name)


def set_user_win(user_id):
    db = UserManager(database_name)
    db.insert_win(user_id)


def set_user_loose(user_id):
    db = UserManager(database_name)
    db.insert_loose(user_id)
