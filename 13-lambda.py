def double(x: int) -> int:
    return x * 2

double = lambda x: x * 2

sum_nums = lambda a, b: a + b

numbers = [1, 2, 3, 4, 5]

doubled = list(map(lambda x: x * 2, numbers)) # Not recommended in Python
evens = list(filter(lambda x: x % 2 == 0, numbers)) # Not recommended in Python

students = [("John", 23), ("Jane", 21), ("Dave", 25)]
sorted_by_age = sorted(students, key=lambda x: x[1])
sorted_by_name = sorted(students, key=lambda x: x[0])
sorted_by_age_and_name = sorted(students, key=lambda x: (x[1], x[0]))