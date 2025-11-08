import xmlschema
import sys
import os
from datetime import datetime

def validate_xml(xml_file, xsd_file):
    """
    Validate an XML file against an XSD schema
    Returns True if valid, False otherwise
    """
    try:
        # Create schema object
        schema = xmlschema.XMLSchema(xsd_file)
        
        # Validate XML against schema
        is_valid = schema.is_valid(xml_file)
        
        if is_valid:
            print(f"XML file '{xml_file}' is valid according to schema '{xsd_file}'")
            
            # Get validation report
            validation_report = schema.validate(xml_file)
            
            # Count elements
            try:
                xml_tree = schema.to_dict(xml_file)
                if isinstance(xml_tree, dict) and 'Citizens' in xml_tree:
                    citizens = xml_tree['Citizens']['Citizen']
                    if isinstance(citizens, list):
                        citizen_count = len(citizens)
                    else:
                        citizen_count = 1  # Single citizen
                    print(f"Found {citizen_count} valid citizen records")
                else:
                    print("Could not count citizen records (schema structure may have changed)")
            except Exception as e:
                print(f"Could not analyze XML content: {e}")
            
            return True
        else:
            print(f"XML file '{xml_file}' is NOT valid according to schema '{xsd_file}'")
            return False
            
    except Exception as e:
        print(f"Validation error: {e}")
        return False

def generate_validation_report(xml_file, xsd_file):
    """Generate a detailed validation report"""
    try:
        # Create schema object
        schema = xmlschema.XMLSchema(xsd_file)
        
        # Create report file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"validation_report_{timestamp}.txt"
        
        with open(report_file, "w") as f:
            f.write(f"XML Validation Report\n")
            f.write(f"===================\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"XML File: {xml_file}\n")
            f.write(f"XSD Schema: {xsd_file}\n\n")
            
            # Check if valid
            is_valid = schema.is_valid(xml_file)
            f.write(f"Validation Result: {'VALID' if is_valid else 'INVALID'}\n\n")
            
            # If invalid, get errors
            if not is_valid:
                try:
                    schema.validate(xml_file)
                except Exception as e:
                    f.write(f"Validation Errors:\n{str(e)}\n\n")
            
            # Get schema info
            f.write("Schema Information:\n")
            f.write(f"  Target Namespace: {schema.target_namespace}\n")
            f.write(f"  Element Count: {len(schema.elements)}\n")
            f.write(f"  Complex Type Count: {len(schema.types)}\n\n")
            
            f.write("Required Elements:\n")
            for name, element in schema.elements.items():
                if not hasattr(element, 'min_occurs') or element.min_occurs > 0:
                    f.write(f"  - {name}\n")
        
        print(f"Validation report generated: {report_file}")
        return report_file
        
    except Exception as e:
        print(f"Error generating validation report: {e}")
        return None

def main():
    # Default file paths
    xml_file = "pan_data.xml"
    xsd_file = "pan_data.xsd"
    
    # Check command line arguments
    if len(sys.argv) > 1:
        xml_file = sys.argv[1]
    if len(sys.argv) > 2:
        xsd_file = sys.argv[2]
    
    # Check if files exist
    if not os.path.exists(xml_file):
        print(f"XML file '{xml_file}' not found")
        return
    
    if not os.path.exists(xsd_file):
        print(f"XSD schema file '{xsd_file}' not found")
        return
    
    # Validate XML
    is_valid = validate_xml(xml_file, xsd_file)
    
    # Generate detailed report
    if is_valid:
        generate_validation_report(xml_file, xsd_file)
    else:
        print("XML is invalid. Fix errors before generating a detailed report.")
        # Skip interactive input for automated runs
        print("Skipping detailed report generation due to automated execution")

if __name__ == "__main__":
    main()
