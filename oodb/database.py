import json
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='database_operations.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DB_FILE = "oodb/database.json"
BACKUP_DIR = "backups"

class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass

def validate_pan(pan_number):
    """Validate PAN number format (e.g., ABCDE1234F)"""
    if not pan_number or len(pan_number) != 10:
        return False
    # First 5 chars should be letters, next 4 digits, last char letter
    if not (pan_number[:5].isalpha() and 
            pan_number[5:9].isdigit() and 
            pan_number[9].isalpha()):
        return False
    return True

def validate_account_number(account_no):
    """Validate account number (simple validation)"""
    if not account_no or len(account_no) < 8:
        return False
    return account_no.isalnum()

def create_backup():
    """Create a backup of the current database"""
    if not os.path.exists(DB_FILE):
        return
        
    # Create backup directory if it doesn't exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"database_backup_{timestamp}.json")
    
    try:
        with open(DB_FILE, "r") as src, open(backup_file, "w") as dst:
            dst.write(src.read())
        logging.info(f"Database backup created: {backup_file}")
    except Exception as e:
        logging.error(f"Backup failed: {str(e)}")

def load_database():
    """Load database with error handling"""
    try:
        if not os.path.exists(DB_FILE):
            return {"citizens": [], "accounts": [], "transactions": []}
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            # Ensure all required keys exist
            if "citizens" not in data:
                data["citizens"] = []
            if "accounts" not in data:
                data["accounts"] = []
            if "transactions" not in data:
                data["transactions"] = []
            return data
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding database: {str(e)}")
        raise DatabaseError(f"Database file is corrupted: {str(e)}")
    except Exception as e:
        logging.error(f"Error loading database: {str(e)}")
        raise DatabaseError(f"Failed to load database: {str(e)}")

