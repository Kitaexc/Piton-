import sqlite3
import stdiomask
import Admin_funks
import User_funks



# Подключение к базе данных (или ее создание, если она не существует)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы для хранения данных пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY, 
        password TEXT, 
        role TEXT DEFAULT 'Пользователь'
    )
''')

# Добавление изначального пользователя-администратора
cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'Администратор')")
conn.commit()

def register():
    username = input("Введите имя пользователя для регистрации: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("Пользователь с таким именем уже существует.")
        return
    password = stdiomask.getpass(mask='*')
    
    # Укажите роль пользователя. Если роль не задана, используйте 'Пользователь' по умолчанию.
    role = "Пользователь"  # Или добавьте запрос у пользователя для ввода роли

    # Вставка пользователя с ролью
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    print("Пользователь успешно зарегистрирован.")

def login():
    username = input("Введите имя пользователя: ")
    password = stdiomask.getpass(mask='*')
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        print("Авторизация успешна.")
        if user[2] == 'Администратор':
            admin_functionality()
        else:
            user_functionality()
    else:
        print("Неверное имя пользователя или пароль.")

def admin_functionality():
    Admin_funks.admin_functionality(cursor, conn)

def user_functionality():
    User_funks.user_functionality(cursor, conn)

def main():
    while True:
        print("\n1. Регистрация\n2. Авторизация\n3. Выход")
        choice = input("Выберите действие (1-3): ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Неверный выбор, попробуйте еще раз.")

if __name__ == "__main__":
    main()
    conn.close()
