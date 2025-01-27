from functools import cached_property
from typing import Dict

class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius: float = 0
        
        self.celsius = celsius
        
    @property
    def celsius(self) -> float:
        """Get the celsius"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float):
        """Set the celsius"""
        if not isinstance(value, (int, float)):
            raise TypeError("Must be a number")
        if value < -273.15:
            raise ValueError("Must be above -273.15°C")
        
        self._celsius = value
        
    @cached_property
    def fahrenheit(self) -> float:
        """Get current fahrenheit"""
        return self._celsius * (9/5) + 32
    
    @classmethod
    def from_fahrenheit(cls, fahrenheit: float) -> "Temperature":
        """Create an instance from fahrenheit"""
        celsius = (fahrenheit - 32) * (5/9)
        return cls(celsius)
    
class Room:
    def __init__(self, name: str, current_temp: Temperature, target_temp: Temperature) -> None:
        self._name = ""
        self._current_temp: Temperature | None = None
        self._target_temp: Temperature | None = None
        
        self.name = name
        self.current_temp = current_temp
        self.target_temp = target_temp
        
    @property
    def current_temp(self):
        return self._current_temp
    
    @current_temp.setter
    def current_temp(self, value: Temperature):
        if not isinstance(value, Temperature):
            raise TypeError("Make sure you pass Temperature")
        
        self._current_temp = value
        
    @property
    def target_temp(self):
        return self._target_temp
    
    @target_temp.setter
    def target_temp(self, value: Temperature):
        if not isinstance(value, Temperature):
            raise TypeError("Make sure you pass Temperature")
        
        self._target_temp = value
        
    @property
    def temperature_difference(self) -> float:
        if self._current_temp and self._target_temp:
            return self._current_temp.celsius - self._target_temp.celsius
        return 0.0
    
class SmartThermostat:
    def __init__(self):
        self._rooms: Dict[str, Room] = {}
        
    @cached_property
    def average_temp(self) -> float:
        """Calculate average temperature across all rooms"""
        if not self._rooms:
            return 0.0
        return sum(room.current_temp.celsius for room in self._rooms.values()) / len(self._rooms)
    
    @staticmethod
    def is_temperature_safe(temp: Temperature) -> bool:
        return temp.celsius < 8 or temp.celsius > 36
    
    