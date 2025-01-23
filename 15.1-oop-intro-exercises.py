from typing import TypedDict

class Book:
    count = 0
    
    def __init__(self, title, author, isbn, is_checked_out):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_checked_out = is_checked_out
        Book.count += 1
        
    def check_out(self):
        if self.is_checked_out:
            print("Book is already checked out. Please try again later")
        else:
            self.is_checked_out = True
            
    def return_book(self):
        if self.is_checked_out:
            self.is_checked_out = False
        else:
            print("Book cannot be returned if it's available")
            
    def get_book_info(self):
        print(f"{self.title} is by {self.author}. ISBN: {self.isbn}")
        
# Create some sample books
book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", False)
book2 = Book("To Kill a Mockingbird", "Harper Lee", "978-0446310789", False)
book3 = Book("1984", "George Orwell", "978-0451524935", False)
book4 = Book("Pride and Prejudice", "Jane Austen", "978-0141439518", False)

class BankAccount:
    interest_rate = 0.044
    
    def __init__(self, account_number: int, holder_name: str, balance: float | int) -> None:
        if not isinstance(account_number, int) or account_number < 0:
            raise ValueError("Account number must be a positive integer")
            
        if not isinstance(holder_name, str) or not holder_name.strip():
            raise ValueError("Holder name must be a non-empty string")
            
        if not isinstance(balance, (int, float)) or balance <= 0:
            raise ValueError("Balance must be a non-negative number")
            
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = float(balance)
        
    def deposit_money(self, amount: float | int):
        if not isinstance(amount, (float, int)) or amount < 0:
            raise ValueError("Amount must be a positive number")
        self.balance += amount
        
    def withdraw_money(self, amount: float | int):
        if not isinstance(amount, (float, int)) or amount < 0:
            raise ValueError("Amount must be a positive number")
        
        if amount > self.balance:
            print("You don't have enough money to perform this operation")
            return
        
        self.balance -= amount
        
    def apply_interest(self):
        self.balance = self.balance * 0.044
        
    def display_account_info(self):
        print(f"This account belongs to {self.holder_name} and has £{self.balance}.")
        
class Grade(TypedDict):
    subject: str
    grade: float
    
def validate_grade(grade: Grade):
    if not isinstance(grade, dict) or "subject" not in grade or "grade" not in grade:
        raise ValueError("Each grade must be a Grade object with subject and grade")
    
    if not 0 <= grade["grade"] <= 100:
        raise ValueError("Grade must be between 0 and 100")

class Student:
    def __init__(self, student_id: int, name: str, grades: list[Grade] = []):
        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("student_id must be a positive number")
        
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("name must be a non empty string")
            
        for grade in grades:
            validate_grade(grade)
            
        self.student_id = student_id
        self.name = name
        self.grades = grades
        
    def add_grade(self, grade: Grade):
        validate_grade(grade)
        self.grades.append(grade)
        
    def calculate_average(self) -> float:
        if not self.grades:
            return 0.0
        return sum([grade["grade"] for grade in self.grades]) / len(self.grades)
    
    def get_highest_grade(self) -> float | None:
        if not self.grades:
            print("No grades at the moment")
        return max([grade["grade"] for grade in self.grades])
    
    def get_lowest_grade(self) -> float | None:
        if not self.grades:
            print("No grades at the moment")
        return min([grade["grade"] for grade in self.grades])
        
class Product:
    total_products: int = 0
    total_value: float = 0
    
    def __init__(self, name: str, price: float | int, quantity: int, category: str) -> None:
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("name must be a non empty string")
        
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("price must be a positive number")
        
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("quantity must be a non-negative integer")
        
        if not isinstance(category, str) or category.strip() == "":
            raise ValueError("category must be a non-empty string")
        
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        
        Product.total_products += 1
        Product.total_value += price * quantity
        
    def restock_product(self, quantity: int):
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("quantity must be a non-negative integer")
        
        self.quantity += quantity
        Product.total_value += quantity * self.price
        
    def sell_product(self):
        if self.quantity == 0:
            print("Out of stock")
            return
        
        self.quantity -= 1
        Product.total_value -= self.price
        
    def apply_discount(self, discount: float):
        if not isinstance(discount, (int, float)) or not 0 < discount < 100:
            raise ValueError("discount must be a percentage between 0 and 100 (exclusive)")
        
        discount_value = discount / 100
        new_price = (1 - discount_value) * self.price
        value_difference = (self.price * self.quantity) - (new_price * self.quantity)
        
        self.price = new_price
        Product.total_value -= value_difference