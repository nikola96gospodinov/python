from typing import Callable, List, TypedDict, Any
from datetime import date
from functools import wraps

def debug(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        print(f"Calling: {func.__name__}")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Returns: {result}")
        return result
    return wrapper

@debug
def add(a, b):
    return a + b

def retry(attempts: int) -> Callable:
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            for attempt in range(attempts):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as error:
                    if attempt == attempts - 1:
                        print(f"An error occurred: {error}")
                        raise error
            return result
        return wrapper
    return decorator
        
@retry(attempts=3)
def possibly_failing_function():
    # This function might raise an exception
    pass

class CacheItem(TypedDict):
    function_name: str
    args: List
    kwargs: List[dict] 
    result: Any

cache: List[CacheItem] = []

def cache_results(max_size: float):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            cached_item: CacheItem | None = [cache_item for cache_item in cache if cache_item["function_name"] == func.__name__ and cache_item["args"] == args and cache_item["kwargs"] == kwargs]
            
            if cached_item:
                cached_item_index = cache.index(cached_item[0])
                moved_item = cache.pop(cached_item_index)
                cache.append(moved_item)
                return moved_item["result"]
            
            result = func(*args, **kwargs)
            new_item: CacheItem = {
                "function_name": func.__name__,
                "args": args,
                "kwargs": kwargs,
                "result": result
            }
            cache.append(new_item)
            
            if len(cache) > max_size:
                cache.pop(0)
                
            return result
        return wrapper
    return decorator

@cache_results(max_size=100)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n + 1)


def validate_types(**type_args):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_params = func.__code__.co_varnames[:func.__code__.co_argcount]

            for key in type_args:
                if key not in func_params:
                    raise KeyError(f"'{key}' was specified in validate_types but isn't a parameter of {func.__name__}")
            
            for i, arg in enumerate(args):
                try:
                    param_name = list(type_args.keys())[i]
                except IndexError:
                    raise ValueError(f"Argument '{arg}' is missing type validation")

                expected_type = type_args[param_name]
                
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Argument '{param_name}' must be {expected_type.__name__}, got {type(arg).__name__}")
            
            for param_name, value in kwargs.items():
                if param_name in type_args:
                    expected_type = type_args[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(f"Argument '{param_name}' must be {expected_type.__name__}, got {type(value).__name__}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_ranges(**range_args):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_params = func.__code__.co_varnames[:func.__code__.co_argcount]
            
            bound_args = dict(zip(func_params, args))
            bound_args.update(kwargs)
            
            for param_name, expected_range in range_args.items():
                if param_name not in bound_args:
                    continue
                    
                arg = bound_args[param_name]
                
                # Numbers range
                if isinstance(arg, (int, float)) and isinstance(expected_range[0], (int, float)) and isinstance(expected_range[1], (int, float)):
                    min_val = min(expected_range[0], expected_range[1])
                    max_val = max(expected_range[0], expected_range[1])
                    if arg < min_val or arg > max_val:
                        raise ValueError(f"{arg} is not in range [{min_val}, {max_val}]")
                        
                # Length range
                elif isinstance(arg, str) and isinstance(expected_range[0], (int, float)) and isinstance(expected_range[1], (int, float)):
                    arg_length = len(arg)
                    min_len = min(expected_range[0], expected_range[1])
                    max_len = max(expected_range[0], expected_range[1])
                    if arg_length < min_len or arg_length > max_len:
                        raise ValueError(f"Length of '{arg}' ({arg_length}) is not in range [{min_len}, {max_len}]")
                        
                # Strings (alphabetical)
                elif isinstance(arg, str) and isinstance(expected_range[0], str) and isinstance(expected_range[1], str):
                    arg_lower = arg.lower()
                    range_start = expected_range[0].lower()
                    range_end = expected_range[1].lower()
                    
                    if not (min(range_start, range_end) <= arg_lower <= max(range_start, range_end)):
                        raise ValueError(f"'{arg}' is not in alphabetical range [{min(expected_range)}, {max(expected_range)}]")
                        
                # Dates
                elif isinstance(arg, date) and isinstance(expected_range[0], date) and isinstance(expected_range[1], date):
                    start_date = min(expected_range[0], expected_range[1])
                    end_date = max(expected_range[0], expected_range[1])
                    
                    if arg < start_date or arg > end_date:
                        raise ValueError(f"Date {arg} is not in range [{start_date}, {end_date}]")
                    
                else:
                    raise ValueError(f"Unsupported range validation for argument type {type(arg).__name__}")
                        
            return func(*args, **kwargs)
        return wrapper
    return decorator
        
@validate_ranges(age=(0, 120))
@validate_types(age=int, name=str)
def create_person(age, name):
    return f"{name} is {age} years old"