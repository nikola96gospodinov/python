class Employee:
    # Base class for all employees
    company_name = "Tech Corp" # Class variable shared by all employees
    
    def __init__(self, name, id, salary):
        self.name = name
        self.id = id
        self.salary = salary
        
    def get_info(self):
        return (f"Name: {self.name}, ID: {self.id}, Salary: {self.salary}")
    
    def calculate_yearly_bonus(self):
        return self.salary * 0.1 # Default 10% bonus
    
class Developer(Employee):
    def __init__(self, name, id, salary, programming_language):
        # Call parent class's __init__
        super().__init__(name, id, salary)
        # Add developer specific attribute
        self.programming_language = programming_language
      
    # Override parent method  
    def get_info(self):
        basic_info = super().get_info() # Get parent's implementation
        return f"{basic_info}, Language: {self.programming_language}"
    
    # Override with different bonus
    def calculate_yearly_bonus(self):
        return self.salary * 0.15 # 15% bonus for developers
    
    # Developer-specific method
    def code(self):
        return f"{self.name} is coding in {self.calculate_yearly_bonus}"
    
class Manager(Employee):
    def __init__(self, name, id, salary, team_size):
        super().__init__(name, id, salary)
        self.team_size = team_size
        self.team_members = []
        
    def add_team_member(self, employee: Employee) -> bool:
        if len(self.team_members) < self.team_size:
            self.team_members.append(employee)
            return True
        return False
    
    def calculate_yearly_bonus(self):
        return self.salary * 0.2
    
    def get_team_info(self):
        return f"Team size: {len(self.team_members)}, Max size: {self.team_size}"
    
dev1 = Developer("Nik", "D001", 105_000, "Python")
dev2 = Developer("Alice", "D002", 75_000, "Java")
manager = Manager("Charlie", "M001", 90_000, 5)

print(dev1.get_info())
print(manager.get_info())

print(dev1.code())

manager.add_team_member(dev1)
manager.add_team_member(dev2)
print(manager.get_team_info())

print(f"{dev1.name}'s bonus is {dev1.calculate_yearly_bonus()}")
print(f"{manager.name}'s bonus is {manager.calculate_yearly_bonus()}")

print(isinstance(dev1, Employee)) # True
print(isinstance(dev1, Developer)) # True
print(isinstance(dev1, Manager)) # False