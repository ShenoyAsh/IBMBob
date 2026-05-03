"""A simple calculator module for demonstration purposes."""


class Calculator:
    """Basic calculator with arithmetic operations."""
    
    def __init__(self):
        """Initialize calculator."""
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> float:
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def power(self, base: float, exponent: float) -> float:
        """Raise base to the power of exponent."""
        result = base ** exponent
        self.history.append(f"{base} ^ {exponent} = {result}")
        return result
    
    def get_history(self) -> list:
        """Return calculation history."""
        return self.history.copy()
    
    def clear_history(self):
        """Clear calculation history."""
        self.history.clear()


def calculate_average(numbers: list[float]) -> float:
    """Calculate average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)


def find_max(numbers: list[float]) -> float:
    """Find maximum value in a list."""
    if not numbers:
        raise ValueError("Cannot find max of empty list")
    return max(numbers)


def find_min(numbers: list[float]) -> float:
    """Find minimum value in a list."""
    if not numbers:
        raise ValueError("Cannot find min of empty list")
    return min(numbers)

# Made with Bob
