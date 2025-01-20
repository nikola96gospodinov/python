from typing import TypedDict, List, Literal, Generator

# def add(a: float | int, b: float | int) -> float | int:
#     return a + b

# def subtract(a: float | int, b: float | int) -> float | int:
#     return a - b

# def multiply(*numbers: float | int) -> float | int:
#     total: int | float = 1
#     for number in numbers:
#         total = total * number
#     return total
#     # return math.prod(numbers)

# def divide(a: float | int, b: float | int) -> float | int:
#     return a / b

# # Define valid operations as a tuple of strings for type checking
# VALID_OPERATIONS = ("add", "subtract", "multiply", "divide")

# def validate_operation(operation: str) -> str:
#     if operation.lower() not in VALID_OPERATIONS:
#         raise ValueError(f"Operation must be one of: {VALID_OPERATIONS}")
#     return operation.lower()

# def get_valid_operation() -> str:
#     while True:
#         operation_input = input("Enter an operation (Add, Subtract, Multiply, Divide) ")
#         try:
#             return validate_operation(operation_input)
#         except ValueError as e:
#             print(e)


# def calculator(operation: str, *numbers: int | float) -> int | float:
#     if operation == "add":
#         return add(*numbers)
#     if operation == "subtract":
#         return subtract(*numbers)
#     if operation == "multiply":
#         return multiply(*numbers)
#     return divide(*numbers)

# operation_input = get_valid_operation()

# numbers: List = []
# while len(numbers) < 2:
#     try:
#         number_input = int(input("Enter a number "))
#         numbers.append(number_input)
#     except ValueError:
#         pass

# print(calculator(operation_input, *numbers))

# users: List = []

# def create_user(name, age, **additional_info):
#     user = {
#         "name": name,
#         "age": age,
#         **additional_info  # This is Python's equivalent to JavaScript's spread operator (...)
#     }
#     users.append(user)
#     return user

# def find_user(username):
#     user = next((user for user in users if user["username"] == username), None)
#     return user
    
# def update_user(username, **additional_info):
#     user = find_user(username)
    
#     if user:
#         user.update(additional_info)
#         return True
#     return False

# def delete_user(username):
#     user = find_user(username)
    
#     if user:
#         users.remove(user)
#         return True
#     return False

# def list_users(sort_by="name"):
#     sorted_list = sorted(users, key=lambda user: user[sort_by])
#     return sorted_list

# Priority = Literal["low", "medium", "high"]
# VALID_PRIORITIES = ("low", "medium", "high")

# class Task(TypedDict):
#     title: str
#     priority: Priority
#     is_done: bool
#     task_id: int

# tasks: List[Task] = []

# def validate_priority(priority: str) -> Priority:
#     match priority.lower():
#         case "low": return "low"
#         case "medium": return "medium"
#         case "high": return "high"
#         case _: raise ValueError(f"Priority must be one of: {VALID_PRIORITIES}")
        
# def get_id() -> Generator[int]:
#     current_id = 0
#     while True:
#         current_id += 1
#         yield current_id

# def add_task(title, priority="medium", is_done=False, **details):
#     task = {
#         "title": title,
#         "priority": validate_priority(priority),
#         "is_done": is_done,
#         "task_id": get_id(),
#         **details
#     }
    
#     tasks.append(task)
#     return task

# def find_task(task_id: int) -> Task | None:
#     task = next((task for task in tasks if task["task_id"] == task_id), None)
#     return task

# def complete_task(task_id: int) -> bool:
#     task = find_task(task_id)
    
#     if task:
#         task["is_done"] == True
#         return True
#     return False

# Status = Literal["all", "pending", "completed"]
# VALID_STATUSES = ("all", "pending", "completed")

# def validate_status(status: str) -> Status:
#     match status.lower():
#         case "all": return "all"
#         case "pending": return "pending"
#         case "completed": return "completed"
#         case _: raise ValueError(f"Status must be one of {VALID_STATUSES}")

# def list_tasks(status="all") -> List[Task]:
#     validated_status = validate_status(status)
    
#     match validated_status:
#         case "all": return tasks
#         case "pending": return [task for task in tasks if task["is_done"] == False]
#         case "completed": return [task for task in tasks if task["is_done"] == True]
        
# def search_tasks(*keywords: str) -> List[Task]:
#     found_tasks: List[Task] = []
#     for keyword in keywords:
#         keyword_found_tasks = [task for task in tasks if keyword.lower() in task["title"].lower()]
#         for found_task in keyword_found_tasks:
#             if found_task not in found_tasks:
#                 found_tasks.append(found_task)
    
#     return found_tasks

items: List = []

class Item(TypedDict):
    name: str
    quantity: int
    price: float
    

def add_item(item: Item):
    items.append(item)
    
def find_item(item_name: str) -> Item | None:
    found_item = next((item for item in items if item["name"] == item_name), None)
    return found_item
    
def update_stock(item_name: str, quantity: int) -> bool:
    found_item = find_item(item_name)
    
    if found_item:
        found_item["quantity"] = quantity
        return True
    return False

def get_total_inventory_value() -> float:
    return sum([item["price"] * item["quantity"] for item in items])

def list_low_stock(threshold=5) -> List[Item]:
    return [item for item in items if item["quantity"] <= threshold]

def process_sale(*processing_items: Item) -> bool:
    for item in processing_items:
        found_item = find_item(item["name"])
        
        if not found_item:
            return False
            
        if found_item["quantity"] < item["quantity"]:
            return False
            
        found_item["quantity"] = found_item["quantity"] - item["quantity"]
        
        if found_item["quantity"] == 0:
            items.remove(found_item)
    
    return True