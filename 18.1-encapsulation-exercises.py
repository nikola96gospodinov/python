class Temperature:
    def __init__(self, celsius=0) -> None:
        self._celsius = 0
        
        self.celsius = celsius
        
    @property
    def celsius(self):
        """Get current celsius"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """Set celsius with validation"""
        if not isinstance(value, (int, float)):
            raise TypeError("Must be a number")
        if value < -273.15:
            raise ValueError("Must be above -273.15°C")
        
        self._celsius = value
        
    @property
    def fahrenheit(self):
        """Get current fahrenheit"""
        return self._celsius * (9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set fahrenheit"""
        self.celsius = (value - 32) * (5/9)
        
    @property
    def kelvin(self):
        """Get current kelvin"""
        return self._celsius + 273.15
    
    @kelvin.setter
    def kelvin(self, value):
        """Set kelvin"""
        self.celsius = value - 273.15