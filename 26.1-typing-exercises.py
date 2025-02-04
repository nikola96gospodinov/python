from typing import TypeVar, Dict, Generic, List, TypedDict, Optional, Protocol, Any
from re import match
from dateutil.parser import parse
from datetime import datetime

# TODO: Create a generic cache that can store any type of value
# 1. Create a Cache class that's generic over type T
# 2. Implement set, get, and delete methods
# 3. Add a method to get all keys
# 4. Add a method to clear the cache
# 5. Use appropriate type hints

T = TypeVar("T")

class Cache(Generic[T]):
    def __init__(self) -> None:
        self._cache: Dict[str, T] = {}
        
    def __setitem__(self, key: str, value: T) -> None:
        if key in self._cache:
            print(f"Updating {key}...")
        else:
           print(f"Adding {key}...") 
        
        self._cache[key] = value
        
    def __getitem__(self, key: str) -> T | None:
        if key in self._cache:
            return self._cache[key]
        return None
    
    def __delitem__(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def get_all_keys(self) -> List[str]:
        return list(self._cache.keys())
    
    def clear_the_cache(self) -> None:
        self._cache = {}

int_cache = Cache[int]()
int_cache["first_operation"] = 10
int_cache["second_operation"] = 8
# int_cache["third_operation"] = "str" # ❌ Raises an error

# TODO: Create a data validation system for a REST API that:
# 1. Defines request/response structures using TypedDict
# 2. Uses Protocol to define validator interfaces
# 3. Implements generic validators for different data types

class UserRequest(TypedDict):
    username: str
    email: str
    age: int
    preferences: Optional[dict[str, str]]
    
class UserResponse(TypedDict):
    id: int
    username: str
    email: str
    created_at: str
    is_active: bool
    
T_contra = TypeVar("T_contra", contravariant=True)
    
class Validator(Protocol[T_contra]):
    def validate(self, data: T_contra) -> List[str]:  # Returns list of error messages
        ...
    
email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
class UserRequestValidator(Validator[UserRequest]):
    def validate(self, data: UserRequest) -> List[str]:
        errors: List[str] = []
        
        if not isinstance(data["username"], str) or data["username"].strip() == "":
            errors.append("username error: Make sure you enter a non-empty string")
            
        if not isinstance(data["email"], str) or not match(email_pattern, data["email"]):
            errors.append("email error: Make sure you enter a valid email")
            
        if not isinstance(data["age"], int) or data["age"] < 18:
            errors.append("age error: Make sure you enter an int above 18")
            
        if data["preferences"]:
            if not isinstance(data["preferences"], dict) or not all([isinstance(key, str) for key in data["preferences"].keys()]) or not all([isinstance(value, str) for value in data["preferences"].values()]):
                errors.append("preferences error: Make sure you pass a dict[str, str]")
        
        return errors
    
class UserResponseValidator(Validator[UserResponse]):
    def validate(self, data: UserResponse) -> List[str]:
        errors: List[str] = []
        
        if not isinstance(data["id"], int) or data["id"] <= 0:
            errors.append("id error: Make sure you enter a positive integer")
            
        if not isinstance(data["username"], str) or data["username"].strip() == "":
            errors.append("username error: Make sure you enter a non-empty string")
            
        if not isinstance(data["email"], str) or not match(email_pattern, data["email"]):
            errors.append("email error: Make sure you enter a valid email")
            
        try:
            parse(data["created_at"])
        except ValueError:
            errors.append("created_at error: Make sure you enter a valid date")
            
        if not isinstance(data["is_active"], bool):
            errors.append("is_active error: Make sure you enter a boolean")
        
        return errors
    
def main() -> None:
    user_data: UserRequest = {
        "username": "john_doe",
        "email": "invalid-email",
        "age": 17,
        "preferences": {"theme": "dark"}
    }
    
    request_validator = UserRequestValidator()
    errors = request_validator.validate(user_data)
    
    if errors:
        print(errors)
    else:
        response: UserResponse = {
            "id": 1,
            "email": "nik@nik.nik",
            "username": "nik",
            "created_at": "2025-01-01",
            "is_active": True
        }
        
        response_validator = UserResponseValidator()
        errors = response_validator.validate(response)
        
        if errors:
            print(errors)
        else:
            # Send response
            pass
        
if __name__ == "__main__":
    main()
    
# TODO: Create a data validation system for a REST API that:
# 1. Defines request/response structures using TypedDict
# 2. Uses Protocol to define validator interfaces
# 3. Implements generic validators for different data types

class RawData(TypedDict):
    timestamp: str
    values: List[str]
    metadata: Dict[str, Any]
    
class ProcessedData(TypedDict):
    timestamp: datetime
    values: List[float]
    average: float
    metadata: Dict[str, str]
    
Input = TypeVar("Input", bound=Dict[str, Any], contravariant=True)
Output = TypeVar("Output", bound=Dict[str, Any], covariant=True)

class DataTransformer(Protocol[Input, Output]):
    def transform(self, data: Input) -> Output: ...
    
class DataTransformationPipeline(DataTransformer[RawData, ProcessedData]): # type: ignore
    def transform(self, data: RawData) -> ProcessedData:
        float_values = [float(value) for value in data["values"]]
        
        transformed_data: ProcessedData = {
            "timestamp": datetime.strptime(data["timestamp"], "%Y-%m-%d"),
            "values": float_values,
            "average": sum(float_values) / len(float_values),
            "metadata": {key: str(value) for key, value in data["metadata"].items()}
        }
        
        return transformed_data
    
def main_2() -> None:
    raw_data: RawData = {
        "timestamp": "2024-01-20",
        "values": ["1.5", "2.5", "3.5"],
        "metadata": {
            "source": "sensor_1",
            "unit": "celsius",
            "raw_count": 3
        }
    }
    
    transformer = DataTransformationPipeline()
    processed = transformer.transform(raw_data)
    
    print(processed)
    
if __name__ == "__main__":
    main_2()