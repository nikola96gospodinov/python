text = "  hello, Python world!  "

print(text.upper()) # "  HELLO, PYTHON WORLD!  "
print(text.lower()) # "  hello, python world!  "
print(text.title()) # "  Hello, Python World!  "
print(text.capitalize()) # "  Hello, python world!  "

print(text.strip()) # "hello, Python world!"
print(text.lstrip())
print(text.rstrip())

message = "Python is amazing, Python is fun"
print(message.count("Python")) # 2
print(message.find("Python")) # 0 (first occurrence index)
print(message.find("Go")) # -1 (not found)

word = "Python3"
print(word.isalpha()) # False - checks if all characters are letters (no numbers, spaces, or punctuation)
print(word.isalnum()) # True - checks if all characters are letters or numbers (no spaces or punctuation)
print(word.isdigit()) # False - checks if all characters are digits (0-9)

sentence = "Python is amazing"
words = sentence.split() # ['Python', 'is', 'amazing']
new_sentence = "-".join(words) # "Python-is-amazing"

text = "I love Java"
new_text = text.replace("Java", "Python")

name = "Nik"
age = 28
print("My name is {} and I am {} years old".format(name, age))

sub_strings = "Python Programming"
# This extracts characters from index 0 to 5 (6 is exclusive)
# In this case it prints "Python" - the first 6 characters of "Python Programming"
print(sub_strings[0:6])

# This extracts characters from index 7 to the end of the string
# In this case it prints "Programming" - everything after "Python "
print(sub_strings[7:])

# This extracts characters from index -11 to the end of the string
# In this case it prints "Programming" - counting 11 characters from the end
print(sub_strings[-11:])

# This reverses the string by using a step of -1
# In this case it prints "gnimmargorP nohtyP" - the string "Python Programming" in reverse
print(sub_strings[::-1])

print("Ha" * 3) # HaHaHa

python = "Python"
# text[0] = "J"  # This will raise an error
jython = "J" + text[1:]