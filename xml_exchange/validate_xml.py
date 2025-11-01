#pip install xmlschema
import xmlschema

xsd_path = "pan_data.xsd"
xml_path = "pan_data.xml"

schema = xmlschema.XMLSchema(xsd_path)

# Validate the XML file
if schema.is_valid(xml_path):
    print("✅ XML is valid against the schema.")
else:
    print("❌ XML is INVALID!")
    for error in schema.iter_errors(xml_path):
        print(f"Error: {error.message}")
