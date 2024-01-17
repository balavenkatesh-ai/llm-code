import re
import csv


response = """

Here are five potential threats identified in the PostgreSQL 1.0 security analysis, along with their corresponding MITRE Tactics and Techniques IDs:

| Threat Name | Threat Description | Attack Domain | Countermeasure | MITRE Tactics ID | MITRE Tactics Description | MITRE Techniques ID | MITRE Techniques Description | CAPEC Reference URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Data Manipulation | Attackers can manipulate data in PostgreSQL due to improper access controls or vulnerabilities in the application using the database. | Application | Implement proper access controls and encryption, validate user input, restrict direct access to the database. | TA0043 - Data Tampering | https://attack.mitre.org/tactics/TA0043/ | T1548 - Data Encoding | https://attack.mitre.org/techniques/T1548/ | 1000 - Data tampering | https://capec.mitre.org/data/definitions/1000.html |
| Authentication Bypass | Attackers can bypass authentication mechanisms in PostgreSQL, gaining unauthorized access to the database. | Network | Implement secure authentication protocols, restrict direct access to the database, use secure passwords and store them securely. | TA0041 - Credential Dumping | https://attack.mitre.org/tactics/TA0041/ | T1546 - Password Guessing | https://attack.mitre.org/techniques/T1546/ | 1002 - Credential dumping | https://capec.mitre.org/data/definitions/1002.html |
| SQL Injection | Attackers can inject malicious SQL code into PostgreSQL, potentially leading to unauthorized access or data manipulation. | Application | Implement proper input validation and sanitization, use prepared statements and parameterized queries, restrict direct access to the database. | TA0042 - SQL Injection | https://attack.mitre.org/tactics/TA0042/ | T1547 - SQL Injection | https://attack.mitre.org/techniques/T1547/ | 1003 - SQL injection | https://capec.mitre.org/data/definitions/1003.html |

Note: The MITRE Tactics and Techniques IDs are based on the MITRE ATT&CK® framework version 9.3.0, and may change with future updates to the framework. The CAPEC Reference URLs link to the corresponding entries in the Common Attack Pattern Enumeration and Classification (CAPEC) database.

"""

# Extract table data using regular expressions
table_data = re.findall(r"\|(.*?)\|", response, flags=re.DOTALL)

# Split rows into lists, removing extra newlines and spaces
rows = [row.strip().splitlines() for row in table_data]

# Create CSV header from the first row
header = rows[0]

# Remove header from data rows
data_rows = rows[1:]

# Write CSV file
with open("threat_report.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)  # Write header row
    writer.writerows(data_rows)  # Write data rows

print("CSV file saved successfully!")