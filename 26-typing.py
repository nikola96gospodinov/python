from typing import TypeVar, Generic, List, Optional, Protocol, Dict, NewType, TypeAlias, Union, Tuple, Callable, Sequence, Any, Final, final, Literal, TypedDict, NotRequired, Required, overload, Annotated, TypeGuard
from datetime import datetime
from numbers import Number
from dataclasses import dataclass
from enum import Enum, auto

# Define a type variable
T = TypeVar("T")

# Generic class that can work with any type
class Box(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item
        
    def get_item(self) -> T:
        return self.item
    
    def set_item(self, item: T) -> None:
        self.item = item
        
# Usage
int_box = Box[int](42)
str_box = Box[str]("Hello")

K = TypeVar('K')
V = TypeVar('V')

class Pair(Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        
    def get_key(self) -> K:
        return self.key
    
    def get_value(self) -> V:
        return self.value
    
# Usage
pair = Pair[str, int]("age", 28)
name_pair = Pair[str, str]("first_name", "Nik")

# Bounded type variable
T = TypeVar("T", bound=Number)

class NumericContainer(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item
        
    def get_item(self) -> T:
        return self.item
    
    def is_positive(self) -> bool:
        return self.item > 0
    
# Valid usage
float_container = NumericContainer[float](5.5)
int_container = NumericContainer[int](10)

# This would raise a type error:
# str_container = NumericContainer[str]("invalid")  # Error: str is not a Number

class Entity(Protocol):
    id: int
    created_at: datetime
    
T = TypeVar("T", bound=Entity)

class Repository(Generic[T]):
    def __init__(self) -> None:
        self._items: Dict[int, T] = {}
        
    def add(self, item: T) -> None:
        self._items[item.id] = item
        
    def get(self, id: int) -> Optional[T]:
        return self._items.get(id)
    
    def get_all(self) -> List[T]:
        return list(self._items.values())
    
    def delete(self, id: int) -> bool:
        if id in self._items:
            del self._items[id]
            return True
        return False
    
class User(Entity):
    def __init__(self, id: int, name: str, email: str) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.created_at = datetime.now()
            
class Product(Entity):
    def __init__(self, id: int, name: str, price: float) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.created_at = datetime.now()
        
def main() -> None:
    # Create a repository for different entity types
    user_repository = Repository[User]()
    product_repository = Repository[Product]()
    
    # Add items
    user = User(1, "John Doe", "john.doe@example.com")
    product = Product(1, "Laptop", 999.99)
    
    # Add items
    user_repository.add(user)
    product_repository.add(product)
    
    # Retrieve items
    found_user = user_repository.get(1)
    if found_user:
        print(f"Found user: {found_user.name}")
    
    found_product = product_repository.get(1)
    if found_product:
        print(f"Found product: {found_product.name}, Price: ${found_product.price}")
        
if __name__ == "__main__":
    main()
    
UserId = int # Simple type alias
def get_user(user_id: UserId) -> str:
    return f"User {user_id}"
print(get_user(42))  # ✅ Works like an int

JsonDict: TypeAlias = Dict[str, Union[str, int, float, bool, None]]
Coordinate = Tuple[float, float]
def get_location() -> Coordinate:
    return (40.7128, -74.0060)  # Example GPS coordinates
print(get_location())  # (40.7128, -74.0060)

MathOperation = Callable[[int, int], int]
def add(a: int, b: int) -> int:
    return a + b
def apply_operation(x: int, y: int, operation: MathOperation) -> int:
    return operation(x, y)
print(apply_operation(2, 3, add)) # 5

# NewType for unique types
AdminId = NewType("AdminId", int)
RegularUserId = NewType("RegularUserId", int)

def process_admin(admin_id: AdminId) -> None:
    print(f"Processing admin {admin_id}")
    
def process_user(user_id: RegularUserId) -> None:
    print(f"Processing user {user_id}")
    
regular_id = RegularUserId(123)
admin_id = AdminId(456)

process_admin(admin_id) # ✅
# process_admin(regular_id) # Type error: Expected AdminId, got RegularUserId - despite both being technically int

T = TypeVar("T")
S = TypeVar("S", bound=Sequence[Any])
N = TypeVar("N", int, float)

class DataProcessor(Generic[T]):
    def __init__(self, data: T) -> None:
        self.data = data
        
    def process(self, func: Callable[[T], T]) -> T:
        return func(self.data)
    
def double_value(x: int) -> int:
    return x * 2

int_processor = DataProcessor[int](5)
result = int_processor.process(double_value)
print(f"Processed int: {result}")
    
class SequenceProcessor(Generic[S]):
    def __init__(self, sequence: S) -> None:
        self.sequence = sequence
        
    def first(self) -> Any:
        return self.sequence[0]
    
list_processor = SequenceProcessor([1, 2, 3])
first = list_processor.first()
print(f"First element: {first}")
    
class NumericCalculator(Generic[N]):
    def __init__(self, value: N) -> None:
        self.value: N = value
        
    def add(self, other: N) -> N:
        return self.value + other
    
int_calc = NumericCalculator(5)
float_calc = NumericCalculator(5.5)
print(f"Int calc: {int_calc.add(3)}")
print(f"Float calc: {float_calc.add(3.2)}")

class Priority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    
T = TypeVar("T")

class Event(Generic[T]):
    def __init__(self, data: T, priority: Priority = Priority.MEDIUM) -> None:
        self.data = data
        self.priority = priority
        self.timestamp = datetime.now()
        
class EventHandler(Protocol[T]):
    def handle(self, event: Event[T]) -> None: ...
    
@dataclass
class UserEvent:
    user_id: int
    action: str
    metadata: Dict[str, Any]
    
@dataclass
class SystemEvent:
    component: str
    status: str
    details: Optional[str] = None
    
class EventBus:
    def __init__(self) -> None:
        self._handlers: Dict[type, List[EventHandler[Any]]] = {}
        self._events: List[Event[Any]] = []
        
    def register_handler(self, event_type: type, handler: EventHandler[Any]) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        
    def publish(self, event: Event[Any]) -> None:
        self._events.append(event)
        event_type = type(event.data)
        
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler.handle(event)
                
    def get_events_by_priority(self, priority: Priority) -> List[Event[Any]]:
        return [event for event in self._events if event.priority == priority]
    
class UserEventHandler(EventHandler[UserEvent]):
    def handle(self, event: Event[UserEvent]) -> None:
        user_event = event.data
        print(f"Handling user event: User {user_event.action} (ID: {user_event.user_id})")
        
class SystemEventHandler(EventHandler[SystemEvent]):
    def handle(self, event: Event[SystemEvent]) -> None:
        system_event = event.data
        print(f"Handling system event: {system_event.component} is {system_event.status}")
        
def main() -> None:
    event_bus = EventBus()
    
    event_bus.register_handler(UserEvent, UserEventHandler())
    event_bus.register_handler(SystemEvent, SystemEventHandler())
    
    user_event = Event(
        UserEvent(
            user_id=1,
            action="register",
            metadata={"id": "192.168.1.1"}
        ),
        Priority.HIGH
    )
    
    user_event_2 = Event(
        UserEvent(
            user_id=2,
            action="login",
            metadata={"id": "192.168.1.1"}
        ),
        Priority.HIGH
    )
    
    system_event = Event(
        SystemEvent(
            component="database",
            status="connected"
        ),
        Priority.MEDIUM
    )
    
    event_bus.publish(user_event)
    event_bus.publish(user_event_2)
    event_bus.publish(system_event)
    
    high_priority = event_bus.get_events_by_priority(Priority.HIGH)
    print(f"\nHigh priority events: {len(high_priority)}")
    
if __name__ == "__main__":
    main()

Mode = Literal["r", "w", "a"]

def open_file(path: str, mode: Mode) -> None:
    with open(path, mode) as f:
        pass
    
open_file("test.txt", "r") # ✅ This is valid
# open_file("test.txt", "x") # ❌ This isn't valid

# Final variables cannot be reassigned
MAX_CONNECTIONS: Final = 100
API_KEY: Final[str] = "secret_key"

@final # ❌ Prevents subclassing
class DatabaseConnection:
    def __init__(self) -> None:
        self.connected = False
        
    @final # ❌ Prevents overriding in subclasses if allowed (in this case we won't have subclasses because of the original @final for the DatabaseConnection class)
    def connect(self) -> None:
        self.connected = True
        
class UserDict(TypedDict):
    name: str
    age: int
    email: str
    address: NotRequired[str] # Optional field
    
class ConfigDict(TypedDict, total=False): # All fields are optional
    debug: bool
    host: str
    port: int
    
def process_user(user: UserDict) -> None:
    print(f"Processing {user['name']}, age {user['age']}")
    
process_user({
    "name": "Nik",
    "age": 28,
    "email": "nikola96gospodinov@gmail.com"
    # "city": "London" - ❌ this will throw an error
})

def process_config(config: ConfigDict) -> None:
    pass

process_config({
    "debug": True # ✅ No need to pass all of them
})

T = TypeVar("T")

Handler = Callable[[str], None]
Transform = Callable[[T], T]

def process_with_handler(data: str, handler: Handler) -> None:
    handler(data)
    
# Function overloads - used to provide static type checks for multiple function signatures
@overload
def process_data(data: str) -> str: ...

@overload
def process_data(data: bytes) -> bytes: ...

@overload
def process_data(data: None) -> None: ...

def process_data(data: Union[str, bytes, None]) -> Union[str, bytes, None]:
    if isinstance(data, (str, bytes)):
        return data.upper()
    return None

Password = Annotated[str, "Must be at least 8 characters long"]
UserId = Annotated[int, "Must be positive"]

@dataclass
class User:
    username: str
    password: Password
    user_id: UserId
    
user = User("nik", "123456", -2) # ❗ Doesn't actually enforce it

def is_string_list(val: List[Any]) -> TypeGuard[List[str]]:
    return all(isinstance(x, str) for x in val)

def process_strings(values: List[Any]) -> None:
    if is_string_list(values):
        # Type is narrowed to List[str]
        print(", ".join(values))
        
def is_non_empty_string(val: Optional[str]) -> TypeGuard[str]:
    return isinstance(val, str) and len(val) > 0

def process_value(val: Optional[str]) -> None:
    if is_non_empty_string(val):
        # Type is narrowed to str
        print(val.upper())