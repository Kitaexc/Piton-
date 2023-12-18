def borrow_book(user_id, cursor, conn):
    book_title = input("Введите название книги, которую хотите взять: ")
    cursor.execute("SELECT id FROM books WHERE title = ?", (book_title,))
    book = cursor.fetchone()
    if book:
        cursor.execute("INSERT INTO borrowed_books (user_id, book_id) VALUES (?, ?)", (user_id, book[0]))
        conn.commit()
        print("Книга успешно взята.")
    else:
        print("Книга не найдена.")
        
def return_book(user_id, cursor, conn):
    book_title = input("Введите название книги, которую хотите вернуть: ")
    cursor.execute("SELECT id FROM books WHERE title = ?", (book_title,))
    book = cursor.fetchone()
    if book:
        cursor.execute("DELETE FROM borrowed_books WHERE user_id = ? AND book_id = ?", (user_id, book[0]))
        conn.commit()
        print("Книга успешно возвращена.")
    else:
        print("Книга не найдена.")

def user_functionality(cursor, conn):
    while True:
        print("\n1. Взять книгу\n2. Вернуть книгу\n3. Выход")
        choice = input("Выберите действие: ")
        if choice == "1":
            # Вызов функции borrow_book с передачей cursor и conn
            borrow_book(cursor, conn)
        elif choice == "2":
            # Вызов функции return_book с передачей cursor и conn
            return_book(cursor, conn)
        elif choice == "3":
            break
        else:
            print("Неверный выбор.")

