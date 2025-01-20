from typing import List, Dict, Union
import re

contacts: List = []
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

while True:
    print("1. Add contact (name, phone, email)")
    print("2. View all contacts")
    print("3. Search for contacts")
    print("4. Update contact")
    print("5. Delete contact")
    print("6. Exit")
    
    while True:
        try:
            action = int(input("Choose an action (1 to 6) "))
            if action in [1, 2, 3, 4, 5, 6]:
                break
        except ValueError:
            pass
    
    if action == 1:
        name = input("Enter a name ")
        while not name.strip():
            name = input("Name cannot be empty. Please enter a name ")
            
        while True:
            try:
                phone = int(input("Enter a valid phone number "))
                break
            except ValueError:
                pass
            
        email = input("Enter an email ")
        while not re.match(email_pattern, email):
            email = input("Please enter a valid email address (e.g. example@domain.com) ")
            
        contacts.append({
            "name": name,
            "phone": phone,
            "email": email
        }) 
        
    if action == 2:
        print(contacts)
        
    if action == 3:        
        while True:
            search = input("Search for contact (type 'back' to go back to the menu) ")
            if search == 'back':
                break
                
            found_contact = next((contact for contact in contacts if contact["name"] == search), None)
            if found_contact:
                print(found_contact)
                break
            
            print("Contact not found. Please try again or type 'back'")
            
    if action == 4:
        while True:
            search = input("Which contact do you want to change (type 'back' to go back to the menu) ")
            if search == 'back':
                break
            
            found_contact = next((contact for contact in contacts if contact["name"] == search), None)
            if found_contact:
                print("What do you want to change?")
                print("1. Name")
                print("2. Phone")
                print("3. Email")
                
                while True:
                    try:
                        update_action = int(input("Choose action "))
                        if update_action in [1, 2, 3]:
                            break
                    except ValueError:
                        pass
                    
                contact_index = contacts.index(found_contact)
                
                if update_action == 1:
                    new_name_value = input("Enter a new name ")
                    found_contact["name"] = new_name_value
                    
                    contacts[contact_index] = found_contact
                    print("Contact updated successfully")
                    break
                
                if update_action == 2:
                    try:
                        new_phone_value = int(input("Enter a new phone number "))
                    except:
                        pass
                    
                    found_contact["phone"] = new_phone_value
                    
                    contacts[contact_index] = found_contact
                    print("Contact updated successfully")
                    break
                
                if update_action == 3:
                    new_email_value = input("Enter a new email ")
                    while not re.match(email_pattern, email):
                        new_email_value = input("Please enter a valid email address (e.g. example@domain.com) ")
                        
                    found_contact["email"] = new_email_value
                    
                    contacts[contact_index] = found_contact
                    print("Contact updated successfully")
                    break
                        
                break
            
            print("Contact not found. Please try again or type 'back'")
       
    if action == 5:
        while True:
            name = input("Which contact do you want to delete (type 'back' to go back to the menu) ")
            
            if name.lower() == 'back':
                break
            
            found_contact = next((contact for contact in contacts if contact["name"] == name), None)
            if found_contact:
                contacts.remove(found_contact)
                print("Contact successfully removed")
                break
            
            print("Contact not found")
            
    if action == 6:
        break
            
students: List = []

while True:
    print("1. Enter student grades")
    print("2. Calculate grades per student")
    print("3. View class average")
    print("4. Exit")
    
    try:
        action = int(input("Select action "))
        if action not in [1, 2, 3]:
            action = 0
    except ValueError:
        action = 0
    
    if action == 1:
        name_input = input("Enter a student name ")
        
        existing_student: Dict | None = next((student for student in students if student["name"] == name_input), None)
        
        if existing_student:
            existing_student_index = students.index(existing_student)
            
        student: Dict[str, Union[str, int]] = {}  # Type hint for mixed string/int values
        student["name"] = name_input
        
        while True:
            subject_input = input("Enter a subject (or type 'quit' to exit) ").lower()
            
            if subject_input == 'quit':
                break
            
            try:
                grade_input = int(input("Enter a grade (0 to 100) "))
                if 0 <= grade_input <= 100:
                    if existing_student:
                        students[existing_student_index][subject_input] = grade_input
                    else:
                        student[subject_input] = grade_input
            except ValueError:
                pass
                
                
            if not existing_student:
                students.append(student)
            
            
    if action == 2:
        while True:
            name_input = input("Enter a student name (or type 'back') ")
        
            if name_input == "back":
                break
            
            found_student: Dict | None = next((student for student in students if student["name"] == name_input), None)
            if found_student is None:
                continue
            
            found_student_items = list(found_student.items()) if found_student else []
            grade_items = [(subject, grade) for subject, grade in found_student_items if subject != "name"]
            top_grade_item = max(grade_items, key=lambda x: x[1]) if grade_items else None
            if top_grade_item:
                print(f"Best subject for {name_input} is {top_grade_item[0]} with grade {top_grade_item[1]}")
            
            found_student_values = list(found_student.values()) if found_student else []
            grades = [grade for grade in found_student_values if grade != name_input]
            average_grade = sum(grades) / len(grades)
            print(f"Average grade for {name_input} is: {average_grade}")
            break
        
    if action == 3:
        all_grades: List = []
        for student in students:
            grades = [grade for grade in student.values() if isinstance(grade, int)]
            all_grades.extend(grades)
        
        print(f"Average grade for the class it: {sum(all_grades) / len(all_grades)}")
        
    if action == 4:
        break
            
