import sqlite3
from config import DB_NAME, TABLE_NAME


class DATABASE:
    def __init__(self):
        self.DB_NAME = DB_NAME
        self.TABLE_NAME = TABLE_NAME

    def execute_query(self, query, data=None):
        """
        Функция для выполнения запроса к базе данных.
        Принимает имя файла базы данных, SQL-запрос и опциональные данные для вставки.
        """
        try:
            connection = sqlite3.connect(self.DB_NAME)
            cursor = connection.cursor()

            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            cursor = cursor.fetchall()
            connection.commit()
            connection.close()
            return cursor

        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)

        finally:
            connection.close()

    def create_table(self):
        sql_query = f"""CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            token INTEGER
        );"""
        self.execute_query(sql_query)

    def add_data(self, user_id):

        sql_query = f'INSERT INTO {self.TABLE_NAME} (user_id, token) VALUES (?, 0);'
        data = (user_id,)

        self.execute_query(sql_query, data)

    def update_data(self, user_id, column, value):

        sql_query = f'UPDATE {self.TABLE_NAME} SET {column} = ? WHERE user_id = ?;'
        data = (value, user_id,)
        self.execute_query(sql_query, data)

    def get_data(self, column, user_id):
        sql_query = f'SELECT {column} FROM {self.TABLE_NAME} WHERE user_id = ?;'
        data = (user_id,)
        result = self.execute_query(sql_query, data)
        return result
