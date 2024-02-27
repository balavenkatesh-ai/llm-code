from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import pandas as pd
from datetime import datetime

app = FastAPI()

class ComponentRequest(BaseModel):
    component_name: str

@app.post("api/generate_ai_threats")
async def generate_threats(component: ComponentRequest):
    component_name = component.component_name
    
    model_url = "http://10.16.1.10:11434/api/generate"

    prompt_text = f"Act as a cyber security expert with the experience of threat library development. your task is to generate 8 threat details for for given {component_name} components as per requirement.It is very important that your responses should be json format(eg.key should be threat_1,threat_2). Threat Name: A concise and descriptive name for the specific threat or attack scenario being analyzed. Attack Domain: The specific area or aspect of the system, application, or network targeted by the threat. Threat Description: A detailed explanation of the nature and characteristics of the threat, including how it operates and its potential impact. CAPEC Reference: Reference to relevant entries in the Common Attack Pattern Enumeration and Classification (CAPEC) database, providing additional context and information about known attack patterns. Countermeasure: Strategies, or techniques, or security controls implemented to mitigate or prevent the identified threat, should be string. MITRE Tactic ID: Unique identifier assigned by MITRE for the tactic associated with the threat, as defined in the MITRE ATT&CK framework. MITRE Tactic Description: Description of the tactic associated with the threat, as defined in the MITRE ATT&CK framework. MITRE Technique ID: Unique identifier assigned by MITRE for the technique associated with the threat, as defined in the MITRE ATT&CK framework. MITRE Technique Description: Description of the technique associated with the threat, as defined in the MITRE ATT&CK framework. Severity: Assessment of the potential impact or harm caused by the threat, typically categorized as low, medium, or high severity. Likelihood: Assessment of the probability or likelihood of the threat being realized, often categorized as low, medium, or high likelihood. Programming Threat Vectors: Specific programming-related vulnerabilities or weaknesses exploited by the threat. Social Engineering Threat Vectors: Techniques or methods involving manipulation of individuals to gain unauthorized access or information. L4 Control: Layer 4 control measures, such as firewall rules or network segmentation, implemented to detect or mitigate the threat. CAPEC ID: Unique identifier assigned by the CAPEC database for the attack pattern associated with the threat. CWE ID: Unique identifier assigned by the Common Weakness Enumeration (CWE) database for any weaknesses or vulnerabilities exploited by the threat. Threat Vector: The method or means by which the threat is delivered or propagated within the system or network. Component Name: The specific component or element of the system or application targeted by the threat. Component Type: The type or category of the component targeted by the threat, such as network, application, or user interface. Domain: The broader domain or area of expertise to which the threat pertains, such as cybersecurity, software development, or network security."
    
    payload = json.dumps({
      "model": "llama2",
      "prompt": prompt_text,
      "stream": False,
      "format": "json"
    })
    headers = {
      'Content-Type': 'application/json'
    }

    model_response = requests.post(model_url, headers=headers, data=payload).json()

    response = model_response['response']
    response_data  = json.loads(model_response['response'])
    df = pd.DataFrame(response_data.values())

    countermeasures = df.iloc[:, 4].tolist()

    for countermeasure in countermeasures:
        url = f"http://10.16.1.10:8000/api/get_ics_details?input_text={countermeasure}"
        response = requests.get(url).json()
        ics_id = response['result'][0]['payload']['ics_id']
        scb_ics_domain = response['result'][0]['payload']['scb_ics_domain']
        df['ICS ID'] = ics_id
        df['SCB ICS Domain'] = scb_ics_domain

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file_path = f"{current_datetime}_{component_name}.csv"
    df.to_csv(csv_file_path, index=False)

    df['is_generated_by_llm'] = 'yes'
    df['Threat ID'] = component_name + '_LLM_001'

    json_response = df.to_json(orient="records")
    return json_response
