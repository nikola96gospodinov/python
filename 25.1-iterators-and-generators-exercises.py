from typing import List, Iterator, Any, Generator, Optional
import math

class PaginatedData:
    def __init__(self, data: List, take: int = 10, current_page: int = 1) -> None:
        self._data: List = data
        self._take = 10
        self._current_page = 1
        
        self.take = take
        self.current_page = current_page
        
        self._index = take * current_page - take
        
    @property
    def take(self) -> int:
        raise AttributeError("This property is not accessible")

    @take.setter
    def take(self, value):
        if value <= 0:
            raise ValueError("Items per page must be greater than 0")
        
        self._take = value
        
    @property
    def current_page(self) -> int:
        raise AttributeError("This property is not accessible")
    
    @current_page.setter
    def current_page(self, value):
        if value < 1:
            raise ValueError("Current page must be greater than 0")
        
        self._current_page = value
        
    @property
    def total_pages(self) -> int:
        return math.ceil(len(self._data) / self._take)
    
    @property
    def has_next_page(self) -> bool:
        if len(self._data) == 0:
            print("There isn't any data")
            return False
        
        if self._index >= len(self._data):
            print("You've reached the end")
            return False
        
        return True
    
    @property
    def has_previous_page(self) -> bool:
        if self._index <= self._take:
            return False
        
        return True
    
    @property
    def current_page_items(self) -> List[Any]:
        start = self._take * (self._current_page - 1)
        end = min(start + self._take, len(self._data))
        return self._data[start:end]
    
    @property
    def page_info(self):
        return {
            "Current page": self._current_page,
            "Total pages": self.total_pages,
            "Items per page": self._take,
            "Total items": len(self._data),
            "Has next page": self.has_next_page,
            "Has previous page": self.has_previous_page
        }
        
    def __iter__(self) -> Iterator:
        return self
    
    def __next__(self) -> Any:
        if not self.has_next_page:
            raise StopIteration
            
        if self._index >= self._take * self._current_page:
            raise StopIteration
            
        value = self._data[self._index]
        self._index += 1
        return value
        
    def go_to_page(self, page: int) -> None:
        if page < 1:
            raise ValueError("Can't be less than 1")
        
        if page > self.total_pages:
            raise ValueError(f"Can't be greater than {self.total_pages}")
        
        self._current_page = page
        self._index = self._take * page - self._take
        
    
data = list(range(1, 101))  # 1 to 100
paginator = PaginatedData(data)

for item in paginator:
    print(item)   
    
paginator.go_to_page(5)

for item in paginator:
    print(item)