shopping_cart: List = []
current_discount = 0.0

store_items = {
    "banana": 0.99,
    "apple": 0.50,
    "orange": 0.75,
    "milk": 3.99,
    "bread": 2.49,
    "cheese": 4.99,
    "eggs": 3.49,
    "chicken": 7.99,
    "rice": 5.99,
    "pasta": 1.99,
    "tomato": 0.99,
    "potato": 0.99,
    "onion": 0.79,
    "cereal": 4.49,
    "coffee": 8.99
}

discount_codes = {
    "SAVE10": 0.10,  # 10% off
    "SAVE20": 0.20,  # 20% off
    "FRESH": 0.15    # 15% off
}

while True:
    print("1. Show items")
    print("2. Add item")
    print("3. Remove item")
    print("4. Apply discount code")
    print("5. Get total")
    print("6. Exit")
    
    try:
        action = int(input("Choose an action (1 to 6) "))
        while action not in [1, 2, 3, 4, 5, 6]:
            action = 0
    except ValueError:
        action = 0
        
    if action == 1:
        print(store_items)
        
    if action == 2:
        while True:
            item_input = input("Enter an item name (or 'back' to return to the menu) ")
            
            if item_input.lower() == 'back':
                break
                
            if item_input in store_items:
                break
                
            print("Please enter an item from the available list")
            
        found_item_in_shopping_cart = next((item for item in shopping_cart if item["name"] == item_input), None)
        
        while True:
            try:
                input_description = f"Update quantity for {item_input} " if found_item_in_shopping_cart else "Enter quantity "
                quantity_input = float(input(input_description))
                break
            except ValueError:
                pass
        
        if found_item_in_shopping_cart:
            found_item_in_shopping_cart_index = shopping_cart.index(found_item_in_shopping_cart)
            shopping_cart[found_item_in_shopping_cart_index]["quantity"] = quantity_input
        else:
            item = {
                "name": item_input,
                "quantity": float(quantity_input)
            }
            
            shopping_cart.append(item)
            
    if action == 3:
        while True:
            item_input = input("Enter an item name to delete (or 'back' to return to the menu) ")
            
            if item_input.lower() == 'back':
                break
                
            if item_input in store_items:
                break
            else:
                print("Please enter an item from the available list")
            
            found_item_in_shopping_cart = next((item for item in shopping_cart if item["name"] == item_input), None)
            if found_item_in_shopping_cart:
                break
            else:
                print(f"Please enter an item from your cart: {shopping_cart}")
                
        shopping_cart.remove(found_item_in_shopping_cart)
            
    if action == 4:
        while True:
            discount_code_input = input("Enter a discount code (or 'back' to return to the menu) ")
            
            if discount_code_input.lower() == 'back':
                break
            
            if discount_code_input.upper() in discount_codes.keys():
                current_discount = discount_codes[discount_code_input.upper()]
                break
            
            print("Please enter a valid discount code")
            
    if action == 5:
        total: float = 0
        for item in shopping_cart:
            total = total + store_items[str(item["name"])] * item["quantity"] # type: ignore
            
        total = total - total * current_discount
        
        print(f"Total is: {total:.2f}")
        
    if action == 6:
        break
        
dictionary: Dict = {}

while True:
    sentence_input = input("Enter a sentence (or type finish to see the results) ")
    
    if sentence_input.lower() == "quit":
        break
    
    for word in sentence_input.split():
        if word.lower() in dictionary:
            dictionary[word.lower()] = dictionary[word.lower()] + 1
        else:
            dictionary[word.lower()] = 1

# This line sorts the dictionary by values (word frequencies) in descending order
# dictionary.items() gets list of (word, count) tuples
# sorted() sorts them using the key function
# lambda item: item[1] is an anonymous function that takes each tuple 'item'
#   and returns item[1] (the count) as the sorting key
# reverse=True makes it sort in descending order instead of ascending
# dict() converts the sorted items back into a dictionary
sorted_dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))

# Get first item using next() and iter()
# iter() creates an iterator from sorted_dictionary.items()
# next() gets the first element from that iterator
# Together they get the first key-value pair from the dictionary
first_item = next(iter(sorted_dictionary.items()))
print(f"Most frequent: {first_item}")

# Get last item by converting to list and accessing last index
last_item = list(sorted_dictionary.items())[-1]
print(f"Least frequent: {last_item}")

print(f"Entire dictionary sorted by frequency: {sorted_dictionary}")

