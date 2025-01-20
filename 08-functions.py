def greet(name):
    return f"Hello, {name}!"

print(greet("Nik"))

def calculate_total(price, quantity, tax=0.1):
    subtotal = price * quantity
    total = subtotal + (subtotal * tax)
    return total

print(calculate_total(20.5, 2, 0.2))
print(calculate_total(tax=0.3, price=3.35, quantity=2))

def add_numbers(a: int, b: int) -> int:
    return a + b

print(add_numbers(2, 3))

def get_user_info() -> tuple[str, int]:
    name = "John"
    age = 30
    return name, age

print(get_user_info())

def sum_numbers(*numbers):
    return sum(numbers)

print(sum_numbers(4, 5, 11))

def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")
        
print_info(name="Nik", age=28, city="London")