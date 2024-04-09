import re
import json
import csv
import io
import html2xlsx
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

def embed_html_into_excel(html_file_path, excel_file_path):
    # Load HTML content from file
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # Create a new workbook
    wb = Workbook()
    ws = wb.active

    # Embed HTML content into the worksheet
    ws.webSettings.url = 'data:text/html;base64,' + html2xlsx.html_to_base64(html_content)

    # Set the column width to fit the content
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column].width = adjusted_width

    # Save the workbook
    wb.save(excel_file_path)
    print("HTML content embedded into Excel file successfully.")

if __name__ == "__main__":
    html_file_path = input("Enter the path to the HTML file: ")
    excel_file_path = input("Enter the output path for the Excel file: ")
    embed_html_into_excel(html_file_path, excel_file_path)







if __name__ == "__main__":
    html_path = "path/to/your/html/file.html"  # Replace with your HTML file path
    convert_html_to_png_with_phantomjs(html_path)


# def json_to_csv(response):
#     """Extracts JSON data from the response and returns a CSV string in memory."""

#     csv_data = io.StringIO()
#     writer = csv.DictWriter(csv_data, fieldnames=None)

#     # Extract JSON blocks, ensuring double quotes around property names (just in case)
#     json_data_str = re.sub(r"(?<!\[)(?<!,)(\w+):\s+([^,{]*)", r'"\1": \2', response.split("```json")[1].split("```")[0])

#     # Add commas between JSON objects
#     json_data_str = "[" + re.sub(r'}\s*{', '},{', json_data_str) + "]"

#     try:
#         # Load JSON data
#         json_data_blocks = json.loads(json_data_str)
#     except json.decoder.JSONDecodeError as e:
#         raise ValueError(f"Error decoding JSON: {e}")

#     for json_data in json_data_blocks:
#         if not writer.fieldnames:
#             writer.fieldnames = list(json_data.keys())
#             writer.writeheader()
#         writer.writerow(json_data)

#     csv_data.seek(0)
#     return csv_data.read()

def json_to_csv(response):
    """Extracts JSON data from the response and returns a CSV string in memory."""

    csv_data = io.StringIO()
    writer = csv.DictWriter(csv_data, fieldnames=None)

    # Extract JSON blocks, ensuring double quotes around property names (just in case)
    json_blocks = re.findall(r"```json\n(.*?)\n```", response, re.DOTALL)

    for json_data_str in json_blocks:
        # Add commas between JSON objects
        json_data_str = "[" + re.sub(r'}\s*{', '},{', json_data_str) + "]"

        try:
            # Load JSON data
            json_data_blocks = json.loads(json_data_str)
        except json.decoder.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON: {e}")

        for json_data in json_data_blocks:
            if not writer.fieldnames:
                writer.fieldnames = list(json_data.keys())
                writer.writeheader()
            writer.writerow(json_data)

    csv_data.seek(0)
    return csv_data.read()
    
