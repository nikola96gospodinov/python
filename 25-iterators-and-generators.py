from typing import Generator

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