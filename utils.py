from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import subprocess
import os
import tempfile

app = FastAPI()

@app.post("/scan")
async def scan_files(mq_policy_file: UploadFile = File(...)):
    with tempfile.TemporaryDirectory() as temp_dir:
        mq_policy_path = os.path.join(temp_dir, "mq_policy.yml")
        ini_path = os.path.join(temp_dir, "qm.ini")
        intercept_path = os.path.join(temp_dir, "intercept")
        intercept_assure_path = os.path.join(temp_dir, "intercept.assure.sarif.json")
        failed_checks_path = os.path.join(temp_dir, "failed_checks.txt")

        # Save uploaded mq_policy.yml file to temp directory
        with open(mq_policy_path, "wb") as f:
            f.write(await mq_policy_file.read())

        # Assuming intercept binary and other necessary files are placed in temp directory
        shutil.copy("/path/to/intercept", intercept_path)  # Adjust this path

        # Make the intercept tool executable
        os.chmod(intercept_path, 0o755)

        try:
            # Run intercept commands
            subprocess.run([intercept_path, "config", "-r", f"config -a {mq_policy_path}"], check=True, cwd=temp_dir)
            subprocess.run([intercept_path, "assure", "-t", ini_path], check=True, cwd=temp_dir)
            subprocess.run(['jq', '-r', '.runs[].results[].ruleId | capture("intercept.cc.assure.policy.({ruleId})")', intercept_assure_path, '>', failed_checks_path], shell=True, check=True, cwd=temp_dir)

            if os.path.exists(failed_checks_path):
                return FileResponse(failed_checks_path, media_type='text/plain', filename='failed_checks.txt')
            else:
                return {"message": "failed_checks.txt not found"}
        except subprocess.CalledProcessError as e:
            return {"message": f"Command '{e.cmd}' returned non-zero exit status {e.returncode}"}
        except Exception as e:
            return {"message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)