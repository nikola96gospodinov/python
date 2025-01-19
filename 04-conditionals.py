age = int(input("What is your age? "))

if age >= 18:
    print("You're an adult")
else:
    print("You're a minor")
    exit()
    
score = int(input("What is your score "))

is_student_input = input("Are you a student? (True/False) ").lower()
while is_student_input not in ['true', 'false']:
    is_student_input = input("Please enter True or False: ").lower()
    
is_student = is_student_input == 'true'

if score >= 90 and not is_student:
    print("A")
elif score >= 80:
    print("B")
elif score >=70:
    print("C")
else:
    print("F")


