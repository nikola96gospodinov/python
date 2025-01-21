try:
    number = int(input("Enter a number: "))
    result = 10 / number
except ValueError:
    print("Please enter a valid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
    
try:
    # Some risky code
    pass
except (ValueError, TypeError) as error:
    print(f"Error occurred: {error}")
    
try:
    # Some risky code
    pass
except Exception as error:
    print(f"An error occurred: {error}")
    
try:
    file = open("data.txt")
except FileNotFoundError:
    print("File not found")
else:
    # Runs if no exception occurred
    print("File opened successfully")
finally:
    # Always runs, regardless of exception
    file.close()
    
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    return age

class AgeError(Exception):
    pass

def verify_age(age):
    if age < 0:
        raise AgeError("Age cannot be negative")
    
def get_positive_number():
    while True:
        try:
            number = float(input("Enter a positive number: "))
            if number < 0:
                raise ValueError("Number must be positive")
            return number
        except ValueError as error:
            print(f"Error: {error}")

def read_config_file(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Config file {filename} not found")
        return None
    except PermissionError:
        print("No permission to read file")
        return None
    
def get_user_info(user_dict, key):
    try:
        return user_dict[key]
    except KeyError:
        return f"No {key} found for user"
