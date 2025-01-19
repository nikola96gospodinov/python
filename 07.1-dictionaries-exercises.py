from typing import List, Dict, Union
import re

# contacts: List = []
# email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# while True:
#     print("1. Add contact (name, phone, email)")
#     print("2. View all contacts")
#     print("3. Search for contacts")
#     print("4. Update contact")
#     print("5. Delete contact")
#     print("6. Exit")
    
#     while True:
#         try:
#             action = int(input("Choose an action (1 to 6) "))
#             if action in [1, 2, 3, 4, 5, 6]:
#                 break
#         except ValueError:
#             pass
    
#     if action == 1:
#         name = input("Enter a name ")
#         while not name.strip():
#             name = input("Name cannot be empty. Please enter a name ")
            
#         while True:
#             try:
#                 phone = int(input("Enter a valid phone number "))
#                 break
#             except ValueError:
#                 pass
            
#         email = input("Enter an email ")
#         while not re.match(email_pattern, email):
#             email = input("Please enter a valid email address (e.g. example@domain.com) ")
            
#         contacts.append({
#             "name": name,
#             "phone": phone,
#             "email": email
#         }) 
        
#     if action == 2:
#         print(contacts)
        
#     if action == 3:        
#         while True:
#             search = input("Search for contact (type 'back' to go back to the menu) ")
#             if search == 'back':
#                 break
                
#             found_contact = next((contact for contact in contacts if contact["name"] == search), None)
#             if found_contact:
#                 print(found_contact)
#                 break
            
#             print("Contact not found. Please try again or type 'back'")
            
#     if action == 4:
#         while True:
#             search = input("Which contact do you want to change (type 'back' to go back to the menu) ")
#             if search == 'back':
#                 break
            
#             found_contact = next((contact for contact in contacts if contact["name"] == search), None)
#             if found_contact:
#                 print("What do you want to change?")
#                 print("1. Name")
#                 print("2. Phone")
#                 print("3. Email")
                
#                 while True:
#                     try:
#                         update_action = int(input("Choose action "))
#                         if update_action in [1, 2, 3]:
#                             break
#                     except ValueError:
#                         pass
                    
#                 contact_index = contacts.index(found_contact)
                
#                 if update_action == 1:
#                     new_name_value = input("Enter a new name ")
#                     found_contact["name"] = new_name_value
                    
#                     contacts[contact_index] = found_contact
#                     print("Contact updated successfully")
#                     break
                
#                 if update_action == 2:
#                     try:
#                         new_phone_value = int(input("Enter a new phone number "))
#                     except:
#                         pass
                    
#                     found_contact["phone"] = new_phone_value
                    
#                     contacts[contact_index] = found_contact
#                     print("Contact updated successfully")
#                     break
                
#                 if update_action == 3:
#                     new_email_value = input("Enter a new email ")
#                     while not re.match(email_pattern, email):
#                         new_email_value = input("Please enter a valid email address (e.g. example@domain.com) ")
                        
#                     found_contact["email"] = new_email_value
                    
#                     contacts[contact_index] = found_contact
#                     print("Contact updated successfully")
#                     break
                        
#                 break
            
#             print("Contact not found. Please try again or type 'back'")
       
#     if action == 5:
#         while True:
#             name = input("Which contact do you want to delete (type 'back' to go back to the menu) ")
            
#             if name.lower() == 'back':
#                 break
            
#             found_contact = next((contact for contact in contacts if contact["name"] == name), None)
#             if found_contact:
#                 contacts.remove(found_contact)
#                 print("Contact successfully removed")
#                 break
            
#             print("Contact not found")
            
#     if action == 6:
#         break
            
students: List = []

while True:
    print("1. Enter student grades")
    print("2. Calculate grades per student")
    print("3. View grades")
    
    try:
        action = int(input("Select action "))
        if action not in [1, 2, 3]:
            action = 0
    except ValueError:
        action = 0
    
    if action == 1:
        student: Dict[str, Union[str, int]] = {}  # Type hint for mixed string/int values
        name_input = input("Enter a student name ")
        student["name"] = name_input
        
        while True:
            subject_input = input("Enter a subject (or type 'quit' to exit) ").lower()
            
            if subject_input == 'quit':
                break
            
            try:
                grade_input = int(input("Enter a grade (0 to 100) "))
                if 0 <= grade_input <= 100:
                    student[subject_input] = grade_input
            except ValueError:
                pass
                
                
            student[subject_input] = grade_input
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
            