def save_database(data):
    """Save database with transaction support"""
    try:
        # Create a backup before saving
        create_backup()
        
        # Write to a temporary file first
        temp_file = f"{DB_FILE}.tmp"
        with open(temp_file, "w") as f:
            json.dump(data, f, indent=4)
            
        # Rename the temp file to the actual file (atomic operation)
        os.replace(temp_file, DB_FILE)
        logging.info("Database saved successfully")
    except Exception as e:
        logging.error(f"Error saving database: {str(e)}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise DatabaseError(f"Failed to save database: {str(e)}")

def add_citizen(citizen):
    """Add a new citizen with validation"""
    if not validate_pan(citizen.pan_number):
        logging.warning(f"Invalid PAN format: {citizen.pan_number}")
        raise ValueError("Invalid PAN number format")
        
    # Check if PAN already exists
    existing = find_citizen_by_pan(citizen.pan_number)
    if existing:
        logging.warning(f"Duplicate PAN: {citizen.pan_number}")
        raise ValueError(f"Citizen with PAN {citizen.pan_number} already exists")
    
    try:
        db = load_database()
        db["citizens"].append(citizen.to_dict())
        save_database(db)
        logging.info(f"Citizen added: {citizen.pan_number}")
        return True
    except Exception as e:
        logging.error(f"Failed to add citizen: {str(e)}")
        raise DatabaseError(f"Failed to add citizen: {str(e)}")

def add_account(account):
    """Add a new bank account with validation"""
    if not validate_account_number(account.account_no):
        logging.warning(f"Invalid account number: {account.account_no}")
        raise ValueError("Invalid account number format")
        
    # Check if account already exists
    existing = find_account_by_number(account.account_no)
    if existing:
        logging.warning(f"Duplicate account number: {account.account_no}")
        raise ValueError(f"Account {account.account_no} already exists")
    
    # Verify PAN exists
    citizen = find_citizen_by_pan(account.pan_number)
    if not citizen:
        logging.warning(f"PAN not found: {account.pan_number}")
        raise ValueError(f"No citizen found with PAN {account.pan_number}")
    
    try:
        db = load_database()
        db["accounts"].append(account.to_dict())
        save_database(db)
        logging.info(f"Account added: {account.account_no}")
        return True
    except Exception as e:
        logging.error(f"Failed to add account: {str(e)}")
        raise DatabaseError(f"Failed to add account: {str(e)}")

def find_citizen_by_pan(pan_number):
    """Find citizen by PAN number"""
    try:
        db = load_database()
        for c in db["citizens"]:
            if c["pan_number"] == pan_number:
                return c
        return None
    except Exception as e:
        logging.error(f"Error finding citizen: {str(e)}")
        raise DatabaseError(f"Failed to search for citizen: {str(e)}")

def find_account_by_number(account_no):
    """Find account by account number"""
    try:
        db = load_database()
        for a in db["accounts"]:
            if a["account_no"] == account_no:
                return a
        return None
    except Exception as e:
        logging.error(f"Error finding account: {str(e)}")
        raise DatabaseError(f"Failed to search for account: {str(e)}")

def update_citizen(pan_number, updated_data):
    """Update citizen information"""
    try:
        db = load_database()
        for i, citizen in enumerate(db["citizens"]):
            if citizen["pan_number"] == pan_number:
                # Don't allow changing the PAN number
                updated_data["pan_number"] = pan_number
                db["citizens"][i] = updated_data
                save_database(db)
                logging.info(f"Citizen updated: {pan_number}")
                return True
        logging.warning(f"Update failed - PAN not found: {pan_number}")
        return False
    except Exception as e:
        logging.error(f"Error updating citizen: {str(e)}")
        raise DatabaseError(f"Failed to update citizen: {str(e)}")

def update_account(account_no, updated_data):
    """Update account information"""
    try:
        db = load_database()
        for i, account in enumerate(db["accounts"]):
            if account["account_no"] == account_no:
                # Don't allow changing the account number
                updated_data["account_no"] = account_no
                db["accounts"][i] = updated_data
                save_database(db)
                logging.info(f"Account updated: {account_no}")
                return True
        logging.warning(f"Update failed - Account not found: {account_no}")
        return False
    except Exception as e:
        logging.error(f"Error updating account: {str(e)}")
        raise DatabaseError(f"Failed to update account: {str(e)}")

def delete_citizen(pan_number):
    """Delete a citizen by PAN number"""
    try:
        db = load_database()
        initial_count = len(db["citizens"])
        db["citizens"] = [c for c in db["citizens"] if c["pan_number"] != pan_number]
        
        if len(db["citizens"]) < initial_count:
            save_database(db)
            logging.info(f"Citizen deleted: {pan_number}")
            return True
        logging.warning(f"Delete failed - PAN not found: {pan_number}")
        return False
    except Exception as e:
        logging.error(f"Error deleting citizen: {str(e)}")
        raise DatabaseError(f"Failed to delete citizen: {str(e)}")

def delete_account(account_no):
    """Delete an account by account number"""
    try:
        db = load_database()
        initial_count = len(db["accounts"])
        db["accounts"] = [a for a in db["accounts"] if a["account_no"] != account_no]
        
        if len(db["accounts"]) < initial_count:
            save_database(db)
            logging.info(f"Account deleted: {account_no}")
            return True
        logging.warning(f"Delete failed - Account not found: {account_no}")
        return False
    except Exception as e:
        logging.error(f"Error deleting account: {str(e)}")
        raise DatabaseError(f"Failed to delete account: {str(e)}")

def record_transaction(transaction):
    """Record a transaction in the database"""
    try:
        db = load_database()
        db["transactions"].append(transaction.to_dict())
        save_database(db)
        logging.info(f"Transaction recorded: {transaction.transaction_id}")
        return True
    except Exception as e:
        logging.error(f"Error recording transaction: {str(e)}")
        raise DatabaseError(f"Failed to record transaction: {str(e)}")

def get_all_citizens():
    """Get all citizens"""
    try:
        db = load_database()
        return db["citizens"]
    except Exception as e:
        logging.error(f"Error retrieving citizens: {str(e)}")
        raise DatabaseError(f"Failed to retrieve citizens: {str(e)}")

def get_all_accounts():
    """Get all accounts"""
    try:
        db = load_database()
        return db["accounts"]
    except Exception as e:
        logging.error(f"Error retrieving accounts: {str(e)}")
        raise DatabaseError(f"Failed to retrieve accounts: {str(e)}")

def get_accounts_by_pan(pan_number):
    """Get all accounts for a specific PAN"""
    try:
        db = load_database()
        return [a for a in db["accounts"] if a["pan_number"] == pan_number]
    except Exception as e:
        logging.error(f"Error retrieving accounts by PAN: {str(e)}")
        raise DatabaseError(f"Failed to retrieve accounts: {str(e)}")
