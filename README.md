# 🧾 PAN Card & Banking System — Object-Oriented Database and XML Data Sharing

## 📘 Introduction

In today’s interconnected digital ecosystem, data consistency and secure exchange between organizations are critical. Two commonly used technologies to handle structured and interoperable data are **Object-Oriented Databases (OODB)** and **XML-based Data Interchange Systems**.

This project demonstrates how an **Object-Oriented Database** can be designed and simulated for a simple **PAN Card and Banking System**, and how **XML** can be used as a medium for structured data sharing between two independent systems — here, between a **PAN Department (Site A)** and a **Bank (Site B)**.

The PAN Department stores individual citizen records (including PAN number, name, date of birth, and contact information). The Bank system imports this verified PAN information to open or update customer accounts. The XML Schema Definition (**XSD**) ensures the data shared adheres to a strict format, enabling **validation, integrity, and interoperability**.

This project is divided into two major components:

1. **Object-Oriented Database (OODB) Implementation** — Simulates storage, retrieval, and querying of PAN and banking data using Python objects and JSON-based persistence.
2. **XML Database System** — Exports citizen data as XML from Site A and imports it at Site B, validating it with XSD before use.

This practical integration mirrors real-world workflows between government and banking organizations, emphasizing modularity, data integrity, and structured interoperability.

---

## ⚙️ Part 1 — Object-Oriented Database (OODB)

### 🧩 Description

An Object-Oriented Database is a system that stores data in the form of objects rather than relational tables. Each object represents a real-world entity with attributes and behaviors.

In this project:

* **Citizen** objects represent individuals with PAN details.
* **BankAccount** objects represent bank accounts linked to citizens.
* The database is simulated using JSON for persistence and indexing.

### 🧱 Key Features

* Object-based data modeling (classes for entities)
* Basic persistence (saving and loading JSON)
* Indexing support (searching by PAN number)
* Version tracking for updates

### 🗂️ Example Classes

```python
class Citizen:
    def __init__(self, pan_no, name, dob, phone):
        self.pan_no = pan_no
        self.name = name
        self.dob = dob
        self.phone = phone
```

```python
class BankAccount:
    def __init__(self, acc_no, pan_no, balance):
        self.acc_no = acc_no
        self.pan_no = pan_no
        self.balance = balance
```

---

## 🧾 Part 2 — XML-Based Data Sharing System

### 🌐 Overview

XML (eXtensible Markup Language) is used for sharing structured data between systems.
In this project:

* **Site A (PAN Department)** exports citizen data as an XML file.
* **Site B (Bank)** imports and validates that XML before creating accounts.

### 📄 XML Example (`pan_data.xml`)

```xml
<citizens>
  <citizen>
    <pan_no>ABCDE1234F</pan_no>
    <name>Rohan Sharma</name>
    <dob>1995-03-12</dob>
    <phone>9876543210</phone>
  </citizen>
</citizens>
```

### 🧩 XML Schema Definition (`pan_data.xsd`)

```xml
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="citizens">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="citizen" maxOccurs="unbounded">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="pan_no" type="xs:string"/>
              <xs:element name="name" type="xs:string"/>
              <xs:element name="dob" type="xs:date"/>
              <xs:element name="phone" type="xs:string"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

### ✅ Validation

Validation ensures that:

* The XML structure is correct.
* Data follows the right types (e.g., date format for DOB).
* The XML adheres to the schema.

Example validation result:

```
✅ XML is valid against the schema.
```

---

## 🧰 Requirements

| Category            | Tools / Libraries       |
| ------------------- | ----------------------- |
| Language            | Python 3.8+             |
| Database Simulation | JSON Files              |
| XML Parsing         | `xml.etree.ElementTree` |
| XML Validation      | `xmlschema`             |
| Data Storage        | Local Filesystem        |

---

## 🧮 Directory Structure

```
pan_banking_system/
│
├── oodb/
│   ├── citizen.py
│   ├── bank_account.py
│   ├── database.py
│   └── main.py
│
└── xml_exchange/
    ├── pan_data.xsd
    ├── site_a_export.py
    ├── site_b_import.py
    └── validate_xml.py
```

---

## 💻 How to Run Locally

### Step 1: Clone or Create the Project

```bash
mkdir pan_banking_system
cd pan_banking_system
```

### Step 2: Create Virtual Environment (Optional)

```bash
python -m venv env
source env/bin/activate   # (on macOS/Linux)
env\Scripts\activate      # (on Windows)
```

### Step 3: Install Dependencies

```bash
pip install xmlschema
```

### Step 4: Run the OODB Simulation

```bash
cd oodb
python main.py
```

This will:

* Create and store `Citizen` and `BankAccount` objects.
* Save them into a JSON-based object database.

### Step 5: Export XML Data (Site A)

```bash
cd ../xml_exchange
python site_a_export.py
```

Generates `pan_data.xml`.

### Step 6: Validate XML against XSD

```bash
python validate_xml.py
```

If valid, you’ll see:

```
✅ XML is valid against the schema.
```

### Step 7: Import at Site B (Bank)

```bash
python site_b_import.py
```

Displays or stores the imported data.

---

## 🧩 Advantages of This System

| Feature                  | Benefit                                                 |
| ------------------------ | ------------------------------------------------------- |
| Object-Oriented Database | Intuitive data representation using real-world models   |
| XML Interchange          | Platform-independent structured data exchange           |
| XSD Validation           | Ensures data integrity between systems                  |
| Simple Implementation    | Lightweight and easy to simulate locally                |
| Extensible Design        | Can be scaled to multiple organizations or new entities |

---

## 📚 Conclusion

This project demonstrates a **miniature ecosystem** of data management and exchange between two systems — simulating how real-world institutions like the **Income Tax Department (for PAN)** and **Banks** interact.

The **Object-Oriented Database** simplifies local data storage through class-based modeling, while the **XML + XSD validation** ensures structured, verifiable communication across independent systems.

Such systems represent the foundation of **modern interoperable architectures**, emphasizing data consistency, reusability, and modularity — core principles of advanced database and web engineering.

