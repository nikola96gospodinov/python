# 1. Global scope
x = 10

def function1():
    print(x) # Can read global variable
    
def function2():
    # x = x + 1 # ERROR! Can't modify global without 'global'
    global x
    x = x + 1 # Now it works with the global keyword
    
# 2. Local scope
def outer_function():
    y = 5 # Local to outer_function
    
    def inner_function():
        z = 3 # Local to inner_function
        print(y) # Can read from outer function
        print(z) # Can read local
    
    inner_function()
    print(y) # Can read local
    # print(z)  # ERROR! z only exists in inner_function
    
# 3. Nonlocal Scope
def outer():
    count = 0
    
    def inner():
        nonlocal count # Allows modification of outer variable
        count += 1
        print(count)
        
    inner()
    print(count)
    
def shadowing_function():
    x = 5 # Creates new local variable, doesn't affect global
    print(x) # Prints 5
    
shadowing_function()
print(x) # Prints 10

# List modification (doesn't need global)
numbers = [1, 2, 3]

def modify_list():
    numbers.append(4) # Works! Modifying object, not variable
    # numbers = [4, 5, 6]  # This would create new local variable

modify_list()
print(numbers)  # [1, 2, 3, 4]

def create_counter():
    count = 0
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter

my_counter = create_counter()
print(my_counter())  # 1
print(my_counter())  # 2