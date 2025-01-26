from typing import List

class Animal:
    def __init__(self, name):
        self.name = name
        
    def speak(self):
        """Base class method - meant to be overridden"""
        raise NotImplementedError("Subclass must be implemented - speak()")
    
    def introduce(self):
        """This method uses speak() polymorphically"""
        return f"I am {self.name} and I {self.speak()}"
    
class Dog(Animal):
    def speak(self):
        return "bark"
    
    def fetch(self):
        return f"{self.name} is fetching the ball"
    
class Cat(Animal):
    def speak(self):
        return "meow"
    
    def scratch(self):
        return f"{self.name} is scratching"
    
class Duck(Animal):
    def speak(self):
        return "quack"
    
    def swim(self):
        return f"{self.name} is swimming"

# Polymorphic behaviour
def animal_chorus(animals: List[Animal]):
    """Function works with any animal subclass"""
    for animal in animals:
        print(animal.introduce())
        
# Create different animals
animals: List[Animal] = [
    Dog("Buddy"),
    Cat("Whiskers"),
    Duck("Donald")
]

# They're all different classes but can be treated as Animals
animal_chorus(animals)

# Each still has its unique methods
print(animals[0].fetch())
print(animals[1].scratch())
print(animals[2].swim())