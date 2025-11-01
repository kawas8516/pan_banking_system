# 🧾 PAN Card & Banking System — Object-Oriented Database and XML Data Sharing

## 📘 Introduction

In today’s interconnected digital ecosystem, data consistency and secure exchange between organizations are critical. Two commonly used technologies to handle structured and interoperable data are **Object-Oriented Databases (OODB)** and **XML-based Data Interchange Systems**.

This project demonstrates how an **Object-Oriented Database** can be designed and simulated for a simple **PAN Card and Banking System**, and how **XML** can be used as a medium for structured data sharing between two independent systems — here, between a **PAN Department (Site A)** and a **Bank (Site B)**.

The PAN Department stores individual citizen records (including PAN number, name, date of birth, and contact information). The Bank system imports this verified PAN information to open or update customer accounts. The XML Schema Definition (**XSD**) ensures the data shared adheres to a strict format, enabling **validation, integrity, and interoperability**.

This project is divided into two major components:

1. **Object-Oriented Database (OODB) Implementation** — Simulates storage, retrieval, and querying of PAN and banking data using Python objects and JSON-based persistence.
2. **XML Database System** — Exports citizen data as XML from Site A and imports it at Site B, validating it with XSD before use.

This practical integration mirrors real-world workflows between government and banking organizations, emphasizing modularity, data integrity, and structured interoperability.
## � Directory Structure

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

6. Import at Site B (Bank)

```powershell
python site_b_import.py
```

This will import/display the validated data on the bank side.

Notes
- The venv step is optional but recommended to avoid dependency conflicts.
- If you prefer a requirements file, add a `requirements.txt` with `xmlschema` and run `pip install -r requirements.txt`.

---
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

