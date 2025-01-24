from typing import List

class BankAccount:
    def __init__(self, account_number, balance=0) -> None:
        # Private attributes (by convention with _)
        self._account_number = account_number
        self._balance = 0 # Start with 0
        self._transaction_history: List = []
        
        self.balance = balance # This calls the setter which may includes validation
        
    @property
    def account_number(self):
        """Read-only account number"""
        return self._account_number
    
    @property
    def balance(self):
        """Get current balance"""
        return self._balance
    
    @balance.setter
    def balance(self, value):
        """Set balance with validation"""
        if not isinstance(value, (int, float)):
            raise TypeError("Balance must be a number")
        if value < 0:
            raise ValueError("Balance cannot be negative")
        
        self._balance = value
        self._add_to_history(f"Balance updated to ${value}")
        
    @property
    def transaction_history(self):
        """Return a copy of history to prevent modification"""
        return self._transaction_history.copy()
    
    def deposit(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a number")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        self.balance += amount
        self._add_to_history(f"Deposited £{amount}")
        return f"Deposited £{amount}"
    
    def withdraw(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a number")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount
        self._add_to_history(f"Withdrew £{amount}")
        return f"Withdrew £{amount}"
    
    def _add_to_history(self, transaction):
        """Private method for adding to transaction history"""
        self._transaction_history.append(transaction)

try:
    account = BankAccount("1234", 1000)
    
    print(account.balance)
    print(account.account_number)
    
    account.deposit(500)
    account.withdraw(200)
    
    # Try invalid operations
    # account.balance = -100       # Raises ValueError
    # account.withdraw(2000)       # Raises ValueError
    # account._balance = -100      # Possible but shouldn't do it (protected attribute)
    
    for transaction in account.transaction_history:
        print(transaction)
    
except(ValueError, TypeError) as error:
    print(f"Error: {error}")