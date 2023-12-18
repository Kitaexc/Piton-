import sqlite3
import hashlib
import os
from getpass import getpass

# Функция для создания хеша пароля
def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)  # 32 байта соли
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + pwdhash

# Функция для проверки пароля
def check_password(stored_password, provided_password):
    salt = stored_password[:32]  # Получаем соль
    stored_password = stored_password[32:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return pwdhash == stored_password

# Подключение к базе данных SQLite и создание таблиц
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Создание таблицы пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT
        )
    ''')

    # Создание таблицы книг
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publication INTEGER NOT NULL,
            type TEXT NOT NULL
        )
    ''')

    # Создание таблицы комиксов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS komic (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publication INTEGER NOT NULL,
            type TEXT NOT NULL
        )
    ''')

    # Данные для таблицы книг
    books_data = [
        ('Лолита', 'Владимир Набоков', 1955, 'book'),
        ('Распад', 'Чинуа Ачебе', 1958, 'book'),
        ('Великий Гэтсби', 'Фрэнсис Скотт Фитцджеральд', 1925, 'book'),
        ('Война и мир', 'Лев Толстой', 1869, 'book'),
        ('Улисс', 'Джеймс Джойс', 1922, 'book'),
        ('Шум и ярость', 'Уильям Фолкнер', 1929, 'book'),
        ('Невидимка', 'Ральф Эллисон', 1952, 'book'),
        ('К маяку', 'Вирджиния Вульф', 1927, 'book'),
        ('Миддлмарч', 'Джордж Элиот', 1874, 'book'),
        ('Сто лет одиночества', 'Габриэль Гарсия Маркес', 1967, 'book')
    ]

    # Данные для таблицы комиксов
    komic_data = [
        ('Kravenʼs Last Hunt', 'Джей Эм ДеМеттьес', 1987, 'comic'),
        ('Flashpoint', 'Джефф Джонс', 2011, 'comic'),
        ('Berserk', 'Кэнтаро Миура', 1989, 'comic'),
        ('The Sandman', 'Нил Гейман', 1989, 'comic'),
        ('Daredevil: Born Again', 'Фрэнк Миллер', 1986, 'comic'),
        ('Sex Criminals', 'Мэтт Фрэкшн', 2013, 'comic'),
        ('Gotham City Sirens', 'Пол Дини, Тони Бедард и Питер Каллоуэй', 2009, 'comic'),
        ('X-Factor Vol.3', 'Питер Дэвид', 2006, 'comic'),
        ('Batman: The Killing Joke', 'Алан Мур', 1988, 'comic'),
        ('Building Stories', 'Крис Уэйр', 2012, 'comic')        
    ]
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowed_books (
            user_id INTEGER,
            book_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')

    
    # Вставляем данные в таблицы
    cursor.executemany('INSERT INTO books (title, author, publication, type) VALUES (?, ?, ?, ?)', books_data)
    cursor.executemany('INSERT INTO komic (title, author, publication, type) VALUES (?, ?, ?, ?)', komic_data)

    conn.commit()
    conn.close()

# Инициализация базы данных
setup_database()
