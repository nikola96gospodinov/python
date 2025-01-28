from abc import ABC, abstractmethod
from typing import List

# SOLID

# S - Single Responsibility Principle
# Bad: Class doing way too many things
class BadUser:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        
    def validate_email(self):
        # Email validation logic
        pass
    
    def save_to_database(self):
        # Database operations
        pass
    
    def send_welcome_email(self):
        # Email sending logic
        pass
    
    def generate_report(self):
        # Report generation
        pass
    
# Good: Split into focused classes
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        
class UserValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        # Only handles email validation
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format")
        return True
    
class UserRepository:
    def save(self, user: User) -> None:
        # Only handles database operations
        print(f"Saving user {user.name} to database")
        
    def get(self, email: str):
        # Only handles database retrieval
        pass
    
    def delete(self, email: str):
        # Only handles database deletion
        pass
    
class EmailService:
    def send_welcome_email(self, user: User) -> None:
        # Only handles email sending
        print(f"Sending welcome email to {user.email}")
        
    def send_confirmation_email(self, user: User) -> None:
        print(f"Sending confirmation email to {user.email}")
        
class ReportGenerator:
    def generate_user_report(Self, user: User) -> str:
        # Only handles report generation
        return f"Report for user {user.name}"
    
# Usage
def register_new_user(name: str, email: str):
    try:
        # Each class has a single responsibility
        validator = UserValidator()
        validator.validate_email(email)
        
        user = User(name, email)
        
        repository = UserRepository()
        repository.save(user)
        
        email_service = EmailService()
        email_service.send_welcome_email(user)
        
        return user
    except (TypeError, ValueError) as error:
        print(f"Registration failed: {error}")
        return None
    
# Example usage
user = register_new_user("John Doe", "john@example.com")

# O - Open/Closed Principle
# Bad example - constantly modifying class to add new types
class BadPaymentProcessor:
    def process_payment(self, payment_type: str, amount: float) -> bool:
        if payment_type == "credit_card":
            print(f"Processing ${amount} via Credit Card")
            return True
        elif payment_type == "paypal":
            print(f"Processing ${amount} via PayPal")
            return True
        elif payment_type == "bitcoin":  # Need to modify existing code to add new type
            print(f"Processing ${amount} via Bitcoin")
            return True
        return False
    
