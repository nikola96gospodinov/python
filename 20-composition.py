class Engine:
    def __init__(self, horsepower) -> None:
        self._horsepower = horsepower
        
    def start(self):
        return "Engine started"
    
    def stop(self):
        return "Engine stopped"
    
class Wheels:
    def __init__(self, size) -> None:
        self._size = size
    
    def rotate(self):
        return f"Rotating {self._size} inch wheels"
    
class Car:
    def __init__(self, engine: Engine, wheels: list[Wheels]) -> None:
        # Car is composed of an engine and wheels
        self.engine = engine
        self.wheels = wheels
        
    def start_car(self):
        status = self.engine.start()
        return f"Car starting: {status}"
    
    def drive(self):
        wheel_status = [wheel.rotate() for wheel in self.wheels]
        return f"Car driving: {', '.join(wheel_status)}"
    
car_engine = Engine(300)
car_wheels = [Wheels(18) for _ in range(4)]
my_car = Car(car_engine, car_wheels)

print(my_car.start_car())
print(my_car.drive())