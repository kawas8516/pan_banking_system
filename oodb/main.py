from citizen import Citizen
from bank_account import BankAccount
import database

def main():
    print("=== PAN Card + Banking OODB Simulation ===")

    # Add a new citizen
    pan = input("Enter PAN number: ")
    name = input("Enter name: ")
    dob = input("Enter DOB (YYYY-MM-DD): ")
    address = input("Enter address: ")

    citizen = Citizen(pan, name, dob, address)
    database.add_citizen(citizen)
    print("Citizen added successfully!\n")

    # Search citizen
    pan_search = input("Enter PAN number to verify: ")
    found = database.find_citizen_by_pan(pan_search)
    if found:
        print("Citizen verified:", found)
    else:
        print("PAN not found!")

    # Create a bank account
    acc_no = input("Enter new account number: ")
    branch = input("Enter branch name: ")
    balance = float(input("Enter initial balance: "))

    account = BankAccount(acc_no, pan_search, balance, branch)
    database.add_account(account)
    print("Bank account created successfully!")

if __name__ == "__main__":
    main()
