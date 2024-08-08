import os
import subprocess
import tempfile
import shutil
import zipfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

def get_zip_path(zip_file_name: str) -> str:
    """Get the path to the zip file in the application directory."""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(app_dir, zip_file_name)

def download_zip(zip_url: str, download_path: str):
    """Download the zip file using curl if it doesn't already exist."""
    if not os.path.isfile(download_path):
        try:
            subprocess.run(["curl", "-L", "-o", download_path, zip_url], check=True)
            if not os.path.isfile(download_path):
                raise HTTPException(status_code=404, detail="Zip file download failed")
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Error downloading zip file: {e.stderr.decode()}")

def extract_zip(zip_path: str, extract_to: str):
    """Extract the zip file to the specified directory."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    except zipfile.BadZipFile:
        raise HTTPException(status_code=500, detail="Error extracting zip file")

@app.post("/scan")
async def scan_files(mq_policy_file: UploadFile = File(...)):
    zip_url = "https://example.com/path/to/intercept.zip"  # Replace with actual URL
    zip_file_name = "intercept.zip"
    extracted_dir = "intercept_dir"
    intercept_binary_name = "intercept"  # Update with the actual binary name if different

    zip_path = get_zip_path(zip_file_name)

    with tempfile.TemporaryDirectory() as temp_dir:
        mq_policy_path = os.path.join(temp_dir, "mq_policy.yml")
        extract_path = os.path.join(temp_dir, extracted_dir)
        intercept_path = os.path.join(extract_path, intercept_binary_name)
        intercept_assure_path = os.path.join(temp_dir, "intercept.assure.sarif.json")
        failed_checks_path = os.path.join(temp_dir, "failed_checks.txt")

        # Save uploaded mq_policy.yml file to the temp directory
        with open(mq_policy_path, "wb") as f:
            f.write(await mq_policy_file.read())

        # Download the zip file if it does not already exist in the application directory
        download_zip(zip_url, zip_path)
        
        # Create directory to extract the zip file
        os.makedirs(extract_path, exist_ok=True)
        # Extract the zip file
        extract_zip(zip_path, extract_path)

        if not os.path.isfile(intercept_path):
            raise HTTPException(status_code=404, detail="Intercept binary not found in zip")

        # Make the intercept tool executable
        os.chmod(intercept_path, 0o755)

        try:
            # Run intercept commands
            subprocess.run([intercept_path, "config", "-r", f"config -a {mq_policy_path}"], check=True, cwd=temp_dir, capture_output=True)
            subprocess.run([intercept_path, "assure", "-t", mq_policy_path], check=True, cwd=temp_dir, capture_output=True)
            
            result = subprocess.run(['jq', '-r', '.runs[].results[].ruleId | capture("intercept.cc.assure.policy.({ruleId})")', intercept_assure_path], text=True, capture_output=True)

            with open(failed_checks_path, "w") as f:
                f.write(result.stdout)
            
            if os.path.exists(failed_checks_path):
                return FileResponse(failed_checks_path, media_type='text/plain', filename='failed_checks.txt')
            else:
                return {"message": "failed_checks.txt not found"}
        except subprocess.CalledProcessError as e:
            return {"message": f"Command '{e.cmd}' returned non-zero exit status {e.returncode}", "stderr": e.stderr.decode()}
        except Exception as e:
            return {"message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)