import sqlite3
import sys
import os

DB_FILE_NAME: str = 'test.db'

def createDatabase():
    conn = sqlite3.connect(DB_FILE_NAME) # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    try:
        # Создание таблицы
        cursor.execute(
            """CREATE TABLE albums
                (title text, artist text, release_date text,
                publisher text, media_type text)
            """
        )

        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()

        print ('Error {}:'.format(e.args[0]))
        sys.exit(1)

# Поиск относительно .venv
existsDatabase: bool = os.path.exists(DB_FILE_NAME)

if (existsDatabase):
    os.remove(DB_FILE_NAME)
    createDatabase()
else:
    createDatabase()
    
# Работы с переменными идёт также, как и в springJdbc

# TODO - сделать по БД
# 1)Написать и протестить querybuilder - мб лучше использовать orm - https://habr.com/ru/post/207110/
# 2)Сделать скрипты создания бд с 0
# 3)Сделать таблицы для хранения данных