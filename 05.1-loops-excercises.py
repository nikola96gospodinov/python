from typing import List
import random

amountOfNumbers = int(input("How many numbers do you want to add? "))

total = 0

for i in range(amountOfNumbers):
    numberInput = int(input("Enter a number: "))
    total = total + numberInput
    
print(f"Total is: {total}")
print(f"Average is: {total / amountOfNumbers}")

password = input("Enter a password ")

while len(password) < 8:
    password = input("Password must be at least 8 characters ")
    
has_number = False

for char in password:
    if char.isdigit():
        has_number = True
        break
    
while has_number == False:
    password = input("Password must contain at least one number ")
    for char in password:
        if char.isdigit():
            has_number = True
            break
        
while not any(c.isupper() for c in password):
    password = input("Password must contain at least one uppercase character ")
    
print("Password is valid")

random_number = random.randint(1, 100)
number_of_tries = 7

while number_of_tries > 0:
    guess = int(input("Have a guess: "))
    
    if guess == random_number:
        print("You win!")
        break
    else:
        number_of_tries = number_of_tries - 1
        if guess < random_number:
            print("Your guess is higher than the number")
        else:
            print("Your guess is lower than the number")

word = input("Give me a word ")
newWord = ""

while word != "no":
    for char in word:
        newWord = f"{char}{newWord}"
        
    print(f"{newWord}")
    newWord = ""
    word = input("Do you want another word? ")

balance = 1000

while True:
    # First, show the menu options
    print("\n=== ATM Menu ===")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    # Then get user's choice
    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        print(f"Balance is {balance}")
        
    if choice == "2":
        deposit = int(input("Enter amount you want to deposit "))
        while int(deposit) < 0:
            deposit = int(input("Enter a positive amount "))
            
        balance = balance + int(deposit)
        
    if choice == "3":
        withdraw = int(input("Enter how much you want to withdraw "))
        
        while int(withdraw) < 0:
            withdraw = int(input("Enter a positive amount "))
        
        while int(withdraw) > balance:
            withdraw = int(input(f"You don't have enough funds. Currently you have {balance}. Enter a number that is lower or equal to your balance "))
            
        balance = balance - int(withdraw)
        
    if choice == "4":
        break

list_of_numbers: List[int] = []   
 
while True:
    number_input = int(input("Enter a number "))
    
    if number_input == 0:
        break
    elif number_input < 0:
        continue
    else:
        list_of_numbers.append(number_input)
        
print(f"Sum of all positive numbers is: {sum(list_of_numbers)}")

