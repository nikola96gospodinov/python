from typing import List
from datetime import datetime

class Employee:
    existing_ids: List[str] = []
    
    def __init__(self, name: str, id: str, base_salary: float | int) -> None:
        if name.strip() == "":
            raise ValueError("name cannot be empty")
        
        if id.strip() == "":
            raise ValueError("id cannot be empty")
        
        if id in Employee.existing_ids:
            raise ValueError("id already exists")
        
        if base_salary < 0:
            raise ValueError("salary needs to be a positive number")
        
        self.name = name
        self.id = id
        self.base_salary = base_salary
        Employee.existing_ids.append(id)
        
    def calculate_salary(self) -> float | int:
        return self.base_salary
    
    def get_info(self):
        return f"{self.name} has an ID of {self.id} and a base salary of {self.base_salary}"
    
class HourlyRateEmployee(Employee):
    def __init__(self, name: str, id: str, base_salary: float | int, hourly_rate: float | int, hours_worked: float | int) -> None:
        super().__init__(name, id, base_salary)
        
        if hourly_rate <= 0:
            raise ValueError("Hourly rate needs to be a positive number")
        
        if hours_worked < 0:
            raise ValueError("Hours worked must be a non negative number")
        
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
        
    def calculate_salary(self) -> float | int:
        return self.hourly_rate * self.hours_worked
    
    def add_extra_hours(self, extra_hours: int | float) -> bool:
        if extra_hours < 0:
            raise ValueError("Extra hours must be a non negative number")
        
        self.hours_worked += extra_hours
        return True
        
class CommissionEmployee(Employee):
    def __init__(self, name: str, id: str, base_salary: float | int, commission_rate: float | int, sales: int) -> None:
        super().__init__(name, id, base_salary)
        
        if commission_rate <= 0:
            raise ValueError("Commission rate needs to be a positive number")
        
        if sales < 0:
            raise ValueError("Sales must be a non negative integer")
        
        self.commission_rate = commission_rate
        self.sales = sales
        
    def calculate_salary(self) -> float | int:
        return self.base_salary + (self.commission_rate * self.sales)
    
    def add_sales(self, sales: int) -> bool:
        if sales <= 0:
            raise ValueError("Sales must be a positive integer")
        
        self.sales += sales
        return True

class Manager(Employee):
    def __init__(self, name: str, id: str, base_salary: float | int, bonus_percentage: float) -> None:
        super().__init__(name, id, base_salary)
        
        if bonus_percentage < 0:
            raise ValueError("Bonus percentage needs to be a non negative number")
        
        self.bonus_percentage = bonus_percentage
        
    def calculate_salary(self) -> float | int:
        bonus_multiplier = self.bonus_percentage / 100
        return self.base_salary * (1 + bonus_multiplier)
    
class MediaItem:
    def __init__(self, title: str, year: int, genre: str) -> None:
        if title.strip() == "":
            raise ValueError("Title must be a non empty string")
        
        current_year = datetime.now().year
            
        if year < 0 or year > current_year:
            raise ValueError(f"Year must be between 0 and {current_year}")
        
        if genre.strip() == "":
            raise ValueError("Genre must be a non empty string")
        
        self.title = title
        self.year = year
        self.genre = genre
        
    def display_info(self) -> str:
        return f"{self.title} is {self.genre} and is from {self.year}."
    
    def calculate_rental_cost(self) -> float:
        return 1
    
class Movie(MediaItem):
    def __init__(self, title: str, year: int, genre: str, director: str, duration_in_minutes: int) -> None:
        super().__init__(title, year, genre)
        
        if director.split() == "":
            raise ValueError("Director must be a non empty string")
        
        if duration_in_minutes <= 0:
            raise ValueError("Duration must be a positive integer")
        
        self.director = director
        self.duration_in_minutes = duration_in_minutes
        
    def display_info(self) -> str:
        base_info = super().display_info()
        return f"{base_info} The movie is by {self.director} and is {self.duration_in_minutes} minutes long"
    
    def calculate_rental_cost(self) -> float:
        return super().calculate_rental_cost() + (self.duration_in_minutes * 0.01)
    
class Book(MediaItem):
    def __init__(self, title: str, year: int, genre: str, author: str, num_pages: int) -> None:
        super().__init__(title, year, genre)
        
        if author.strip() == "":
            raise ValueError("Author must be a non empty string")
        
        if num_pages <= 0:
            raise ValueError("Number of pages must be a positive integer")
        
        self.author = author
        self.num_pages = num_pages
        
    def display_info(self) -> str:
        base_info = super().display_info()
        return f"{base_info} The book is written by {self.author} and it has {self.num_pages} pages."
    
    def calculate_rental_cost(self) -> float:
        return super().calculate_rental_cost() + (self.num_pages * 0.01)
    
class AudioBook(Book):
    def __init__(self, title: str, year: int, genre: str, author: str, num_pages: int, narrator: str, duration_in_hours: int) -> None:
        super().__init__(title, year, genre, author, num_pages)
        
        if narrator.strip() == "":
            raise ValueError("Narrator must be a non empty string")
        
        if duration_in_hours <= 0:
            raise ValueError("Duration must be a positive integer")
        
        self.narrator = narrator
        self.duration_in_hours = duration_in_hours
        
    def display_info(self) -> str:
        base_info = super().display_info()
        return f"{base_info} The audiobook is narrated by {self.narrator} and is {self.duration_in_hours} hours long."
    
    def calculate_rental_cost(self) -> float:
        return super().calculate_rental_cost() + (self.duration_in_hours * 0.25)