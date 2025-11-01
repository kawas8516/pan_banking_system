class BankAccount:
    def __init__(self, account_no, pan_number, balance, branch_name):
        self.account_no = account_no
        self.pan_number = pan_number
        self.balance = balance
        self.branch_name = branch_name

    def to_dict(self):
        return {
            "account_no": self.account_no,
            "pan_number": self.pan_number,
            "balance": self.balance,
            "branch_name": self.branch_name
        }

    def __str__(self):
        return f"Account {self.account_no} | PAN: {self.pan_number} | Balance: ₹{self.balance} | Branch: {self.branch_name}"
