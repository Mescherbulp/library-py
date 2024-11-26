import json
from typing import List, Dict, Union

# Путь к JSON файлу
DATA_FILE = 'library.json'

# Структура книги
class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

# Чтение данных из JSON
def load_data() -> List[Dict]:
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Если файл отсутствует, возвращаем пустой список
    except json.JSONDecodeError:
        print("Ошибка чтения JSON файла.")
        return []

# Сохранение данных в JSON
def save_data(data: List[Dict]) -> None:
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Функция для генерации уникального ID
def generate_id(data: List[Dict]) -> int:
    if not data:
        return 1
    return max(book["id"] for book in data) + 1

# Основное меню
def main_menu():
    print("\nДобро пожаловать в систему управления библиотекой!")
    print("1. Добавить книгу")
    print("2. Удалить книгу")
    print("3. Найти книгу")
    print("4. Показать все книги")
    print("5. Изменить статус книги")
    print("0. Выход")


# Добавление книги

def add_book():
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    try:
        year = int(input("Введите год издания: "))
    except ValueError:
        print("Год издания должен быть числом.")
        return

    books = load_data()
    book_id = generate_id(books)
    new_book = Book(book_id, title, author, year)
    books.append(new_book.to_dict())
    save_data(books)
    print(f"Книга '{title}' успешно добавлена!")


# Удаление книги
def delete_book():
    try:
        book_id = int(input("Введите ID книги для удаления: "))
    except ValueError:
        print("ID должен быть числом.")
        return

    books = load_data()
    updated_books = [book for book in books if book["id"] != book_id]
    if len(books) == len(updated_books):
        print("Книга с указанным ID не найдена.")
    else:
        save_data(updated_books)
        print("Книга успешно удалена.")

# Реализация поиска

def search_book():
    print("\nВыберите критерий поиска:")
    print("1. Название")
    print("2. Автор")
    print("3. Год издания")

    choice = input("Введите номер критерия: ")
    query = input("Введите значение для поиска: ").strip()

    books = load_data()

    if choice == "1":
        results = [book for book in books if query.lower() in book["title"].lower()]
    elif choice == "2":
        results = [book for book in books if query.lower() in book["author"].lower()]
    elif choice == "3":
        try:
            query = int(query)
            results = [book for book in books if book["year"] == query]
        except ValueError:
            print("Год издания должен быть числом.")
            return
    else:
        print("Некорректный выбор.")
        return

    if results:
        print("\nНайденные книги:")
        for book in results:
            print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                  f"Год: {book['year']}, Статус: {book['status']}")
    else:
        print("Книги не найдены.")

# Отображение всех книг

def display_books():
    books = load_data()
    if not books:
        print("Библиотека пуста.")
        return

    print("\nСписок всех книг:")
    for book in books:
        print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
              f"Год: {book['year']}, Статус: {book['status']}")

# Изменение статуса

def change_status():
    try:
        book_id = int(input("Введите ID книги для изменения статуса: "))
    except ValueError:
        print("ID должен быть числом.")
        return

    books = load_data()
    for book in books:
        if book["id"] == book_id:
            print(f"Текущий статус книги: {book['status']}")
            new_status = input("Введите новый статус (в наличии/выдана): ").strip().lower()

            if new_status in ["в наличии", "выдана"]:
                book["status"] = new_status
                save_data(books)
                print(f"Статус книги '{book['title']}' успешно изменен на '{new_status}'.")
                return
            else:
                print("Некорректный статус.")
                return

    print("Книга с указанным ID не найдена.")

# функционал меню

if __name__ == "__main__":
    while True:
        main_menu()
        choice = input("\nВыберите действие: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            delete_book()
        elif choice == "3":
            search_book()
        elif choice == "4":
            display_books()
        elif choice == "5":
            change_status()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор, попробуйте снова.")
