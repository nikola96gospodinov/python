counter = 0
while counter < 5:
    print(counter)
    counter += 1
    
password = input("Enter password ")
while password != "secret":
    password = input("Wrong password. Try again: ")
    
while True:
    choice = input("Enter 'quit' to exit: ")
    if choice.lower() != "quit":
        continue # Skip back to start if not `quit`
    break # Exit if `quit`
    
# range(5) generates: 0, 1, 2, 3, 4    
for i in range(5): 
    print(i)
    
# range(2, 6) generates: 2, 3, 4, 5    
for i in range(2, 6):
    print(i)
    
# range(0, 20, 5) generates: 0, 5, 10, 15
for i in range(0, 20, 5):
    print(i)
    
# range(5, 0, -1) generates: 5, 4, 3, 2, 1
for i in range(5, 0, -1):
    print(i)
    
number = 5
for i in range(1, 11):
    print(f"{number} x {i} = {number * i}")
    
numbers = list(range(1, 6)) # [1, 2, 3, 4, 5]

name = "Python"
for letter in name:
    print(letter)
    
numbers = [1, 2, 3, 4, 5, 6]
search_for = int(input("Enter a number "))

for num in numbers:
    if num == search_for:
        print("Number found!")
        break # break out of the loop
else:
    print("Could not find number")
    
for number in [1, 2, 3, 4, 5, 6]:
    if number % 2 == 0:
        continue # skip the rest of the iteration and do the next iteration. Essentially skipping even numbers
    print(number)