# Good example - extended through inheritance/interfaces
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Process the payment"""
        pass
    
    @property
    @abstractmethod
    def payment_type(self) -> str:
        """Get payment type"""
        pass
    
class CreditCardProcessor(PaymentProcessor):
    @property
    def payment_type(self) -> str:
        return "Credit Card"
    
    def process_payment(self, amount: float) -> bool:
        print(f"Processing ${amount} via Credit Card")
        return True
    
class PayPalProcessor(PaymentProcessor):
    @property
    def payment_type(self) -> str:
        return "PayPal"
    
    def process_payment(self, amount: float) -> bool:
        print(f"Processing ${amount} via PayPal")
        return True
    
class BitcoinProcessor(PaymentProcessor):  # Add new processor without modifying existing code
    @property
    def payment_type(self) -> str:
        return "Bitcoin"
    
    def process_payment(self, amount: float) -> bool:
        print(f"Processing ${amount} via Bitcoin")
        return True
    
class PaymentServices:
    def __init__(self) -> None:
        self._processors: List[PaymentProcessor] = []
        
    def add_processor(self, processor: PaymentProcessor) -> None:
        if not isinstance(processor, PaymentProcessor):
            raise TypeError("Must be a PaymentProcessor")
        self._processors.append(processor)
        
    def process_payment(self, payment_type: str, amount: float) -> bool:
        for processor in self._processors:
            if processor.payment_type == payment_type:
                return processor.process_payment(amount)
        raise ValueError(f"No processor found for {payment_type}")
    
# Usage
service = PaymentServices()
service.add_processor(CreditCardProcessor())
service.add_processor(PayPalProcessor())
service.add_processor(BitcoinProcessor())

# Process payments
service.process_payment("Credit Card", 100.00)
service.process_payment("PayPal", 50.00)
service.process_payment("Bitcoin", 75.00)

# Add new payment type without modifying existing code
class ApplePayProcessor(PaymentProcessor):
    @property
    def payment_type(self) -> str:
        return "Apple Pay"
    
    def process_payment(self, amount: float) -> bool:
        print(f"Processing ${amount} via Apple Pay")
        return True
    
# Just add the new processor
service.add_processor(ApplePayProcessor())
service.process_payment("Apple Pay", 200.00)

# L - Liskov Substitution Principle
# Bad example - an object of the superclass cannot be replaced with and object of some of the subclasses
class BadBird:
    def fly(self):
        return "Flying high!"

class BadDuck(BadBird):
    def fly(self):
        return "Duck flying!"

class BadPenguin(BadBird):  # Violates LSP
    def fly(self):
        raise NotImplementedError("Penguins can't fly!")  # Breaks substitution
    
# Good example - any subclass can substitute the superclass
class Bird:
    def move(self):
        """All birds can move somehow"""
        pass

class FlyingBird(Bird):
    def move(self):
        return "Flying in the air"
    
    def fly(self):
        return "Flying high!"

class SwimmingBird(Bird):
    def move(self):
        return "Swimming in the water"
    
    def swim(self):
        return "Swimming along!"
    
class Duck(FlyingBird, SwimmingBird):
    def move(self):
        return "Walking or swimming"
    
    def fly(self):
        return "Duck flying"
    
    def swim(self):
        return "Duck swimming"
    
class Penguin(SwimmingBird):
    def move(self):
        return "Swimming"
    
    def swim(self):
        return "Penguin is swimming"
    
# Usage example that works with any Bird
def make_bird_move(bird: Bird):
    return bird.move()

duck = Duck()
penguin = Penguin()
print(make_bird_move(duck))
print(make_bird_move(penguin))

# I - Interface Segregation Principle
# Bad example - classes shouldn't be forced to implement methods they don't use
class BadWorker(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass
    
    @abstractmethod
    def sleep(self):
        pass
    
    @abstractmethod
    def code(self):
        pass
    
    @abstractmethod
    def test(self):
        pass
    
class BadRobot(BadWorker):  # Robots don't eat or sleep!
    def work(self):
        return "Working..."
    
    def eat(self):
        raise NotImplementedError
    
    def sleep(self):
        raise NotImplementedError
    
    def code(self):
        return "Coding..."
    
    def test(self):
        return "Testing..."
    
class Worker(ABC):
    @abstractmethod
    def work(self):
        pass
    
class NeedsRest(ABC):
    @abstractmethod
    def eat(self):
        pass
    
    @abstractmethod
    def sleep(self):
        pass
    
class Programmable(ABC):
    @abstractmethod
    def code(self):
        pass

class Testable(ABC):
    @abstractmethod
    def test(self):
        pass
    
# Now classes can implement only what they need
class Human(Worker, NeedsRest):
    def work(self):
        return "Working..."
    
    def eat(self):
        return "Eating..."
    
    def sleep(self):
        return "Sleeping..."
    
class Robot(Worker, Programmable, Testable):
    def work(self):
        return "Working efficiently..."
    
    def code(self):
        return "Coding bug-free..."
    
    def test(self):
        return "Testing thoroughly..."
    
# D - Dependency Inversion Principle
# Bad example - high level modules should not depend on low level modules - they should depend on abstractions and abstractions should not depend on details, but details should depend on abstractions
class BadMySQLDatabase:
    def save(self, data: dict):
        print(f"Saving {data} to MySQL database")
        
class BadUserService:
    def __init__(self):
        # Directly depends on concrete MySQLDatabase
        self.database = BadMySQLDatabase()  # Tightly coupled!
        
    def save_user(self, user_data: dict):
        self.database.save(user_data)
        
# Good example - depends on abstractions
class Database(ABC):
    @abstractmethod
    def save(self, data: dict):
        pass
    
    @abstractmethod
    def delete(self, id: int):
        pass
    
    @abstractmethod
    def update(self, id: int, data: dict):
        pass
    
class MySQLDatabase(Database):
    def save(self, data: dict):
        print(f"Saving {data} to MySQL database")
    
    def delete(self, id: int):
        print(f"Deleting id {id} from MySQL database")
    
    def update(self, id: int, data: dict):
        print(f"Updating id {id} with {data} in MySQL database")
        
class PostgresDatabase(Database):
    def save(self, data: dict):
        print(f"Saving {data} to Postgres database")
    
    def delete(self, id: int):
        print(f"Deleting id {id} from Postgres database")
    
    def update(self, id: int, data: dict):
        print(f"Updating id {id} with {data} in Postgres database")
        
class UserService:
    def __init__(self, database: Database):  # Depends on abstraction
        self.database = database
    
    def save_user(self, user_data: dict):
        self.database.save(user_data)
    
    def delete_user(self, user_id: int):
        self.database.delete(user_id)
        
# Usage
mysql_db = MySQLDatabase()
postgres_db = PostgresDatabase()

# Can use either database implementation
user_service_mysql = UserService(mysql_db)
user_service_postgres = UserService(postgres_db)
