from citizen import Citizen
from bank_account import SavingsAccount, CurrentAccount, FixedDepositAccount, Transaction
import database
import sys

def display_menu():
    """Display the main menu options"""
    print("\n=== PAN Card + Banking OODB System ===")
    print("1. Add New Citizen")
    print("2. Search Citizen by PAN")
    print("3. Create Bank Account")
    print("4. View Account Details")
    print("5. Deposit Money")
    print("6. Withdraw Money")
    print("7. Update Citizen Information")
    print("8. List All Citizens")
    print("9. List All Accounts")
    print("0. Exit")
    try:
        return input("Enter your choice: ")
    except EOFError:
        print("Exiting due to input error...")
        return "0"

def add_citizen():
    """Add a new citizen to the database"""
    print("\n=== Add New Citizen ===")
    try:
        pan = input("Enter PAN number (format ABCDE1234F): ")
        name = input("Enter name: ")
        dob = input("Enter DOB (YYYY-MM-DD): ")
        address = input("Enter address: ")

        citizen = Citizen(pan, name, dob, address)
        database.add_citizen(citizen)
        print("✅ Citizen added successfully!")
    except ValueError as e:
        print(f"❌ Error: {e}")
    except database.DatabaseError as e:
        print(f"❌ Database error: {e}")

def search_citizen():
    """Search for a citizen by PAN number"""
    print("\n=== Search Citizen ===")
    pan_search = input("Enter PAN number to search: ")
    try:
        found = database.find_citizen_by_pan(pan_search)
        if found:
            print("✅ Citizen found:")
            print(f"PAN: {found['pan_number']}")
            print(f"Name: {found['name']}")
            print(f"DOB: {found['dob']}")
            print(f"Address: {found['address']}")
            
            # Show linked accounts
            accounts = database.get_accounts_by_pan(pan_search)
            if accounts:
                print(f"\nLinked Accounts ({len(accounts)}):")
                for acc in accounts:
                    print(f"- {acc['account_no']} ({acc['account_type'].capitalize()}) | Balance: ₹{acc['balance']}")
        else:
            print("❌ PAN not found!")
    except database.DatabaseError as e:
        print(f"❌ Database error: {e}")

def create_account():
    """Create a new bank account"""
    print("\n=== Create Bank Account ===")
    pan_number = input("Enter PAN number of account holder: ")
    
    try:
        # Verify citizen exists
        citizen = database.find_citizen_by_pan(pan_number)
        if not citizen:
            print("❌ PAN not found! Please register the citizen first.")
            return
            
        acc_no = input("Enter new account number: ")
        branch = input("Enter branch name: ")
        
        print("\nSelect Account Type:")
        print("1. Savings Account")
        print("2. Current Account")
        print("3. Fixed Deposit")
        acc_type = input("Enter choice (1-3): ")
        
        balance = float(input("Enter initial balance: ₹"))
        
        if acc_type == "1":
            interest_rate = float(input("Enter interest rate (default 3.5%): ") or "3.5")
            account = SavingsAccount(acc_no, pan_number, balance, branch, interest_rate)
        elif acc_type == "2":
            overdraft = float(input("Enter overdraft limit (default 0): ₹") or "0")
            account = CurrentAccount(acc_no, pan_number, balance, branch, overdraft)
        elif acc_type == "3":
            term = int(input("Enter term in months (default 12): ") or "12")
            interest_rate = float(input("Enter interest rate (default 6.5%): ") or "6.5")
            account = FixedDepositAccount(acc_no, pan_number, balance, branch, term, interest_rate)
        else:
            print("❌ Invalid account type selected!")
            return
            
        database.add_account(account)
        print(f"✅ {account.account_type.capitalize()} account created successfully!")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    except database.DatabaseError as e:
        print(f"❌ Database error: {e}")

def view_account():
    """View account details"""
    print("\n=== View Account Details ===")
    acc_no = input("Enter account number: ")
    
    try:
        account = database.find_account_by_number(acc_no)
        if account:
            print(f"\nAccount Type: {account['account_type'].capitalize()}")
            print(f"Account Number: {account['account_no']}")
            print(f"PAN: {account['pan_number']}")
            print(f"Balance: ₹{account['balance']}")
            print(f"Branch: {account['branch_name']}")
            print(f"Status: {account['status']}")
            print(f"Open Date: {account['open_date']}")
            
            # Show account-specific details
            if account['account_type'] == "savings":
                print(f"Interest Rate: {account.get('interest_rate', 'N/A')}%")
                print(f"Minimum Balance: ₹{account.get('min_balance', 'N/A')}")
            elif account['account_type'] == "current":
                print(f"Overdraft Limit: ₹{account.get('overdraft_limit', 'N/A')}")
            elif account['account_type'] == "fixed_deposit":
                print(f"Term: {account.get('term_months', 'N/A')} months")
                print(f"Interest Rate: {account.get('interest_rate', 'N/A')}%")
                print(f"Maturity Date: {account.get('maturity_date', 'N/A')}")
        else:
            print("❌ Account not found!")
    except database.DatabaseError as e:
        print(f"❌ Database error: {e}")

