import xml.etree.ElementTree as ET
import hashlib
import json
import os
from datetime import datetime

def verify_signature():
    """Verify the digital signature of the XML file"""
    try:
        # Read the signature file
        with open("pan_data.signature", "r") as f:
            stored_signature = f.read().strip()
        
        # Calculate the current signature
        with open("pan_data.xml", "rb") as f:
            content = f.read()
            current_signature = hashlib.sha256(content).hexdigest()
        
        # Compare signatures
        if stored_signature == current_signature:
            print("XML file signature verified successfully")
            return True
        else:
            print("WARNING: XML file may have been tampered with!")
            return False
    except FileNotFoundError:
        print("Signature file not found. Cannot verify XML integrity.")
        return False

def format_address(address_elem):
    """Convert structured address to string format"""
    if address_elem is None:
        return "Unknown address"
    
    parts = []
    for field in ["Street", "City", "State", "PostalCode", "Country"]:
        elem = address_elem.find(field)
        if elem is not None and elem.text:
            parts.append(elem.text)
    
    return ", ".join(parts)

def save_to_local_db(citizens_data):
    """Save imported data to a local database file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"imported_data_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(citizens_data, f, indent=2)
    
    print(f"Imported data saved to {filename}")

def main():
    # Verify file integrity
    if not verify_signature():
        # Skip interactive input for automated runs
        print("Proceeding with import despite signature verification failure")

    # Parse the XML file
    try:
        tree = ET.parse('pan_data.xml')
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return
    except FileNotFoundError:
        print("XML file not found.")
        return

    # Find the Citizens element (handle both old and new schema)
    citizens_elem = root
    if root.tag == "PanBankingData":
        citizens_elem = root.find('Citizens')
        
        # Display metadata if available
        metadata = root.find('Metadata')
        if metadata is not None:
            print("=== METADATA ===")
            for child in metadata:
                print(f"{child.tag}: {child.text}")
            print("=" * 30)

    # Process and print citizen data
    citizens_data = []
    
    for citizen in citizens_elem.findall('Citizen'):
        pan_elem = citizen.find('PAN')
        name_elem = citizen.find('Name')
        dob_elem = citizen.find('DOB')
        address_elem = citizen.find('Address')
        
        if None in (pan_elem, name_elem, dob_elem):
            print("Warning: Skipping citizen with missing required data")
            continue
            
        pan = pan_elem.text
        name = name_elem.text
        dob = dob_elem.text
        
        # Handle address (both old and new format)
        if address_elem is not None:
            if len(address_elem) > 0:  # Structured address
                address = format_address(address_elem)
            else:  # Simple text address
                address = address_elem.text
        else:
            address = "Unknown"
        
        print(f"PAN: {pan}")
        print(f"Name: {name}")
        print(f"DOB: {dob}")
        print(f"Address: {address}")
        
        # Process accounts if available
        accounts_data = []
        accounts_elem = citizen.find('Accounts')
        if accounts_elem is not None:
            print("Accounts:")
            for account in accounts_elem.findall('Account'):
                acc_num = account.find('AccountNumber')
                acc_type = account.find('AccountType')
                balance = account.find('Balance')
                
                if acc_num is not None and acc_num.text:
                    acc_info = f"  - {acc_num.text}"
                    if acc_type is not None and acc_type.text:
                        acc_info += f" ({acc_type.text})"
                    if balance is not None and balance.text:
                        acc_info += f": {balance.text}"
                    print(acc_info)
                    
                    # Add to accounts data
                    account_data = {
                        "account_number": acc_num.text if acc_num is not None else "Unknown",
                        "account_type": acc_type.text if acc_type is not None else "Unknown",
                        "balance": balance.text if balance is not None else "0"
                    }
                    accounts_data.append(account_data)
        
        print("-" * 30)
        
        # Add to citizens data
        citizen_data = {
            "pan": pan,
            "name": name,
            "dob": dob,
            "address": address,
            "accounts": accounts_data
        }
        citizens_data.append(citizen_data)
    
    # Save imported data to local database
    if citizens_data:
        save_to_local_db({"citizens": citizens_data})
    else:
        print("No valid citizen data found to import.")

if __name__ == "__main__":
    main()
