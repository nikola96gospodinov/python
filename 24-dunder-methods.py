from typing import Dict, Iterator, Any, Optional, List
from datetime import datetime

# Object Representation (How objects are converted to strings)
class Person:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age
        
    def __str__(self) -> str:
        # Used when str() is called or print() is used
        # For human-readable representation
        return f"{self.name}, {self.age} years old"
    
    def __repr__(self) -> str:
        # Used for debugging and development
        # Should ideally be unambiguous and complete
        return f"Person(name='{self.name}', age='{self.age}')"
    
# Usage
person = Person("Alice", 30)
print(person) # Uses __str__: "Alice, 30 years old"
print(repr(person)) # Uses __repr__: "Person(name='Alice', age=30)"

# Container and Sequence Behavior (Making objects behave like lists/dictionaries)
class Inventory:
    def __init__(self) -> None:
        self.items: Dict[str, int] = {}
        self.last_updated: datetime = datetime.now()
        self.max_capacity: int = 100
        
    def __len__(self):
        # Makes len() work
        return len(self.items)
    
    def __getitem__(self, key: str) -> int:
        # Makes inventory["item"] work
        return self.items[key]
    
    def __setitem__(self, key: str, value: int) -> None:
        # Makes inventory["item"] = value work
        current_total = sum(self.items.values())
        if key not in self.items:
            if current_total + value > self.max_capacity:
                raise ValueError(f"Adding {value} items would exceed max capacity of {self.max_capacity}")
        else:
            if current_total - self.items[key] + value > self.max_capacity:
                raise ValueError(f"Updating to {value} items would exceed max capacity of {self.max_capacity}")
            
        self.items[key] = value
        self.last_updated = datetime.now()
        
    def __iter__(self) -> Iterator[str]:
        return iter(self.items)
    
    def __contains__(self, key: str) -> bool:
        return key in self.items
    
    def get_item_count(self, item: str) -> Optional[int]:
        """Get the count of a specific item."""
        return self.items.get(item)
    
    def get_total_items(self) -> int:
        """Get the total count of all items."""
        return sum(self.items.values())
    
    def get_available_capacity(self) -> int:
        """Get remaining capacity."""
        return  self.max_capacity - self.get_total_items()
    
    def __str__(self) -> str:
        return f"Inventory(items: {len(self.items)}, total count: {self.get_total_items()}, available: {self.get_available_capacity()})"
    
    def __repr__(self) -> str:
        return f"Inventory(items={self.items}, last_updated={self.last_updated}, max_capacity={self.max_capacity})"

# Usage example
def main() -> None:
    inventory = Inventory()
    
    try:
        inventory["banana"] = 30
        inventory["apple"] = 25
        inventory["orange"] = 15
        
        print(f"Total items: {len(inventory)}")
        print(f"Apple count: {inventory["apple"]}")
        print(f"Total count: {inventory.get_total_items()}")
        print(f"Available capacity: {inventory.get_available_capacity()}")
        print(f"Last updated: {inventory.last_updated}")
        
        print("Current inventory:")
        for item in inventory:
            print(f"{item}: {inventory[item]}")
            
        print(f"Has apples: {"apple" in inventory}")
        print(f"Has grapes: {'grape' in inventory}")
        
        # Try to exceed capacity
        inventory['grape'] = 40
    except ValueError as error:
        print(f"Error: {error}")
        
if __name__ == "__main__":
    main()

# Comparison Operations (How objects are compared)
class Temperature:
    def __init__(self, celsius) -> None:
        self.celsius = celsius
        
    def __eq__(self, other) -> bool:
        # Defines == behavior
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius == other.celsius
    
    def __lt__(self, other) -> bool:
        # Defines < behavior
        # Python uses this to derive >, <=, >= automatically
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius < other.celsius
    
# Usage
t1 = Temperature(20)
t2 = Temperature(25)
print(t1 < t2) # True
print(t1 == t2) # False

# Arithmetic Operations (How objects behave with mathematical operators)
class Money:
    def __init__(self, amount: float) -> None:
        self.amount = amount
        
    def __add__(self, other):
        # Defines + operator
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.amount + other.amount)
        
    def __sub__(self, other):
        # Defines - operator
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.amount - other.amount)
    
# Usage
m1 = Money(100)
m2 = Money(50)
m3 = m1 + m2  # Uses __add__

# Context Management (For use with 'with' statement)
class QueryBuilder:
    def __init__(self) -> None:
        self.query: Dict[str, Any] = {}
        self.order_by: List[str] = []
        self.limit_value: Optional[int] = None
        self._operators = {
            'eq': '=',
            'gt': '>',
            'lt': '<',
            'gte': '>=',
            'lte': '<=',
            'like': 'LIKE',
            'in': 'IN'
        }
        
    def __call__(self, **kwargs: Any) -> 'QueryBuilder':
        """
        Allows the object to be called like a function to add conditions.
        Example: query(name='John', age__gt=25)
        """
        for key, value in kwargs.items():
            # Handle special operators (e.g., age__gt=25)
            if "__" in key:
                field, operator = key.split("__")
                if operator in self._operators:
                    self.query[field] = {
                        "operator": self._operators[operator],
                        "value": value
                    }
            else:
                # Handle simple equality
                self.query[key] = {
                    "operator": "=",
                    "value": value
                }
            
        return self
        
    def order(self, *fields: str) -> 'QueryBuilder':
        """Add ORDER BY clause"""
        self.order_by.extend(fields)
        return self
    
    def limit(self, value: int) -> 'QueryBuilder':
        """Add LIMIT clause"""
        self.limit_value = value
        return self
    
    def _format_value(self, value: Any) -> str:
        """Format values based on their type"""
        if isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, datetime):
            return f"'{value.strftime("%Y-%m-%d %H:%M:%S")}'"
        elif isinstance(value, (list, tuple)):
            return f"({", ".join(map(self._format_value, value))})"
        return str(value)
    
    def __str__(self) -> str:
        """Convert the query to SQL string"""
        conditions = []
        
        for field, details in self.query.items():
            operator = details["operator"]
            value = self._format_value(details["value"])
            conditions.append(f"{field} {operator} {value}")
            
        sql = "SELECT * FROM some_table"
        
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
            
        if self.order_by:
            sql += " ORDER BY " + ", ".join(self.order_by)
            
        if self.limit_value:
            sql += f" LIMIT {self.limit_value}"
            
        return sql
    
# Usage example
def demo_query_builder() -> None:
    query = QueryBuilder()
    
    # Example 1: Simple equality conditions
    print("Example 1: Simple query")
    result = query(name="Nik", age=28)
    print(result)
    
    # Example 2: Using operators
    print("\nExample 2: Query with operators")
    query = QueryBuilder()
    result = query(
        age__gt=25,
        salary__lte=5000,
        department__in=("HR", "IT"),
        name__like="J%"
    )
    print(result)
    
    # Example 3: Chaining methods
    print("\nExample 3: Chained query with ordering and limit")
    query = QueryBuilder()
    result = (
        query(status="active")
        .order("created_at", "name")
        .limit(10)
    )
    print(result)
    
    # Example 4: Date handling
    print("\nExample 4: Query with datetime")
    query = QueryBuilder()
    result = query(created_at__gt=datetime(2024, 1, 1))
    print(result)
    
if __name__ == "__main__":
    demo_query_builder()
