x = 10
y = 3

print(f"Addition {y + x}")
print(f"Subtraction {x - y}")
print(f"Multiplication {x * y}")
print(f"Division {x / y}")
print(f"Floor division {x // y}")
print(f"Modulus {x % y}")
print(f"Exponent {x ** y}")

# Rounding numbers for display
print(f"{x / y :.2f}")

# Rounding numbers for calculations
rounded_number = round(x / y, 2)
calculation = rounded_number * 0.1
print(f"{calculation:.2f}")