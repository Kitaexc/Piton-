from Bdata import hash_password

def add_user(cursor, conn):
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    role = input("Введите роль (Пользователь/Администратор): ")
    # Здесь должна быть обработка и хэширование пароля
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
    conn.commit()
    print("Пользователь добавлен.")

def delete_user(cursor, conn):
    username = input("Введите имя пользователя для удаления: ")
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    print("Пользователь удален.")

def change_user_role(cursor, conn):
    username = input("Введите имя пользователя: ")
    new_role = input("Введите новую роль: ")
    cursor.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
    conn.commit()
    print("Роль пользователя изменена.")

def add_book_or_comic(table, cursor, conn):
    title = input("Введите название: ")
    author = input("Введите автора: ")
    publication = int(input("Введите год публикации: "))
    type_ = input("Введите тип (book/comic): ")
    cursor.execute(f"INSERT INTO {table} (title, author, publication, type) VALUES (?, ?, ?, ?)", (title, author, publication, type_))
    conn.commit()
    print("Данные добавлены.")

def delete_book_or_comic(table,cursor, conn):
    title = input("Введите название для удаления: ")
    cursor.execute(f"DELETE FROM {table} WHERE title = ?", (title,))
    conn.commit()
    print("Данные удалены.")

def admin_functionality():
    while True:
        print("\n1. Добавить пользователя\n2. Удалить пользователя\n3. Изменить роль пользователя\n4. Добавить книгу/комикс\n5. Удалить книгу/комикс\n6. Выход")
        choice = input("Выберите действие: ")
        if choice == "1":
            add_user()
        elif choice == "2":
            delete_user()
        elif choice == "3":
            change_user_role()
        elif choice in ["4", "5"]:
            table = 'books' if input("Выберите тип (1 - Книга, 2 - Комикс): ") == "1" else 'komic'
            if choice == "4":
                add_book_or_comic(table)
            else:
                delete_book_or_comic(table)
        elif choice == "6":
            break
        else:
            print("Неверный выбор.")
