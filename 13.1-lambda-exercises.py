from typing import TypedDict, List, Tuple, Literal
from datetime import datetime

class Student(TypedDict):
    name: str
    age: int
    grade: int

students: List[Student] = [
    {'name': 'John', 'age': 19, 'grade': 85},
    {'name': 'Emma', 'age': 22, 'grade': 91},
    {'name': 'Michael', 'age': 20, 'grade': 78},
    {'name': 'Sarah', 'age': 19, 'grade': 95},
    {'name': 'James', 'age': 21, 'grade': 89}
]

def sort_students(property: str) -> List[Student]:
    if property not in Student.__annotations__ or property.lower() != "length":
        print(f"Property '{property}' doesn't exist")
        return students
    
    if property.lower() == "length":
        sorted_students = sorted(students, key=lambda x: len(x["name"]))
        return sorted_students
    
    sorted_students = sorted(students, key=lambda x: x[property])  # type: ignore
    return sorted_students

def sort_strings(strings: List[str]) -> List[str]:
    sorted_strings = sorted(strings, key=lambda x: (x[-1], len(x)), reverse=True)
    return sorted_strings

Product = Tuple[str, float, int]

products: List[Product] = [
    ('Laptop', 899.99, 5),
    ('Smartphone', 499.99, 12),
    ('Headphones', 89.99, 20),
    ('Tablet', 299.99, 7),
    ('Mouse', 24.99, 30),
    ('Keyboard', 59.99, 15),
    ('Monitor', 249.99, 8),
    ('Printer', 199.99, 0),
    ('Speakers', 149.99, 10),
    ('Webcam', 79.99, 3),
    ('USB Drive', 19.99, 50),
    ('External HDD', 129.99, 0),
    ('Gaming Console', 399.99, 6),
    ('Router', 89.99, 25),
    ('Power Bank', 49.99, 18)
]

def process_products() -> List[str]:
    sorted_products = sorted(products, key=lambda x: x[1] * x[2], reverse=True)
    filtered_products = [product for product in sorted_products if product[1] * product[2] != 0]
    product_names = [product[0] for product in filtered_products]
    return product_names

def sorter(items: List) -> List:
    if not items:
        raise ValueError("Input list cannot be empty")
        
    try:
        sorted_items: List = sorted([item for item in items if isinstance(item, (int, float))])
        strings = sorted([item for item in items if isinstance(item, str)], key=str.lower)
        
        if not (sorted_items or strings):
            raise ValueError("List must contain at least one number or string")
            
        sorted_items.extend(strings)
        return sorted_items
        
    except TypeError as e:
        raise TypeError("All items must be numbers or strings") from e
    
Rating = Literal[1, 2, 3, 4, 5]
    
class Book(TypedDict):
    title: str
    author: str
    year: int
    rating: Rating
    price: float
    
books: List[Book] = []

# Look into Pydantic to simplify
def add_book(book: Book) -> bool:
    try:
        # Validate all string fields are non-empty
        for field in ['title', 'author']:
            if not isinstance(book[field], str) or not book[field].strip(): # type: ignore 
                raise ValueError(f"{field.capitalize()} must be a non-empty string")
        
        # Validate year
        current_year = datetime.now().year
        if not isinstance(book['year'], int) or book['year'] > current_year:
            raise ValueError(f"Year must be an integer not greater than {current_year}")
        
        # Rating is already constrained by the Literal type, but we can check at runtime
        if book['rating'] not in (1, 2, 3, 4, 5):
            raise ValueError("Rating must be between 1 and 5")
        
        # Validate price
        if not isinstance(book['price'], float) or book['price'] <= 0:
            raise ValueError("Price must be a positive float")

        books.append(book)  # Actually add the book if all validation passes
        return True
        
    except (KeyError, ValueError) as error:
        print(f"Validation error: {error}")
        return False
    except Exception as error:
        print(f"Unexpected error: {error}")
        return False

sample_books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925, "rating": 5, "price": 9.99},
    {"title": "1984", "author": "George Orwell", "year": 1949, "rating": 5, "price": 12.99},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "rating": 4, "price": 11.99},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813, "rating": 4, "price": 8.99},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951, "rating": 3, "price": 10.99}
]

for book in sample_books:
    add_book(book)  # type: ignore
    
def sort_books(criteria: int) -> List[Book]:
    if criteria not in (1, 2, 3, 4, 5, 6):
        print("Option not supported")
        return books    
    
    if criteria == 1:
        print("Sorted by title:")
        return sorted(books, key=lambda x: x["title"].lower())
    elif criteria == 2:
        print("Sorted by author")
        return sorted(books, key=lambda x: x["author"].lower())
    elif criteria == 3:
        print("Sorted by year")
        return sorted(books, key=lambda x: x["year"])
    elif criteria == 4:
        print("Sorted by rating (high to low)")
        return sorted(books, key=lambda x: x["rating"], reverse=True)
    elif criteria == 5:
        print("Sorted by price (low to high)")
        return sorted(books, key=lambda x: x["price"])
    elif criteria == 6:
        print("Sorted by price-to-rating ratio")
        return sorted(books, key=lambda x: x["price"] / x["rating"])
    
    return books
