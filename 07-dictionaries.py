person = {
    "name": "Nik",
    "age": 28,
    "city": "London"
}

print(person["name"])
print(person.get("age"))

person["email"] = "nikola96gospodinov@gmail.com"
person["age"] = 31

keys = person.keys()
print(keys)

values = person.values()
print(values)

items = person.items()
print(items)

# Get values with defaults
age = person.get("age", 0) # Returns 0 if age is not found

if "name" in person:
    print("name exists")
    
del person["age"]
popped = person.pop("name")

person1: dict[str, str | int] = {"name": "Nik"}
person2: dict[str, str | int] = {"age": 30}
person1.update(person2)