from datetime import datetime
from typing import List
from functools import cached_property
import time

# @staticmethod is useful when it belongs logically to a class but doesn't need instance data, performs utility functions related to the class and doesn't need access to self or cls
class DateValidator:
    @staticmethod
    def is_valid_date(year: int, month: int, day: int) -> bool:
        """Validate date without needing instance data"""
        if not (isinstance(year, int) and isinstance(month, int) and isinstance(day, int)):
            return False
        
        if month < 1 or month > 12:
            return False
        
        if day < 1 or day > 31:
            return False
        
        days_in_month = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        
        return day <= days_in_month[month]
    
    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Check if yeas is lead year - doesn't need instance data"""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
# Usage
print(DateValidator.is_valid_date(2023, 12, 25)) # True
print(DateValidator.is_valid_date(2023, 13, 1)) # False
print(DateValidator.is_leap_year(2024)) # True

# @classmethod is useful when you want to have alternative constructors
class Date:
    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day
        
    @classmethod
    def from_string(cls, date_string: str):
        """Create Date from string format YYYY-MM-DD"""
        year, month, day = map(int, date_string.split("-"))
        # cls(year, month, day) calls __init__ with those arguments
        # cls refers to the Date class, so this is equivalent to:
        # Date(year, month, day)
        return cls(year, month, day)
    
    @classmethod
    def today(cls):
        """Create Date from today"""
        today = datetime.now()
        return cls(today.year, today.month, today.day)
    
    @classmethod
    def from_timestamp(cls, timestamp: float):
        """Create Date from timestamp"""
        date = datetime.fromtimestamp(timestamp)
        return cls(date.year, date.month, date.day)

# Usage - different ways to create Date objects
date1 = Date(2023, 12, 25)                # Regular constructor
date2 = Date.from_string('2023-12-25')    # From string
date3 = Date.today()                      # Today's date
date4 = Date.from_timestamp(1703480400)   # From timestamp

class EuropeanDate(Date):
    @classmethod
    def from_string(cls, date_string: str):
        """Create Date from string format DD-MM-YYYY"""
        day, month, year = map(int, date_string.split("-"))
        return cls(year, month, day)
    
# Uses EuropeanDate class, not Date
euro_date = EuropeanDate.from_string('25-12-2023')

# @abstractmethod - used for defining interfaces, enforcing method implementation and creating base classes
from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def connect(self) -> bool:
        """Must implement connection logic"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Must implement disconnection logic"""
        pass
    
    @abstractmethod
    def fetch_data(self) -> List:
        """Must implement data fetching"""
        pass
    
    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Must implement connection status"""
        pass
    
class DatabaseSource(DataSource):
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connected = False
        
    def connect(self) -> bool:
        print(f"Connecting to database: {self._connection_string}")
        self._connected = True
        return True
    
    def disconnect(self) -> bool:
        self._connected = False
        return True
    
    def fetch_data(self) -> list:
        if not self.is_connected:
            raise ConnectionError("Not connected")
        return ["data1", "data2"]
    
    @property
    def is_connected(self) -> bool:
        return self._connected
    
# @cached_property - computing expensive results that won't change and are needed multiple times
class ReportGenerator:
    def __init__(self, data: list) -> None:
        self.data = data
        
    @cached_property
    def summary_statistics(self) -> dict:
        """Expensive computation - cached after the first call"""
        print("Computing summary statistics...")
        time.sleep(1) # Simulate expensive operation
        return {
            "mean": sum(self.data) / len(self.data),
            "max": max(self.data),
            "min": min(self.data)
        }
        
    @cached_property
    def sorted_data(self) -> list:
        """Expensive sorting - cached after first call"""
        print("Sorting data...")
        time.sleep(1)  # Simulate expensive computation
        return sorted(self.data)
    
report = ReportGenerator(["Nik", "Nikola"])
print(report.summary_statistics)
print(report.sorted_data)
# Clear the cached properties
del report.summary_statistics
del report.sorted_data
