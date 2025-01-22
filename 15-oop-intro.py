class Dog:
    # Class variable (share by all instances)
    species = "Canis familiaris"
    count = 0  # Keep track of how many dogs we create
    
    # Constructor (initializer method)
    def __init__(self, name, age, breed) -> None:
        # Instance variables (unique to each instance)
        self.name = name
        self.age = age
        self.breed = breed
        Dog.count += 1
        
    # Instance method
    def bark(self):
        return f"{self.name} says Woof!"
    
    def info(self):
        return f"{self.name} is a {self.breed} "
    
# Creating objects (instances) of the class
dog1 = Dog("Max", 5, "German Shepherd")
dog2 = Dog("Bella", 3, "Chihuahua")
dog3 = Dog("Charlie", 4, "Labrador")

# Using class variables
print(Dog.species) # "Canis familiaris"
print(Dog.count) # 3

# All dogs share the same species
print(dog1.species) # "Canis familiaris"
print(dog2.species) # "Canis familiaris"

# But each has its own name, age, and breed
print(dog1.info()) # Max is a German Shepherd
print(dog2.info()) # Bella is a Chihuahua