def deposit_money():
    """Deposit money into an account"""
    print("\n=== Deposit Money ===")
    acc_no = input("Enter account number: ")
    
    try:
        account_data = database.find_account_by_number(acc_no)
        if not account_data:
            print("❌ Account not found!")
            return
            
        amount = float(input("Enter deposit amount: ₹"))
        description = input("Enter description (optional): ") or "Deposit"
        
        # Create appropriate account object based on type
        if account_data['account_type'] == "savings":
            account = SavingsAccount(
                account_data['account_no'],
                account_data['pan_number'],
                account_data['balance'],
                account_data['branch_name']
            )
        elif account_data['account_type'] == "current":
            account = CurrentAccount(
                account_data['account_no'],
                account_data['pan_number'],
                account_data['balance'],
                account_data['branch_name'],
                account_data.get('overdraft_limit', 0)
            )
        elif account_data['account_type'] == "fixed_deposit":
            account = FixedDepositAccount(
                account_data['account_no'],
                account_data['pan_number'],
                account_data['balance'],
                account_data['branch_name'],
                account_data.get('term_months', 12),
                account_data.get('interest_rate', 6.5)
            )
        else:
            print("❌ Unknown account type!")
            return
            
        # Perform deposit
        transaction = account.deposit(amount, description)
        
        # Update account in database
        database.update_account(acc_no, account.to_dict())
        
        # Record transaction
        database.record_transaction(transaction)
        
        print(f"✅ Deposited ₹{amount} successfully!")
        print(f"New Balance: ₹{account.balance}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    except database.DatabaseError as e:
        print(f"❌ Database error: {e}")

def withdraw_money():
    """Withdraw money from an account"""
    print("\n=== Withdraw Money ===")
    acc_no = input("Enter account number: ")
    
    try:
        account_data = database.find_account_by_number(acc_no)
        if not account_data:
            print("❌ Account not found!")
            return
            
        amount = float(input("Enter withdrawal amount: ₹"))
        description = input("Enter description (optional): ") or "Withdrawal"
        
        # Create appropriate account object based on type
        if account_data['account_type'] == "savings":
            account = SavingsAccount(
                account_data['account_no'],
                account_data['pan_number'],
                account_data['balance'],
                account_data['branch_name'],
                account_data.get('interest_rate', 3.5)
            )
            account.min_balance = account_data.get('min_balance', 1000)
        elif account_data['account_type'] == "current":
            account = CurrentAccount(
                account_data['account_no'],
                account_data['pan_number'],
                account_data['balance'],
                account_data['branch_name'],
                account_data.get('overdraft_limit', 0)
            )
        elif account_data['account_type'] == "fixed_deposit":
            account = FixedDepositAccount(
                account_data['account_no'],
                account_data['pan_number'],
                account_data['balance'],
                account_data['branch_name'],
                account_data.get('term_months', 12),
                account_data.get('interest_rate', 6.5)
            )
        else:
            print("❌ Unknown account type!")
            return
            
        # Perform withdrawal
        transaction = account.withdraw(amount, description)
        
        # Update account in database
        database.update_account(acc_no, account.to_dict())
        
        # Record transaction
        database.record_transaction(transaction)
        
        print(f"✅ Withdrew ₹{amount} successfully!")
        print(f"New Balance: ₹{account.balance}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    except database.DatabaseError as e:
        print(f"❌ Database error: {e}")

def update_citizen_info():
    """Update citizen information"""
    print("\n=== Update Citizen Information ===")
    pan = input("Enter PAN number: ")
    
    try:
        citizen = database.find_citizen_by_pan(pan)
        if not citizen:
            print("❌ PAN not found!")
            return
            
        print(f"Current Name: {citizen['name']}")
        print(f"Current DOB: {citizen['dob']}")
        print(f"Current Address: {citizen['address']}")
        
        print("\nEnter new information (leave blank to keep current):")
        name = input("Name: ") or citizen['name']
        dob = input("DOB (YYYY-MM-DD): ") or citizen['dob']
        address = input("Address: ") or citizen['address']
        
        updated_citizen = {
            "pan_number": pan,
            "name": name,
            "dob": dob,
            "address": address
        }
        
        if database.update_citizen(pan, updated_citizen):
            print("✅ Citizen information updated successfully!")
        else:
            print("❌ Failed to update citizen information!")
            
    except database.DatabaseError as e:
        print(f"❌ Database error: {e}")

def list_all_citizens():
    """List all citizens in the database"""
    print("\n=== All Citizens ===")
    try:
        citizens = database.get_all_citizens()
        if not citizens:
            print("No citizens found in database.")
            return
            
        print(f"Total Citizens: {len(citizens)}\n")
        for i, citizen in enumerate(citizens, 1):
            print(f"{i}. {citizen['name']} | PAN: {citizen['pan_number']} | DOB: {citizen['dob']}")
    except database.DatabaseError as e:
        print(f"❌ Database error: {e}")

def list_all_accounts():
    """List all accounts in the database"""
    print("\n=== All Accounts ===")
    try:
        accounts = database.get_all_accounts()
        if not accounts:
            print("No accounts found in database.")
            return
            
        print(f"Total Accounts: {len(accounts)}\n")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. {account['account_type'].capitalize()} Account {account['account_no']} | PAN: {account['pan_number']} | Balance: ₹{account['balance']}")
    except database.DatabaseError as e:
        print(f"❌ Database error: {e}")

def main():
    """Main function to run the application"""
    while True:
        choice = display_menu()
        
        if choice == "1":
            add_citizen()
        elif choice == "2":
            search_citizen()
        elif choice == "3":
            create_account()
        elif choice == "4":
            view_account()
        elif choice == "5":
            deposit_money()
        elif choice == "6":
            withdraw_money()
        elif choice == "7":
            update_citizen_info()
        elif choice == "8":
            list_all_citizens()
        elif choice == "9":
            list_all_accounts()
        elif choice == "0":
            print("Thank you for using the PAN Banking System!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
