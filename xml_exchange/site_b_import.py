import xml.etree.ElementTree as ET

tree = ET.parse("pan_data.xml")
root = tree.getroot()

print("=== Imported Citizens (from PAN XML) ===\n")

for citizen in root.findall("Citizen"):
    pan = citizen.find("PAN").text
    name = citizen.find("Name").text
    dob = citizen.find("DOB").text
    address = citizen.find("Address").text

    print(f"PAN: {pan}\nName: {name}\nDOB: {dob}\nAddress: {address}\n")
