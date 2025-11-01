import json
import os

DB_FILE = "database.json"

def load_database():
    if not os.path.exists(DB_FILE):
        return {"citizens": [], "accounts": []}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_database(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_citizen(citizen):
    db = load_database()
    db["citizens"].append(citizen.to_dict())
    save_database(db)

def add_account(account):
    db = load_database()
    db["accounts"].append(account.to_dict())
    save_database(db)

def find_citizen_by_pan(pan_number):
    db = load_database()
    for c in db["citizens"]:
        if c["pan_number"] == pan_number:
            return c
    return None
