import re
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class Temperature:
    def __init__(self, celsius=0) -> None:
        self._celsius = 0
        
        self.celsius = celsius
        
    @property
    def celsius(self):
        """Get current celsius"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """Set celsius with validation"""
        if not isinstance(value, (int, float)):
            raise TypeError("Must be a number")
        if value < -273.15:
            raise ValueError("Must be above -273.15°C")
        
        self._celsius = value
        
    @property
    def fahrenheit(self):
        """Get current fahrenheit"""
        return self._celsius * (9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set fahrenheit"""
        self.celsius = (value - 32) * (5/9)
        
    @property
    def kelvin(self):
        """Get current kelvin"""
        return self._celsius + 273.15
    
    @kelvin.setter
    def kelvin(self, value):
        """Set kelvin"""
        self.celsius = value - 273.15
        
        
class Product:
    def __init__(self, name, price, quantity):
        self._name = ""
        self._price = 0
        self._quantity = 0
        
        self.name = name
        self.price = price
        self.quantity = quantity
        
    @property
    def name(self):
        """Get current name"""
        return self._name
    
    @name.setter
    def name(self, value):
        """Set the name"""
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if value.strip() == "":
            raise ValueError("Name cannot be an empty string")
        
        self._name = value
        
    @property
    def price(self):
        """Get current price"""
        return self._price
    
    @price.setter
    def price(self, value):
        """Set the price"""
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value <= 0:
            raise ValueError("Price must be positive")
        
        self._price = value
        
    @property
    def quantity(self):
        """Get current quantity"""
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        """Set the quantity"""
        if not isinstance(value, (int, float)):
            raise TypeError("Quantity must be a number")
        if value <= 0:
            raise ValueError("Quantity must be positive")
        
        self._quantity = value
        
    @property
    def total_value(self):
        """Get the total value"""
        return self._quantity * self._price
    
    def restock(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a number")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        self.quantity += amount
        
    def sell(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a number")
        if amount <= 0  or amount > self.quantity:
            raise ValueError(f"Amount must be between 0 and {self.quantity}")
        
        self.quantity -= amount
        
        
class EmailAccount:
    def __init__(self, email):
        self._email = ""
        self._password = ""
        
        self.email = email
        
    @property
    def email(self):
        """Get email"""
        return self._email
    
    @email.setter
    def email(self, value):
        """Set email"""
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(value, email_pattern):
            raise ValueError("Please enter a valid email")
        
        self._email = value
        
    @property
    def username(self):
        """Get the username"""
        return self._email.split("@")[0]
    
    @property
    def domain(self):
        """Get the domain"""
        return self._email.split("@")[1]
    
    @property
    def password(self):
        """Password is write-only"""
        raise AttributeError("Password cannot be read, only set")
    
    @password.setter
    def password(self, value):
        """Set password"""
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(char.isalnum() for char in value):
            raise ValueError("Password must contain at least one number")
        if not any(char.isalpha for char in value):
            raise ValueError("Password must contain at least one letter")
        
        self._password = value