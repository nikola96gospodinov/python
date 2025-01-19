temp = float(input("Enter temperature "))

temp_metric = input("Choose what your current temperature is in (Fahrenheit, Celsius). Enter either F or C ")
while temp_metric not in ['C', 'F']:
    temp_metric = input("Enter either F or C please ")
    
if temp_metric == "C":
    temp = (9/5 * temp) + 32
else:
    temp = (temp - 32) * 5/9
    
print(f"Temperature in { "Celsius" if temp_metric == "C" else "Fahrenheit" } is {temp}")

OPTIONS = ['rock', 'paper', "scissors"]

player1 = input("Rock, paper, scissors? ").lower()
while player1 not in OPTIONS:
    player1 = input("Enter either 'rock', 'paper', or 'scissors'")

player2 = input("Rock, paper, scissors? ")
while player2 not in OPTIONS:
    player2 = input("Enter either 'rock', 'paper', or 'scissors'")
    
WINNING_MOVES = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}
    
if player1 == player2:
    print("Draw")
elif WINNING_MOVES[player1] == player2:
    print("Player 1 wins")
else:
    print("Player 2 wins")

username = input("Enter username ")
while not username == "admin":
    username = input("Username not found. Try again ")

password = input("Enter password ")
while not password == "password123":
    password = input("Wrong password. Try again ")
    
print("Login success")
    
number = int(input("Enter a number "))

print(f"{"Number is even" if number % 2 == 0 else "Number is odd"}")    
print(f"{"Number is divisible by 5" if number % 5 == 0 else "Number is not divisible by 5"}")

if number == 0:
    print("Number is 0")
elif number > 0:
    print("Number is positive")
else:
    print("Number is negative")

size = input("What size do you want? (Small, Medium, Large) ").lower()
while size not in ["small", "medium", "large"]:
    size = input("Enter a size that is either Small, Medium or Large")
    
extraShot = input("Do you want an extra shot? (Yes, No) ").lower()
while extraShot not in ["yes", "no"]:
    extraShot = input("Enter either Yes or No")
    
pricing = {
    "small": 3,
    "medium": 4,
    "large": 5
}

total = pricing[size] + 1.5 if extraShot == "yes" else 0
print(f"Total: {total}")
