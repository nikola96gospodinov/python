############
## TUPLES ##
############
point = (10, 20)
person = ("Nik", 28, "London")
# The comma is necessary to distinguish a single-item tuple from a regular parenthesized expression
# Without the comma, (42) would just be the number 42 in parentheses
# With the comma, (42,) creates a tuple with one item
single_item = (42,)
empty = ()

x = point[0] # 10
name = person[0] # "Nik"

x, y = point # x = 10, y = 20
name, age, city = person # Unpacks all three values

def get_coordinates() -> tuple[int, int]:
    return (3, 4) # Return tuple

x, y = get_coordinates() # Unpacks returned tuple

numbers = (1, 2, 2, 3, 2)
count = numbers.count(2) # Counts occurrences: 3
index = numbers.index(3) # Finds first index: 3

length = len(point)
exists = 20 in point
combined = point + (30,) # (10, 20, 30)

matrix = ((1, 2), (3, 4))
value = matrix[0][1] # 2

##########
## SETS ##
##########
numbers_set = {1, 2, 3}
from_list = set([1, 2, 3])
empty_set: set = set()

numbers_set.add(4) # {1, 2, 3, 4}
numbers_set.update([4, 5, 6]) # {1, 2, 3, 4, 5, 6} No duplicates
numbers_set.update({7, 8}, {9}) # {1, 2, 3, 4, 5, 6, 7, 8, 9}

numbers_set.remove(1) # Removes 1 (raises error if not found)
numbers_set.discard(1) # Removes 1 (no error if not found)
popped = numbers_set.pop() # Removes and returns first item
numbers_set.clear()

set1 = {1, 2, 3}
set2 = {3, 4, 5}

# Union (all unique items from both sets)
union = set1 | set2 # {1, 2, 3, 4, 5}
union = set1.union(set2)

# Intersection (items in both sets)
common = set1 & set2 # {3}
common = set1.intersection(set2)

# Difference (items in set1 but not in set2)
diff = set1 - set2 # {1, 2}
diff = set1.difference(set2)

if 1 in set1:
    print("1 exists in set!")
    
# Check if subset/superset
set3 = {1, 2}
print(set3 <= set1) # True - Subset
print(set1 >= set3) # True - Superset

# Remove duplicates
repeat_numbers = [1, 2, 2, 3, 3, 4]
unique_numbers = list(set(numbers)) # [1, 2, 3, 4]

# Find common items
list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
common = set(list1) & set(list2) # {3, 4}

# Remove specific items from list
new_numbers = [1, 2, 3, 4, 5]
remove_these = {2, 4}
filtered = set(new_numbers) - remove_these

# 1. LISTS - Ordered, mutable collection
# Use when you:
# - Need ordered items
# - Want to modify collection
# - Need duplicate items
# - Need to access by index

# Practical examples:
todo_list = ["Buy milk", "Walk dog", "Code"]
scores = [95, 89, 92, 88, 95]
queue = ["John", "Alice", "Bob"]  # First in, first out


# 2. TUPLES - Ordered, immutable collection
# Use when you:
# - Have data that shouldn't change
# - Want to return multiple values
# - Need slightly better performance than lists

# Practical examples:
coordinates = (10, 20)
rgb_color = (255, 128, 0)
user_info = ("john_doe", "John", 25)


# 3. DICTIONARIES - Key-value pairs
# Use when you:
# - Need to associate values with keys
# - Want fast lookups by key
# - Need to store object-like data

# Practical examples:
user = {"name": "John", "age": 25, "city": "NY"}
settings = {"dark_mode": True, "notifications": False}
menu = {"coffee": 2.99, "tea": 1.99, "cake": 3.99}


# 4. SETS - Unordered collection of unique items
# Use when you:
# - Need unique items only
# - Want to check membership quickly
# - Need set operations (union, intersection)

# Practical examples:
unique_visitors = {"user1", "user2", "user3"}
valid_categories = {"electronics", "books", "clothing"}
friends1 = {"Alice", "Bob"}
friends2 = {"Bob", "Charlie"}
mutual_friends = friends1 & friends2  # Intersection