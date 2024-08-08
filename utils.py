import os
import subprocess
import tempfile
import shutil
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

def parse_sarif_file(sarif_path: str) -> str:
    """Parse the SARIF JSON file and extract the ruleId values."""
    try:
        with open(sarif_path, 'r') as f:
            sarif_data = json.load(f)
        rule_ids = [result["ruleId"] for run in sarif_data["runs"] for result in run["results"]]
        return "\n".join(rule_ids)
    except (json.JSONDecodeError, KeyError) as e:
        raise HTTPException(status_code=500, detail=f"Error parsing SARIF file: {str(e)}")

@app.post("/scan")
async def scan_files(mq_policy_file: UploadFile = File(...)):
    intercept_binary_path = "scan_tools/intercept/intercept"
    print(f"Looking for intercept binary at: {os.path.abspath(intercept_binary_path)}")
    
    if not os.path.isfile(intercept_binary_path):
        raise HTTPException(status_code=404, detail="Intercept binary not found")

    with tempfile.TemporaryDirectory() as temp_dir:
        mq_policy_path = os.path.join(temp_dir, "mq_policy.yml")
        intercept_path = os.path.join(temp_dir, "intercept")
        intercept_assure_path = os.path.join(temp_dir, "intercept.assure.sarif.json")
        failed_checks_path = os.path.join(temp_dir, "failed_checks.txt")

        # Save uploaded mq_policy.yml file to the temp directory
        with open(mq_policy_path, "wb") as f:
            f.write(await mq_policy_file.read())

        # Copy the intercept binary to the temp directory
        shutil.copy(intercept_binary_path, intercept_path)
        print(f"Intercept binary copied to: {intercept_path}")

        # Make the intercept tool executable
        os.chmod(intercept_path, 0o755)

        try:
            # Debug statement to print the command
            print(f"Running command: {[intercept_path, 'config', '-r', mq_policy_path]}")
            
            # Run intercept commands
            subprocess.run([intercept_path, "config", "-r", mq_policy_path], check=True, cwd=temp_dir, capture_output=True)
            subprocess.run([intercept_path, "assure", "-t", mq_policy_path], check=True, cwd=temp_dir, capture_output=True)
            
            # Parse the SARIF file and extract ruleId values
            rule_ids = parse_sarif_file(intercept_assure_path)
            with open(failed_checks_path, "w") as f:
                f.write(rule_ids)
            
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
