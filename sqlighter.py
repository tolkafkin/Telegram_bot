import curses
import sqlite3
import time


class SQLighter:
    def __init__(self, db):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        self.create_db()


    def create_db(self):
        """Вспомогательная функция для создания БД"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities(
        name TEXT,
        url TEXT,
        population TEXT
                        )""")
        self.connection.commit()
        

    def clear_date(self):
        """Удаление данных из таблицы каждый раз, когда бот запускается, для обновления данных""" 
        with self.connection:        
            self.cursor.execute("DELETE FROM cities")


    def put_date(self, data):
        """Функция, зполняющая таблицу данными из словаря после парсинга"""   
        with self.connection:
            for city in data.keys():
                self.cursor.execute("INSERT INTO cities (name, url, population) VALUES (?,?,?)", (city, data[city]['url'], data[city]['population']))


    def get_names(self, message_user):
        """Делаем запрос на основе сообщения от пользователя и возвращаем список подходящих вариантов"""
        with self.connection:
            result = self.cursor.execute("SELECT name FROM cities WHERE lower(name) LIKE lower('%' || ? || '%')", (str(message_user),)).fetchall()
        return result


    def get_data (self, name):
        """Из точного имени города делаем запрос на получение ссылки и количества населения"""
        with self.connection:
            result = self.cursor.execute("SELECT url, population FROM cities WHERE name=(?)", name).fetchone()
        return result


    # def close(self):
    #     '''Закрываем соединение с БД'''
    #     self.connection.close()



 