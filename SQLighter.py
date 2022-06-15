import sqlite3


class BaseManager:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()


class MusicManager(BaseManager):

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('''SELECT * FROM music''').fetchall()

    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('''SELECT * FROM music WHERE id = ?''', (rownum,)).fetchall()[0]

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('''SELECT * FROM music''').fetchall()
            return len(result)


class UserManager(BaseManager):

    def init_user(self, user_id, first_name):
        with self.connection:
            self.cursor.execute('''INSERT OR IGNORE INTO users(user_id, first_name) VALUES (?,?);''',
                                (user_id, first_name))

    def insert_win(self, user_id):
        with self.connection:
            self.cursor.execute('''UPDATE users SET win_count = win_count + 1 WHERE user_id = ?''',
                                (user_id,))

    def insert_loose(self, user_id):
        with self.connection:
            self.cursor.execute('''UPDATE users SET loose_count = loose_count + 1 WHERE user_id = ?''',
                                (user_id,))
