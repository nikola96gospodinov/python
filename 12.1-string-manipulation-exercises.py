from typing import TypedDict

def validate_password(password: str) -> bool:
    if len(password) < 8:
        print("Password must be at least 8 characters")
        return False
    
    if not any(char.isupper() for char in password):
        print("Password must contain at least one uppercase letter")
        return False
    
    if not any(char.islower() for char in password):
        print("Password must contain at least on lowercase letter")
        return False
    
    if not any(char.isdigit() for char in password):
        print("Password must contain at least one number")
        return False
    
    if not any(not char.isalnum() for char in password):
        print("Password must contain at least one special character")
        return False
    
    return True

class Statistics(TypedDict):
    word_count: int
    letter_count: int
    vowel_count: int
    longest_word: str
    most_frequent_word: str

def get_word_statistics(sentence: str) -> Statistics:
    words = sentence.split()
    
    word_count = len(words)
    letter_count = len("".join(words))
    vowel_count = len([letter for letter in "".join(words) if letter.lower() in ('a', 'e', 'i', 'o', 'u')])
    longest_word = max(words, key=len) if words else ""
    most_frequent_word = ""
    dictionary: dict[str, int] = {}
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    most_frequent_word = max(dictionary.items(), key=lambda x: x[1])[0] if dictionary else ""
    
    return {
        "word_count": word_count,
        "letter_count": letter_count,
        "vowel_count": vowel_count,
        "longest_word": longest_word,
        "most_frequent_word": most_frequent_word
    }
    
encoding_matrix = {
    "a": "1",
    "e": "2",
    "i": "3",
    "o": "4",
    "u": "5"
}
    
def encode_string(string: str) -> str:
    no_empty_space = "".join(string.split())
    encoded = ""
    
    for letter in no_empty_space:
        encoded_letter = encoding_matrix.get(letter.lower(), letter.upper())
        encoded = encoded + encoded_letter
            
    return encoded

