import json
import xml.etree.ElementTree as ET

# Load citizens from JSON database
with open("../oodb/database.json", "r") as f:
    data = json.load(f)

citizens = data.get("citizens", [])

# Create XML root
root = ET.Element("Citizens")

for c in citizens:
    citizen_elem = ET.SubElement(root, "Citizen")
    ET.SubElement(citizen_elem, "PAN").text = c["pan_number"]
    ET.SubElement(citizen_elem, "Name").text = c["name"]
    ET.SubElement(citizen_elem, "DOB").text = c["dob"]
    ET.SubElement(citizen_elem, "Address").text = c["address"]

# Write to XML file
tree = ET.ElementTree(root)
tree.write("pan_data.xml", encoding="utf-8", xml_declaration=True)

print("✅ Citizen data exported to pan_data.xml")
