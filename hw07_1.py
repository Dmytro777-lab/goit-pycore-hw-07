from datetime import datetime
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name  # Виклик сеттера для перевірки

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if value:  # Перевірка, що ім'я не порожнє
            self._name = value
        else:
            raise ValueError("The name cannot be empty")

class Phone(Field):
    def __init__(self, phone_number: str):
        self._phone_number = None  # Тимчасове значення, щоб пройшла перша перевірка
        self.phone_number = phone_number  # Виклик сеттера для перевірки номера

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: str):
        if value.isdigit() and len(value) == 10:  # Перевірка, що номер складається з 10 цифр
            self._phone_number = value
        else:
            raise ValueError("The phone number must contain only 10 digits")
        
class Birthday(Field):
    def __init__(self, value):
        try:
           self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")   

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []  # Список для зберігання об'єктів Phone
        self.birthday = None  # За замовчуванням відсутня день народження
    
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)  # Створюємо об'єкт Birthday з перевіркою формату
    
    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)  # Використовуємо клас Phone для створення об'єкта
        self.phones.append(phone)  # Додаємо створений об'єкт до списку

    def remove_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.phone_number == phone_number:  # Порівнюємо номери
                self.phones.remove(phone)  # Видаляємо об'єкт Phone зі списку
                return
        raise ValueError("Phone not found")  # Якщо телефон не знайдено
    
    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        for phone in self.phones:
            if phone.phone_number == old_phone_number:  # Порівнюємо старий номер
                phone.phone_number = new_phone_number  # Змінюємо номер на новий
                return
        raise ValueError("Old phone not found")  # Якщо старий номер не знайдено
    
    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.phone_number == phone_number:  # Порівнюємо номер
                return phone  # Повертаємо знайдений об'єкт Phone
        raise ValueError("Phone not found")  # Якщо номер не знайдено
    
    def __str__(self):
        phones = '; '.join(p.phone_number for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.name}, phones: {phones}{birthday_str}"

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record):
        self.data[record.name.name] = record  # Використовуємо ім'я контакту як ключ

    def find(self, name: str):
        for record in self.data.values():  # Перебираємо всі записи
            if record.name.name.lower() == name.lower():  
                return record  # Повертаємо знайдений запис
        raise ValueError("Contact not found")  

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
    from datetime import timedelta

    def upcoming_birthdays(self, days=7):
        today = datetime.now().date()
        upcoming_contacts = []

        for record in self.data.values():
            if record.birthday:
                # Обновляем день рождения на текущий год для сравнения
                birthday_this_year = record.birthday.value.replace(year=today.year)
                delta = (birthday_this_year - today).days

                # Если день рождения в ближайшие дни
                if 0 <= delta <= days:
                    upcoming_contacts.append(record)
                elif delta < 0 and abs(delta) <= days:
                    upcoming_contacts.append(record)
        if upcoming_contacts:
            return upcoming_contacts
        return "No upcoming birthdays."
    
    def input_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                return str(e)
            except IndexError:
                return "Not enough arguments."
        return wrapper

    @input_error
    def add_birthday(self, args):
        name = args[0]
        birthday_date = args[1]
        record = self.find(name)
        if not record:
            return f"Contact {name} not found."
        record.add_birthday(birthday_date)
        return f"Birthday for {name} added."

    @input_error
    def show_birthday( self, args):
        name = args[0]
        record = self.find(name)  # Знайти контакт
        if record and record.birthday:
            return f"Birthday for {name} - {record.birthday.value.strftime('%d.%m.%Y')}."
        return f"No birthday for {name}."

    @input_error
    def birthdays(self):
        upcoming = self.upcoming_birthdays()
        if not upcoming:
            return "No birthdays in the coming week."
        return "\n".join(f"{record.name.name} - {record.birthday.value.strftime('%d.%m.%Y')}" for record in upcoming) 
    
    def add_contact(self, name: str, phone_number: str):
        if name in self.data:
            raise ValueError("Contact already exists")
        record = Record(name)
        record.add_phone(phone_number)
        self.add_record(record)
        return f"Contact {name} with phone {phone_number} added."

    def edit_phone(self, name: str, old_phone: str, new_phone: str):
        record = self.find(name)
        if record:
            record.edit_phone(old_phone, new_phone)
            return f"Phone for {name} changed from {old_phone} to {new_phone}."
        else:
            raise ValueError("Contact not found")

    def find_phone(self, phone_number: str):
        for record in self.data.values():
            if any(phone.phone_number == phone_number for phone in record.phones):
                return record
        raise ValueError("Phone number not found")

    def all_contacts(self):
        return "\n".join(str(record) for record in self.data.values())
    
def main():
    def parse_input(user_input):
        return user_input.strip().split()
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            print("Please enter a command.")
            continue
        command, *args = parse_input(user_input)
        
        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        
        elif command == "add":
            print(book.add_contact(args[0], args[1]))

        elif command == "change":
            print(book.edit_phone(args[0], args[1], args[2]))

        elif command == "phone":
            print(book.find_phone(args[0]))

        elif command == "all":
            print(book.all_contacts())

        elif command == "add-birthday":
            print(book.add_birthday(args))

        elif command == "show-birthday":
            print(book.show_birthday(args))

        elif command == "birthdays":
            print(book.birthdays(args))

        else:
            print("Invalid command.")

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
if __name__ == "__main__":
        main()
