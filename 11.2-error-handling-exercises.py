from typing import List, TypedDict, Any
import re

class AgeError(Exception):
    pass

def get_age():
    while True:
        try:
            age_input = int(input("Enter your age "))
            if (0 <= age_input <= 120):
                break
            
            raise AgeError
        except ValueError:
            print("Enter a number")
        except AgeError:
            print("Age must be between 0 and 120")
        except Exception as error:
            print(f"Unexpected error: {error}")
            
    return age_input

VALID_OPERATIONS = {
    "plus": "+",
    "minus": "-",
    "multiply": "*",
    "divide": "/"
}

class InvalidOperationError(Exception):
    pass

results: List = []

def get_float() -> float:
    while True:
        try:
            float_input = float(input("Enter a number "))
            break
        except ValueError:
            print("Value needs to be a number (e.g 2, -5, 12.1)")
    
    return float_input

def calculator():
    while True:
        try:
            operation_input = input(f"Choose an operation {VALID_OPERATIONS.values()} ")
            
            if operation_input not in VALID_OPERATIONS.values():
                raise InvalidOperationError(f"It needs to be one of: {VALID_OPERATIONS.values()}")
            
            first_number = get_float()
            second_number = get_float()
            
            if operation_input == VALID_OPERATIONS['plus']:
                result = first_number + second_number
                results.append(result)
                print(f"Result is: {result}")
                
            if operation_input == VALID_OPERATIONS["minus"]:
                result = first_number - second_number
                results.append(result)
                print(f"Result is: {result}")
                
            if operation_input == VALID_OPERATIONS["multiply"]:
                result = first_number * second_number
                results.append(result)
                print(f"Result is: {result}")
                
            if operation_input == VALID_OPERATIONS['divide']:
                result = first_number / second_number
                results.append(result)
                print(f"Result is: {result}")
            
        except InvalidOperationError as error:
            print(error)
        except ZeroDivisionError as error:
            print(error)
        except Exception as error:
            print(f"Unexpected error: {error}")
        
items = ["apple", "orange", "kiwi", "pineapple", "mango"]

class NonPositiveIntError(Exception):
    pass

def get_positive_int(exit_word="quit") -> int | None:
    while True:
        user_input = input(f"Enter a number (or {exit_word.lower()} to exit) ")
        
        if user_input.lower() == exit_word.lower():
            return None
            
        try:
            int_input = int(user_input)
            
            if int_input < 0:
                raise NonPositiveIntError("Value needs to be a positive number")
            
            break
        except ValueError:
            print("Value needs to be a number (e.g 2, 19)")
        except NonPositiveIntError as error:
            print(error)
    
    return int_input

def get_item_by_index():
    while True:
        index = get_positive_int()
        
        if index is None:
            print("Exiting program...")
            break
            
        try:
            item = items[index]
            print(f"The item for index {index} is {item}")
        except IndexError:
            print(f"Index {index} doesn't exist")
        except Exception as error:
            print(f"Unexpected error: {error}")
            
class User(TypedDict):
    name: str
    age: int
    email: str
    
class ContainsNumbersError(Exception):
    pass

class EmailError(Exception):
    pass

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_user(user: User) -> bool:
    try:
        for letter in user["name"]:
            if isinstance(letter, int):
                raise ContainsNumbersError("Name shouldn't include numbers")
            
        if not isinstance(user["age"], int):
            raise ValueError("Age must be a whole number")
        
        if not re.match(email_pattern, user["email"]):
            raise EmailError("This is not a valid email")
    except ContainsNumbersError as error:
        print(error)
        return False
    except ValueError as error:
        print(error)
        return False
    except EmailError as error:
        print(error)
        return False
    
    return True

def convert_to_floats(list: List) -> tuple[List[float], List[Any]]:
    successful_converts: List[float] = []
    failed_converts: List = []
    
    for item in list:
        try:
            converted_item = float(item)
            successful_converts.append(converted_item)
        except ValueError:
            failed_converts.append(item)
        except Exception as error:
            print(f"Unexpected error: {error}")
            failed_converts.append(item)
    
    return (successful_converts, failed_converts)