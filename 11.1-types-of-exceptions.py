# ValueError - Wrong type of value
try:
    number = int("hello") # Can't convert string to int
except ValueError as error:
    print(f"ValueError: {error}")
    
# TypeError - Wrong type operation
try:
    result = "hello" + 5 # Can't add string and int
except TypeError as error:
    print(f"TypeError: {error}")
    
# IndexError - List index out of range
try:
    list = [1, 2, 3]
    print(list[10]) # Index doesn't exist
except IndexError as error:
    print(f"IndexError: {error}")
    
# KeyError - Dictionary key not found
try:
    dict = {"name": "Nik"}
    print(dict["age"]) # Key doesn't exist
except KeyError as error:
    print(f"KeyError: {error}")
    
# FileNotFoundError - File doesn't exist
try:
    file = open("nonexistent.txt")
except FileNotFoundError as error:
    print(f"FileNotFoundError: {error}")
    
# ZeroDivisionError - Division by zero
try:
    result = 10 / 0
except ZeroDivisionError as error:
    print(f"ZeroDivisionError: {error}")
    
# AttributeError - Object has no attribute/method
try:
    number = 42
    number.append(1) # int has no append method
except AttributeError as error:
    print(f"AttributeError: {error}")
    
# NameError - Variable no defined
try:
    print(undefined_variable)
except NameError as error:
    print(f"NameError: {error}")
    
# SyntaxError - Invalid Python syntax
# Note: SyntaxError cannot be caught, code won't run
# if age > 18    # Missing colon

# IndentationError - Incorrect indentation
# Note: Also can't be caught, code won't run
# def function():
# print("wrong indentation")

# Combining different exceptions
def safe_operation():
    try:
        number = int(input("Enter number: "))
        result = 10 / number
        list = [1, 2, 3]
        print(list[result])
    except ValueError:
        print("Please enter a valid number")
    except ZeroDivisionError:
        print("Cannot divide by 0")
    except IndexError:
        print("Index doesn't exist")
    except Exception as error:
        print(f"Unexpected error: {error}")
        
# Using get() to avoid KeyError
user = {"name": "John"}
age = user.get("age", 0)  # Returns 0 if age not found