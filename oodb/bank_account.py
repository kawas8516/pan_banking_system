from abc import ABC, abstractmethod
import uuid
from datetime import datetime

class Transaction:
    def __init__(self, account_no, amount, transaction_type, description=""):
        self.transaction_id = str(uuid.uuid4())
        self.account_no = account_no
        self.amount = amount
        self.transaction_type = transaction_type  # "deposit", "withdrawal", "transfer"
        self.description = description
        self.timestamp = datetime.now().isoformat()
        self.status = "completed"  # could be "pending", "completed", "failed"
        
    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "account_no": self.account_no,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "description": self.description,
            "timestamp": self.timestamp,
            "status": self.status
        }
        
    def __str__(self):
        return f"Transaction {self.transaction_id} | {self.transaction_type.capitalize()} | ₹{self.amount} | {self.timestamp}"


class BankAccount(ABC):
    """Abstract base class for all bank accounts"""
    
    def __init__(self, account_no, pan_number, balance, branch_name):
        self.account_no = account_no
        self.pan_number = pan_number
        self.balance = float(balance)
        self.branch_name = branch_name
        self.account_type = "generic"
        self.open_date = datetime.now().isoformat()
        self.status = "active"  # could be "active", "inactive", "closed"
        self.transactions = []

    def deposit(self, amount, description="Deposit"):
        """Add funds to account"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
            
        self.balance += amount
        transaction = Transaction(self.account_no, amount, "deposit", description)
        self.transactions.append(transaction)
        return transaction
        
    def withdraw(self, amount, description="Withdrawal"):
        """Remove funds from account if sufficient balance"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
            
        if amount > self.balance:
            raise ValueError("Insufficient funds")
            
        self.balance -= amount
        transaction = Transaction(self.account_no, amount, "withdrawal", description)
        self.transactions.append(transaction)
        return transaction
    
    @abstractmethod
    def calculate_interest(self):
        """Calculate interest based on account type"""
        pass
        
    def to_dict(self):
        return {
            "account_no": self.account_no,
            "pan_number": self.pan_number,
            "balance": self.balance,
            "branch_name": self.branch_name,
            "account_type": self.account_type,
            "open_date": self.open_date,
            "status": self.status
        }

    def __str__(self):
        return f"{self.account_type.capitalize()} Account {self.account_no} | PAN: {self.pan_number} | Balance: ₹{self.balance} | Branch: {self.branch_name}"


class SavingsAccount(BankAccount):
    """Savings account with interest rate"""
    
    def __init__(self, account_no, pan_number, balance, branch_name, interest_rate=3.5):
        super().__init__(account_no, pan_number, balance, branch_name)
        self.account_type = "savings"
        self.interest_rate = interest_rate
        self.min_balance = 1000  # Minimum balance requirement
        
    def calculate_interest(self):
        """Calculate yearly interest"""
        return self.balance * (self.interest_rate / 100)
        
    def withdraw(self, amount, description="Withdrawal"):
        """Override withdraw to enforce minimum balance"""
        if self.balance - amount < self.min_balance:
            raise ValueError(f"Cannot withdraw: minimum balance of ₹{self.min_balance} must be maintained")
        return super().withdraw(amount, description)
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "interest_rate": self.interest_rate,
            "min_balance": self.min_balance
        })
        return data


class CurrentAccount(BankAccount):
    """Current account for businesses with overdraft facility"""
    
    def __init__(self, account_no, pan_number, balance, branch_name, overdraft_limit=0):
        super().__init__(account_no, pan_number, balance, branch_name)
        self.account_type = "current"
        self.overdraft_limit = overdraft_limit
        self.overdraft_fee = 100  # Fee charged when using overdraft
        
    def calculate_interest(self):
        """Current accounts typically don't earn interest"""
        return 0
        
    def withdraw(self, amount, description="Withdrawal"):
        """Allow withdrawals up to overdraft limit"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
            
        if amount > (self.balance + self.overdraft_limit):
            raise ValueError(f"Exceeds available balance and overdraft limit of ₹{self.overdraft_limit}")
            
        # Apply overdraft fee if withdrawal exceeds balance
        if amount > self.balance:
            description += " (with overdraft)"
            # Add overdraft fee transaction
            fee_transaction = Transaction(
                self.account_no, 
                self.overdraft_fee, 
                "fee", 
                "Overdraft fee"
            )
            self.transactions.append(fee_transaction)
            self.balance -= self.overdraft_fee
            
        self.balance -= amount
        transaction = Transaction(self.account_no, amount, "withdrawal", description)
        self.transactions.append(transaction)
        return transaction
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "overdraft_limit": self.overdraft_limit,
            "overdraft_fee": self.overdraft_fee
        })
        return data


class FixedDepositAccount(BankAccount):
    """Fixed deposit account with maturity date and penalty for early withdrawal"""
    
    def __init__(self, account_no, pan_number, balance, branch_name, term_months=12, interest_rate=6.5):
        super().__init__(account_no, pan_number, balance, branch_name)
        self.account_type = "fixed_deposit"
        self.term_months = term_months
        self.interest_rate = interest_rate
        self.maturity_date = self._calculate_maturity_date()
        self.early_withdrawal_penalty = 1.0  # Percentage penalty
        
    def _calculate_maturity_date(self):
        """Calculate maturity date based on term"""
        open_date = datetime.fromisoformat(self.open_date)
        maturity_month = open_date.month + self.term_months
        maturity_year = open_date.year + (maturity_month - 1) // 12
        maturity_month = ((maturity_month - 1) % 12) + 1
        maturity_date = datetime(maturity_year, maturity_month, open_date.day)
        return maturity_date.isoformat()
        
    def calculate_interest(self):
        """Calculate interest at maturity"""
        return self.balance * (self.interest_rate / 100) * (self.term_months / 12)
        
    def withdraw(self, amount, description="Withdrawal"):
        """Apply penalty for early withdrawal before maturity"""
        if datetime.now().isoformat() < self.maturity_date:
            penalty_amount = amount * (self.early_withdrawal_penalty / 100)
            description += f" (Early withdrawal penalty: ₹{penalty_amount})"
            
            # Add penalty transaction
            penalty_transaction = Transaction(
                self.account_no, 
                penalty_amount, 
                "fee", 
                "Early withdrawal penalty"
            )
            self.transactions.append(penalty_transaction)
            self.balance -= penalty_amount
            
        return super().withdraw(amount, description)
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "term_months": self.term_months,
            "interest_rate": self.interest_rate,
            "maturity_date": self.maturity_date,
            "early_withdrawal_penalty": self.early_withdrawal_penalty
        })
        return data
