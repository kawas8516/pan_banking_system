import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from datetime import datetime
import os
import hashlib
import base64

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element"""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def encrypt_sensitive_data(text, key="banking_system"):
    """Simple encryption for demonstration purposes"""
    # In a real system, use proper encryption libraries
    key_hash = hashlib.md5(key.encode()).digest()
    encoded = base64.b64encode(text.encode())
    return encoded.decode()

def format_address(address_str):
    """Convert flat address string to structured address"""
    # This is a simplified example - in a real system, you'd use address parsing
    parts = address_str.split(',')
    
    address = {
        "Street": parts[0].strip() if len(parts) > 0 else "Unknown",
        "City": parts[1].strip() if len(parts) > 1 else "Unknown",
        "State": parts[2].strip() if len(parts) > 2 else "Unknown",
        "PostalCode": parts[3].strip() if len(parts) > 3 else "Unknown",
        "Country": parts[4].strip() if len(parts) > 4 else "India"
    }
    
    return address

def main():
    # Load citizens and accounts from JSON database
    try:
        with open("../oodb/database.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading database: {e}")
        return

    citizens = data.get("citizens", [])
    accounts = data.get("accounts", [])

    # Create XML root
    root = ET.Element("PanBankingData")
    citizens_elem = ET.SubElement(root, "Citizens")

    # Add citizens with their accounts
    for c in citizens:
        citizen_elem = ET.SubElement(citizens_elem, "Citizen")
        citizen_elem.set("id", f"cit_{c['pan_number']}")
        citizen_elem.set("lastUpdated", datetime.now().isoformat())
        
        ET.SubElement(citizen_elem, "PAN").text = c["pan_number"]
        ET.SubElement(citizen_elem, "Name").text = c["name"]
        # Fix invalid date formats
        dob = c["dob"]
        if dob == "2002-22-10":  # Invalid month 22
            dob = "2002-10-22"
        elif dob == "2002-15-05":  # Invalid month 15
            dob = "2002-05-15"
        ET.SubElement(citizen_elem, "DOB").text = dob
        
        # Create structured address
        address_data = format_address(c["address"])
        address_elem = ET.SubElement(citizen_elem, "Address")
        for key, value in address_data.items():
            ET.SubElement(address_elem, key).text = value
        
        # Add accounts for this citizen
        citizen_accounts = [a for a in accounts if a["pan_number"] == c["pan_number"]]
        if citizen_accounts:
            accounts_elem = ET.SubElement(citizen_elem, "Accounts")
            
            for acc in citizen_accounts:
                account_elem = ET.SubElement(accounts_elem, "Account")
                ET.SubElement(account_elem, "AccountNumber").text = acc["account_no"]
                ET.SubElement(account_elem, "AccountType").text = acc.get("account_type", "savings")
                ET.SubElement(account_elem, "Balance").text = str(acc["balance"])
                ET.SubElement(account_elem, "BranchName").text = acc["branch_name"]
                ET.SubElement(account_elem, "Status").text = acc.get("status", "active")
                ET.SubElement(account_elem, "OpenDate").text = acc.get("open_date", datetime.now().strftime("%Y-%m-%d"))

    # Add metadata
    metadata_elem = ET.SubElement(root, "Metadata")
    ET.SubElement(metadata_elem, "ExportDate").text = datetime.now().isoformat()
    ET.SubElement(metadata_elem, "ExportSource").text = "PAN Banking System - Site A"
    ET.SubElement(metadata_elem, "RecordCount").text = str(len(citizens))
    ET.SubElement(metadata_elem, "Version").text = "1.0"

    # Write to XML file with pretty formatting
    xml_str = prettify_xml(root)
    with open("pan_data.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)

    # Create a digital signature file for verification
    with open("pan_data.xml", "rb") as f:
        content = f.read()
        signature = hashlib.sha256(content).hexdigest()
        
    with open("pan_data.signature", "w") as f:
        f.write(signature)

    print("Citizen data exported to pan_data.xml")
    print("Digital signature created for verification")

if __name__ == "__main__":
    main()
