from typing import List

amount_of_numbers = int(input("How many numbers do you need "))
numbers: List[int] = []

for i in range(0, amount_of_numbers):
    number_input = int(input("Enter a number "))
    numbers.append(number_input)
    
biggest_number = max(numbers)
smallest_number = min(numbers)
average_number = sum(numbers) / len(numbers)

numbers_above_average = 0
for i in range(0, amount_of_numbers):
    if numbers[i] > average_number:
        numbers_above_average += 1
        
print(f"Biggest number is: {biggest_number}")
print(f"Smallest number is: {smallest_number}")
print(f"Average is: {average_number}")
print(f"There are {numbers_above_average} numbers above average")

items: List[str] = []

while True:
    print("1. Add item")
    print("2. Remove item")
    print("3. Show list")
    print("4. Clear list")
    print("5. Exit")
    
    try:
        action = int(input("Choose an action: "))
    except ValueError:
        action = 0
    while action not in [1, 2, 3, 4, 5]:
       try:
           action = int(input("Please pick a number between 1 and 5 "))
       except ValueError:
           action = 0
        
        
    if action == 1:
        added_item = input("Add an item: ")
        items.append(added_item)
        print(f"{added_item} successfully added")
        
    elif action == 2:
        while True:
            removed_item = input("Remove an item: ")
            if removed_item.lower() == "back":
                break
            elif removed_item == "3":
                print(f"Items: {items}")
            elif removed_item in items:
                items.remove(removed_item)
                print(f"{removed_item} successfully removed")
                break
            else:
                print("Item not found in list")
            
    elif action == 3:
        print(f"Items: {items}")
        
    elif action == 4:
        items.clear()
        
    elif action == 5:
        break

name_input = input("Enter a name or say 'Done' if you've entered enough ")
names: List[str] = []

while name_input.lower() != 'done':
    names.append(name_input)
    name_input = input("Enter a name or say 'Done' if you've entered enough ")
    
print(f"Original order: {names}")
print(f"Alphabetical order: {sorted(names, key=str.lower)}")
print(f"Reverse alphabetical order: {sorted(names, reverse=True)}")
print(f"By length {sorted(names, key=len)}")

mixed_numbers = [-3, 10, 102, -23, 11]
positive_numbers: List[int] = []
negative_numbers: List[int] = []
even_numbers: List[int] = []

for i in mixed_numbers:
    if i > 0:
        positive_numbers.append(i)
    else:
        negative_numbers.append(i)
        
    if i % 2 == 0:
        even_numbers.append(i)
        
print(f"Positive numbers: {positive_numbers}")
print(f"Negative numbers: {negative_numbers}")
print(f"Even numbers: {even_numbers}")

todos: List = []

todo_name = ""

while True:
    print("1. Add task")
    print("2. View tasks")
    print("3. Mark tasks as complete")
    print("4. View completed tasks")
    print("5. View pending tasks")
    print("6. Exit")
    
    while True:
        try:
            action = int(input("Enter action (1-6) "))
            if action in [1, 2, 3, 4, 5, 6]:
                break
        except ValueError:
            # pass is a placeholder statement that does nothing
            # it's used when we need a statement syntactically but have no code to execute
            pass
            
    if action == 1:
        todo_name = input("What todo do you want to add? ")
        
        todo_priority = input("What is the priority? High/Medium/Low ")
        while todo_priority.lower() not in ["high", "medium", "low"]:
            todo_priority = input("Select a priority out of high, medium and low ")

        todos.append({
            "name": todo_name,
            "priority": todo_priority,
            "is_done": False
        })
    
    if action == 2:
        print(f"Todos: {todos}")
        
    if action == 3:
        while True:
            todo_name = input("Which todo do you want to complete? ")
            for todo in todos:
                if todo["name"] == todo_name:
                    todo["is_done"] = True
                    print(f"Marked '{todo_name}' as complete!")
                    break
            else:
                print("Todo not found. Try again.")
                continue
            break
        
    if action == 4:
        completed_todos = [todo for todo in todos if todo["is_done"] == True]
        print(f"Completed todos: {completed_todos}")
        
    if action == 5:
        pending_todos = [todo for todo in todos if todo["is_done"] == False]
        print(f"Pending todos: {pending_todos}")
        
    if action == 6:
        break