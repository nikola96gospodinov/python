from typing import Callable

def greet(name: str) -> str:
    return f"Hello, {name}"

my_function = greet
print(my_function("Nik")) # Hello Nik

def my_decorator(func: Callable) -> Callable:
    def wrapper() -> None:
        print("Something happens before")
        func()
        print("Something happens after")
    return wrapper

@my_decorator
def say_hello():
    print("Hello")
    
# This is the same as writing:
# say_hello = my_decorator(say_hello)

say_hello()
# Something happens before
# Hello!
# Something happens after

def decorator_with_args(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@decorator_with_args
def add(a, b):
    return a + b

print(add(3, 5))
# Output:
# Before function call
# After function call
# 8

def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet_someone(name: str) -> None:
    print(f"Hello, {name}")
    
greet_someone("Bob")
# Output:
# Hello, Bob
# Hello, Bob
# Hello, Bob

# Use cases

# Timing
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done!"

# result = slow_function()
# print(result)

# Logging
def log_function(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_function
def calculate_something(x, y):
    return x + y

# calculation_result = calculate_something(2, 12)
# print(calculation_result)

# Input validation
def validate_inputs(func):
    def wrapper(*args, **kwargs):
        if any(arg <= 0 for arg in args):
            raise ValueError("Arguments must be positive")
        return func(*args, **kwargs)
    return wrapper

@validate_inputs
def calculate_rectangle_area(length, width):
    return length * width