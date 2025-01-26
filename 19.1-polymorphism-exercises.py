from typing import List

class Shape:
    def area(self):
        raise NotImplementedError
    
    def perimeter(Self):
        raise NotImplementedError
    
class Circle(Shape):
    def __init__(self, radius) -> None:
        super().__init__()
        self._radius = 0
        
        self.radius = radius
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Radius must be a number")
        if value <= 0:
            raise ValueError("Radius must be a positive number")
        
        self._radius = value
        
    def area(self):
        return 3.14 * (self._radius ** 2)
    
    def perimeter(self):
        return 2 * 3.14 * self._radius
    
class Rectangle(Shape):
    def __init__(self, width, height) -> None:
        super().__init__()
        self._width = 0
        self._height = 0
        
        self.width = width
        self.height = height
        
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Width must be a number")
        if value <= 0:
            raise ValueError("Width must be a positive number") 
        
        self._width = value
        
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Height must be a number")
        if value <= 0:
            raise ValueError("Height must be a positive number")
        
        self._height = value
        
    def area(self):
        return self._height * self._width
    
    def perimeter(self):
        return 2 * (self._height * self._width)
    
class Triangle(Shape):
    def __init__(self, base, height, sides) -> None:
        super().__init__()
        self._base = 0
        self._height = 0
        self._sides = (0, 0)
        
        self.base = base
        self.height = height
        self.sides = sides
        
    @property
    def base(self):
        return self._base
    
    @base.setter
    def base(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Base must be a number")
        if value <= 0:
            raise ValueError("Base must be a positive number") 
        
        self._base = value
        
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Height must be a number")
        if value <= 0:
            raise ValueError("Height must be a positive number") 
        
        self._height = value
        
    @property
    def sides(self):
        return self._sides
    
    @sides.setter
    def sides(self, value):
        if not isinstance(value, tuple):
            raise TypeError("Sides must be a tuple")
        if len(value) != 2:
            raise ValueError("Sides must contain exactly 2 values")
        if not all(isinstance(side, (int, float)) for side in value):
            raise TypeError("Both sides must be numbers")
        if not all(side > 0 for side in value):
            raise ValueError("Both sides must be positive numbers")
            
        self._sides = value
        
    def area(self):
        return (self._base * self._height) / 2
    
    def perimeter(self):
        return self._base + sum(self._sides)
    
class Square(Rectangle):
    def __init__(self, side) -> None:
        super().__init__(side, side)
        self._side = side
        
        self.side = side
        
    @property
    def side(self):
        return self._side
    
    @side.setter
    def side(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Side must be a number")
        if value <= 0:
            raise ValueError("Side must be a positive number")
        
        self._side = value
        
    def area(self):
        return self._side ** 2
    
    def perimeter(self):
        return self._side * 4
    
# Function
def shape_calculator(shapes: List[Shape]):
    all_areas = [shape.area() for shape in shapes]
    total_area = sum(all_areas)
    largest_area = max(all_areas)
    
    all_perimeters = [shape.perimeter() for shape in shapes]
    total_perimeter = sum(all_perimeters)
    largest_perimeter = max(all_perimeters)
    
    return {
        "total_area": total_area,
        "largest_area": largest_area,
        "total_perimeter": total_perimeter,
        "largest_perimeter": largest_perimeter
    }
    
# Class
class ShapeCalculator:
    def __init__(self) -> None:
        self._shapes: List[Shape] = []
        
    def add_shape(self, shape):
        """Add a shape"""
        if not isinstance(shape, Shape):
            raise TypeError("Make sure you pass a shape")
        
        self._shapes.append(shape)
        
    def remove_shape(self, shape):
        """Remove a shape"""
        if not isinstance(shape, Shape):
            raise TypeError("Make sure you pass a shape")
        
        self._shapes.remove(shape)
        
    @property
    def total_area(self):
        """Get total area"""
        return sum(shape.area() for shape in self._shapes)
    
    @property
    def largest_area(self):
        """Get the largest area"""
        if len(self._shapes) == 0:
            raise ValueError("No shapes added to calculator")
        
        return max(self._shapes, key=lambda shape: shape.area())
    
    @property
    def total_perimeter(self):
        """Get total perimeter"""
        return sum(shape.perimeter() for shape in self._shapes)
    
    @property
    def largest_perimeter(self):
        """Get the largest perimeter"""
        if len(self._shapes) == 0:
            raise ValueError("No shapes added to calculator")
        
        return max(self._shapes, key=lambda shape: shape.perimeter()) 
    
    def generate_report(self):
        """Generate a report of all shapes"""
        if not self._shapes:
            return "No shapes to report"
        
        report = "Shape Calculator Report\n"
        report += "=====================\n"
        report += f"Total shapes: {len(self._shapes)}\n"
        report += f"Total area: {self.total_area}\n"
        report += f"Total perimeter: {self.total_perimeter}\n"
        report += "\nIndividual Shapes:\n"
        
        for i, shape in enumerate(self._shapes, 1):
            report += f"{i}. {shape.__class__.__name__}:\n"
            report += f"   Area: {shape.area()}\n"
            report += f"   Perimeter: {shape.perimeter()}\n"
        
        return report
    
if __name__ == "__main__":    
    calculator = ShapeCalculator()
    circle = Circle(5)
    rectangle = Rectangle(4, 6)
    square = Square(4)
    triangle = Triangle(3, 4, (5, 5))

    try:
        calculator.add_shape(circle)
        calculator.add_shape(rectangle)
        calculator.add_shape(square)
        calculator.add_shape(triangle)
        
        print(f"Total Area: {calculator.total_area}")
        print(f"Total Perimeter: {calculator.total_perimeter}")
        
        print("\n" + calculator.generate_report())
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")