from typing import List

numbers = [1, 2, 3, 4, 5]
names = ["Alice", "Bob", "Charlie"]
mixed = [1, "hello", True, 3.14]
empty_list: List = []

enforced_numbers_only: List[int] = [1, 2, 3]

fruits = ["apple", "banana", "orange"]
print(fruits[0]) # First
print(fruits[-1]) # Last
print(fruits[1:3]) # Slice

fruits.append("mango")
fruits.insert(1, "grape")

fruits.remove("banana")
popped = fruits.pop()
del fruits[0]

length = len(fruits)

print(length)
print(fruits)

if 3 in numbers:
    print("Found 3!")
    
index = numbers.index(3)
count_occurrences = numbers.count(3)

numbers.sort() # ascending
numbers.sort(reverse=True) # descending
fruits.sort(key=str.lower) # case insensitive sorting

numbers.reverse()
numbers_copy = numbers.copy()

numbers.clear() # empty the list
