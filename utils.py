from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import subprocess
import os

app = FastAPI()

@app.post("/scan")
async def scan_files(ini_file: UploadFile = File(...), mq_policy_file: UploadFile = File(...)):
    # Save uploaded files to disk
    ini_path = "/tmp/qm.ini"
    mq_policy_path = "/tmp/mq_policy.yml"
    
    with open(ini_path, "wb") as f:
        f.write(await ini_file.read())
    
    with open(mq_policy_path, "wb") as f:
        f.write(await mq_policy_file.read())
    
    # Assuming intercept tool and other necessary files are already available in /tmp/
    intercept_path = "/tmp/intercept"
    intercept_config_path = "/tmp/intercept_config"
    
    # Make the intercept tool executable
    os.chmod(intercept_path, 0o755)

    # Run the intercept commands
    subprocess.run([intercept_path, "config", "-r", f"config -a {mq_policy_path}"], shell=True)
    subprocess.run([intercept_path, "assure", "-t", ini_path], shell=True)
    subprocess.run(['jq', '-r', f'.runs[].results[].ruleId | capture("intercept.cc.assure.policy.({{ruleId}})")', 'intercept.assure.sarif.json', '>', 'failed_checks.txt'], shell=True)
    
    failed_checks_path = "/tmp/failed_checks.txt"
    
    if os.path.exists(failed_checks_path):
        return FileResponse(failed_checks_path, media_type='text/plain', filename='failed_checks.txt')
    else:
        return {"message": "failed_checks.txt not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
    # Create a temporary directory to work in
    temp_dir = "/tmp/intercept_scan"
    os.makedirs(temp_dir, exist_ok=True)

    # Save uploaded files to the temporary directory
    ini_path = os.path.join(temp_dir, "qm.ini")
    mq_policy_path = os.path.join(temp_dir, "mq_policy.yml")
    
    with open(ini_path, "wb") as f:
        f.write(await ini_file.read())
    
    with open(mq_policy_path, "wb") as f:
        f.write(await mq_policy_file.read())
    
    # Define paths to intercept binaries and working files
    intercept_path = "/tmp/intercept"
    intercept_assure_path = os.path.join(temp_dir, "intercept.assure.sarif.json")
    failed_checks_path = os.path.join(temp_dir, 