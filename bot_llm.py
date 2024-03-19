import os
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import pandas as pd
from datetime import datetime

def generate_threats(component_name):
    component_name = component.component_name

    llm_csv_folder = "llm_threat_files"
    llm_csv_file_path = os.path.join(llm_csv_folder, "llm_threat_library.csv")
    
    # Check if the separate CSV file exists for llm_threat_library
    if os.path.exists(llm_csv_file_path):
        existing_df = pd.read_csv(llm_csv_file_path)
        if component_name in existing_df['Component Name'].unique():
            # Read data from the existing CSV file for the specified component
            component_csv_file_path = os.path.join(llm_csv_folder, f"{component_name}.csv") 
            if os.path.exists(component_csv_file_path):
                df = pd.read_csv(component_csv_file_path)
        else:
            # If the component name is not present, call the API to generate data
            df = call_api_and_generate_data(component_name)
    else:
        # If the separate CSV file does not exist, call the API to generate data
        df = call_api_and_generate_data(component_name)
    
    # Add ICS ID and SCB ICS Domain to the DataFrame
    df = add_ics_id_and_scb_ics_domain(df)
    
    # Add additional columns
    df['is_generated_by_llm'] = 'yes'
    df['Threat ID'] = df.apply(lambda row: f"{component_name}_LLM_{row.name + 1:03}", axis=1)

    # Save DataFrame as CSV with Current Path and Timestamp
    csv_file_path = os.path.join(llm_csv_folder, f"{component_name}.csv")
    df.to_csv(csv_file_path, index=False)
    
    # Convert DataFrame to JSON response
    json_response = df.to_json(orient="records")
    return json_response

def call_api_and_generate_data(component_name):
    model_url = "http://10.16.1.10:11434/api/generate"
    prompt_text = f"Act as a cyber security expert with the experience of threat library development. your task is to generate 8 threat details for for given {component_name} components as per requirement."
    # Remaining part of the prompt_text ...

    payload = json.dumps({
      "model": "llama2",
      "prompt": prompt_text,
      "stream": False,
      "format": "json"
    })
    headers = {'Content-Type': 'application/json'}
    model_response = requests.post(model_url, headers=headers, data=payload).json()
    response_data = json.loads(model_response['response'])
    df = pd.DataFrame(response_data.values())
    return df

def add_ics_id_and_scb_ics_domain(df):
    countermeasures = df.iloc[:, 4].tolist()
    for countermeasure in countermeasures:
        url = f"http://10.16.1.10:8000/api/get_ics_details?input_text={countermeasure}"
        response = requests.get(url).json()
        ics_id = response['result'][0]['payload']['ics_id']
        scb_ics_domain = response['result'][0]['payload']['scb_ics_domain']
        df['ICS ID'] = ics_id
        df['SCB ICS Domain'] = scb_ics_domain
    return df


def generate_threats_api(component_name):
    json_response = generate_threats(component_name)
    return json_response
