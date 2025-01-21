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