response =  """ 
 Here is a list of potential threats for Nginx 1.0 based on my analysis as a cyber security expert with over 30 years of experience in threat library development:

```json
{
    "Threat Name": "Data Manipulation",
    "Threat Description": "Attackers can manipulate data in Nginx's configuration files and logs due to improper access controls or vulnerabilities in the application using the database.",
    "Attack Domain": "Application",
    "Countermeasure": "Implement proper access controls and encryption for sensitive data, regularly review and update configurations, and use secure protocols for data transfer.",
    "MITRE Tactics ID": "TA0043 - Data Tampering",
    "MITRE Tactics Description": "An attacker can manipulate or alter data to achieve a desired outcome, such as modifying sensitive information or injecting malware into the system.",
    "MITRE Techniques ID": "T1548 - Data Tampering",
    "MITRE Techniques Description": "An attacker can tamper with data to manipulate the system's behavior or steal sensitive information.",
    "CAPEC Reference URL": "https://capec.mitre.org/data/definitions/1000.html"
}
```

```json
{
    "Threat Name": "Command Injection",
    "Threat Description": "Attackers can inject malicious commands into Nginx's configuration files and logs due to vulnerabilities in the application using the database.",
    "Attack Domain": "Application",
    "Countermeasure": "Implement proper input validation and sanitization, use prepared statements and parameterized queries, and limit privileges for system accounts.",
    "MITRE Tactics ID": "TA0042 - Command Injection",
    "MITRE Tactics Description": "An attacker can inject malicious commands into a system to execute arbitrary code or manipulate the system's behavior.",
    "MITRE Techniques ID": "T1547 - Command Injection",
    "MITRE Techniques Description": "An attacker can inject malicious commands into a system to execute arbitrary code or manipulate the system's behavior.",
    "CAPEC Reference URL": "https://capec.mitre.org/data/definitions/1000.html"
}
```

```json
{
    "Threat Name": "SQL Injection",
    "Threat Description": "Attackers can inject malicious SQL code into Nginx's database queries due to vulnerabilities in the application using the database.",
    "Attack Domain": "Database",
    "Countermeasure": "Implement proper input validation and sanitization, use prepared statements and parameterized queries, and limit privileges for system accounts.",
    "MITRE Tactics ID": "TA0041 - SQL Injection",
    "MITRE Tactics Description": "An attacker can inject malicious SQL code into a system to manipulate the database or steal sensitive information.",
    "MITRE Techniques ID": "T1546 - SQL Injection",
    "MITRE Techniques Description": "An attacker can inject malicious SQL code into a system to manipulate the database or steal sensitive information.",
    "CAPEC Reference URL": "https://capec.mitre.org/data/definitions/1000.html"
}
```

```json
{
    "Threat Name": "Cross-Site Scripting (XSS)",
    "Threat Description": "Attackers can inject malicious scripts into Nginx's web pages due to vulnerabilities in the application using the database.",
    "Attack Domain": "Web Application",
    "Countermeasure": "Implement proper input validation and sanitization, use Content Security Policy (CSP) and JavaScript injection protection, and limit privileges for system accounts.",
    "MITRE Tactics ID": "TA0044 - Cross-Site Scripting (XSS)",
    "MITRE Tactics Description": "An attacker can inject malicious scripts into a web page to steal sensitive information or manipulate the user's interaction with the application.",
    "MITRE Techniques ID": "T1549 - Cross-Site Scripting (XSS)",
    "MITRE Techniques Description": "An attacker can inject malicious scripts into a web page to steal sensitive information or manipulate the user's interaction with the application.",
    "CAPEC Reference URL": "https://capec.mitre.org/data/definitions/1000.html"
}
```

```json
{
    "Threat Name": "Denial of Service (DoS)",
    "Threat Description": "Attackers can flood Nginx's network connections or consume excessive system resources, leading to a denial of service and potential data loss.",
    "Attack Domain": "Network",
    "Countermeasure": "Implement rate limiting and IP blocking, use load balancers and redundant systems, and regularly monitor network traffic for suspicious activity.",
    "MITRE Tactics ID": "TA0045 - Denial of Service (DoS)",
    "MITRE Tactics Description": "An attacker can flood a system with network traffic or consume excessive system resources to cause a denial of service and potential data loss.",
    "MITRE Techniques ID": "T1550 - Denial of Service (DoS)",
    "MITRE Techniques Description": "An attacker can flood a system with network traffic or consume excessive system resources to cause a denial of service and potential data loss.",
    "CAPEC Reference URL": "https://capec.mitre.org/data/definitions/1000.html"
}
```

Please note that these threats are not exhaustive, and new threats may emerge as Nginx 1.0 is used in different environments and configurations. Regularly reviewing and updating the threat library is essential to ensure the security of the system.
"""

tests =""" Here are two potential threats for JBoss 1.0 based on my analysis as a cyber security expert with over 30 years of experience in threat library development:

```json
{
    "Threat Name": "Data Manipulation",
    "Threat Description": "Attackers can manipulate data in JBoss 1.0 due to improper access controls or vulnerabilities in the application using the database, leading to potential data tampering or loss of integrity.",
    "Attack Domain": "Application",
    "Countermeasure": "Implement proper access controls and encryption for sensitive data, regularly back up critical data, and monitor database activity for suspicious behavior.",
    "MITRE Tactics ID": "TA0043 - Data Tampering",
    "MITRE Tactics Description": "Tampering with data to manipulate its appearance or content.",
    "MITRE Techniques ID": "T1548 - Data Tampering",
    "MITRE Techniques Description": "Tampering with data to manipulate its appearance or content, often to gain an advantage or to hide malicious activity.",
    "CAPEC Reference URL": "https://capec.mitre.org/data/definitions/1000.html"
}

{
    "Threat Name": "Command Injection",
    "Threat Description": "Attackers can inject malicious commands into JBoss 1.0 through vulnerabilities in the application using the database, leading to potential execution of unauthorized code and compromise of system integrity.",
    "Attack Domain": "Application",
    "Countermeasure": "Implement proper input validation and sanitization, use prepared statements and parameterized queries, and regularly update software components to address known vulnerabilities.",
    "MITRE Tactics ID": "TA0042 - Command Injection",
    "MITRE Tactics Description": "Inserting malicious code or commands into a command or query to manipulate the behavior of the application or system.",
    "MITRE Techniques ID": "T1547 - Command Injection",
    "MITRE Techniques Description": "Inserting malicious code or commands into a command or query to manipulate the behavior of the application or system, often to gain unauthorized access or control.",
    "CAPEC Reference URL": "https://capec.mitre.org/data/definitions/1000.html"
}
```
Note that these threats are just examples and may not be exhaustive. The actual threats to JBoss 1.0 will depend on its specific configuration, usage, and environment."""

print(json_to_csv(tests))
