from typing import Generator, List, Iterator, Any, Optional, Dict
import sys
from itertools import cycle, islice, chain, combinations
from datetime import datetime

def number_generator(start: int, end: int) -> Generator[int]:
    """Simple generator that yields numbers from start to end"""
    current = start
    while current <= end:
        yield current
        current += 1
        
for num in number_generator(1, 5):
    print(num)
    
def fibonacci_generator():
    """Generates Fibonacci numbers"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, b + a
    
def first_n_fibonacci(n: int):
    fib = fibonacci_generator()
    for _ in range(n):
        yield next(fib)
        
# Get first 5 Fibonacci numbers
print(list(first_n_fibonacci(5)))

class ReverseIterator:
    """Custom iterator that traverses a list in reverse"""
    def __init__(self, data: List) -> None:
        self.data = data
        self.index = len(data)
        
    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> Any:
        if self.index <= 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]
    
# Usage
numbers = [1, 2, 3, 4, 5]
reverse_iter = ReverseIterator(numbers)
print(list(reverse_iter))

numbers = [1, 2, 3, 4, 5]
squares_gen = (x * x for x in numbers) # Generator expressions
squares_list = [x * x for x in numbers] # List comprehension

print(squares_gen)  # <generator object <genexpr> at ...>
print(squares_list) # [1, 4, 9, 16, 25]

print(f"Generator size: {sys.getsizeof(squares_gen)} bytes") # 200
print(f"List size: {sys.getsizeof(squares_list)} bytes") # 120

# Generator expressions are useful when:
# 
# 1) Working with large datasets
def read_large_file(file_path: str):
    # ✅ - only loads one line at a time in memory
    lines = (line for line in open(file_path))
    
    # ❌ - loads entire file into memory
    # lines = [line for line in open(file_path)]
    
    for line in lines:
        # Do something with the line
        pass
    
# 2) You only need to iterate once
def process_sensor_data(readings):
    # ✅ Generates values on-the-fly
    processed = (reading * 1.5 for reading in readings)
    
    for value in processed:
        # Do something the value
        pass
    
# 3) Memory is a concern
def running_average(data):
    total = 0
    count = 0
    # ✅ Doesn't store all values
    squares = (x * x for x in data)
    
    for num in squares:
        total += num
        count += 1
        yield total / count
        
# List Comprehensions are useful when
#
# 1) You need to use results multiple times
def analyze_data(numbers):
    # ✅ List is reused multiple times
    squares = [x * x for x in numbers]
    
    average = sum(squares) / len(squares)
    maximum = max(squares)
    minimum = min(squares)
    
    return average, maximum, minimum

# 2) You need random access
def get_specific_items(data):
    # ✅ Can access by index
    processed = [x.upper() for x in data]
    
    first = processed[0]
    last = processed[-1]
    middle = processed[len(processed)//2]
    
    return first, middle, last

# 3) Dataset is small
def transform_small_list(items):
    # ✅ Small dataset, need full list functionality
    transformed = [item.strip().lower() for item in items]
    transformed.sort()
    transformed.reverse()
    return transformed

# Memory comparison
def compare_memory_usage(n: int) -> None:
    # Generator expression
    gen: Generator = (x * x for x in range(n))
    # List comprehension
    list: List[int] = [x * x for x in range(n)]
    
    gen_size = sys.getsizeof(gen)
    list_size = sys.getsizeof(list)
    
    print(f"{n}")
    print(f"Generator size: {gen_size} bytes")
    print(f"List size: {list_size} bytes")
    print(f"\n")
    
compare_memory_usage(1_000)
compare_memory_usage(1_000_000)

# Infinite cycle
colors = ["red", "green", "blue"]
color_cycle = cycle(colors)
print(list(islice(color_cycle, 5))) # ['red', 'green', 'blue', 'red', 'green']

# Chaining iterables
numbers = [1, 2, 3]
letters = ["a", "b", "c"]
combined = chain(numbers, letters)
print(list(combined)) # [1, 2, 3, 'a', 'b', 'c']

# Combinations
print(list(combinations(range(3), 2))) # [(0, 1), (0, 2), (1, 2)]

def advanced_generator() -> Generator[int, str, str]:
    """
    Generator[YieldType, SendType, ReturnType]
    - YieldType: Type of values yielded (int in this case)
    - SendType: Type of values that can be sent to generator (str in this case)
    - ReturnType: Type of final return value (str in this case)
    """
    # First yield
    received = yield 1
    # After yielding 1, generator pauses here waiting for send() or next()
    print(f"Received: {received}")
    
    # Second yield
    received = yield 2
    # After yielding 2, generator pauses here waiting for send() or next()
    print(f"Received: {received}")
    
    # Return final value
    return "Done"
    # Generator stops, raises StopIteration with return value

# Usage
# Create generator instance
gen = advanced_generator()

# Step 1: First next() call
first_value = next(gen)  # Starts generator, runs until first yield
print(first_value)  # Prints: 1

# Step 2: First send() call
second_value = gen.send("Hello")  # Sends "Hello" to waiting generator
# Inside generator:
# - "received" gets value "Hello"
# - Prints: "Received: Hello"
# - Yields 2
print(second_value)  # Prints: 2

# Step 3: Second send() call
try:
    gen.send("world") # Sends "World" to waiting generator
    # Inside generator:
    # - "received" gets value "World"
    # - Prints: "Received: World"
    # - Hits return statement
    # - Raises StopIteration with value "Done"
except StopIteration as error:
    print(f"Generator returned: {error.value}") # Prints: Generator returned: Done
    
def stateful_generator() -> Generator[int, str, str]:
    """Generator that maintains state between yields"""
    
    # Initialise state
    messages: List[str] = []
    
    # First state: Collect first message
    msg = yield 1 # Pause and wait for the first message
    messages.append(msg)
    print(f"Stored message 1: {msg}")
    
    # Second state: Collect second message
    msg = yield 2 # Pause and wait for second message
    messages.append(msg)
    print(f"Stored message 2: {msg}")
    
    # Final state: Return processed messages
    return f"Processed messages: {', '.join(messages)}"

# Usage with error handling
def run_stateful_generator() -> None:
    gen = stateful_generator()
    
    try:
        # Start generator
        value = next(gen)
        print(f"Generator yielded: {value}")  # 1
        
        # Send first message
        value = gen.send("Hello")
        print(f"Generator yielded: {value}")  # 2
        
        # Send second message
        gen.send("World") # Will raise StopIteration
    except StopIteration as e:
        print(f"Generator finished: {e.value}")
        
run_stateful_generator()

class DataProcessor:
    def process_stream(self) -> Generator[dict, Optional[str], list[str]]:
        """
        Process a stream of data with control commands
        - Yields: Processing status (dict)
        - Accepts: Control commands (str)
        - Returns: Processing summary (list[str])
        """
        results: List[str] = []
        
        try:
            # First state: Initialise
            command = yield { "status": "ready", "processed": 0 }
            
            while True:
                if command == "stop":
                    break
                
                # Process data
                results.append(f"Processed command: {command}")
                
                # Yield status and wait for next command
                command = yield {
                    "status": "running",
                    "processed": len(results)
                }
                
        except GeneratorExit:
            # Handle generator cleanup
            results.append("Processing terminated")
            
        return results
    
# Usage
def run_processor() -> None:
    processor = DataProcessor()
    gen = processor.process_stream()
    
    # Start processor
    status = next(gen)
    print(f"Initial status: {status}") # { "status": "ready", "processed": 0 }
    
    # Send commands
    commands = ["process_a", "process_b", "stop"]
    
    try:
        for cmd in commands:
            status = gen.send(cmd)
            print(f"Command: {cmd}, Status: {status}")
    except StopIteration as e:
        print(f"Final results: {e.value}")
        
run_processor()

def read_data() -> Generator[Dict, None, None]:
    """Simulate reading data from a source"""
    data = [
        {"id": 1, "timestamp": "2025-01-20 10:00:00", "value": 100},
        {"id": 2, "timestamp": "2025-01-20 10:01:00", "value": 200},
        # ... imagine millions of records
    ]
    
    for record in data:
        yield record
        
def parse_timestamp(records: Generator[Dict, None, None]) -> Generator[Dict, None, None]:
    """Parse timestamp strings to datetime objects"""
    for record in records:
        record["timestamp"] = datetime.strptime(record["timestamp"], '%Y-%m-%d %H:%M:%S')
        yield record
        
def filter_values(records: Generator[Dict, None, None], threshold: int) -> Generator[Dict, None, None]:
    """Filter records based on value"""
    for record in records:
        if record["value"] > threshold:
            yield record
            
# Usage: Chain the generators together
def process_data(threshold: int = 150) -> List[Dict]:
    pipeline = filter_values(parse_timestamp(read_data()), threshold)
    return list(pipeline)

# Run the pipeline
results = process_data()
for result in results:
    print(result)