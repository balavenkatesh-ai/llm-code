from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import subprocess
import os
import tempfile
import shutil
print(f"Looking for intercept binary at: {os.path.abspath(intercept_binary_path)}")
app = FastAPI()

@app.post("/scan")
async def scan_files(mq_policy_file: UploadFile = File(...)):
    intercept_binary_path = "scan_tools/intercept/intercept"
    
    if not os.path.isfile(intercept_binary_path):
        raise HTTPException(status_code=404, detail="Intercept binary not found")

    with tempfile.TemporaryDirectory() as temp_dir:
        mq_policy_path = os.path.join(temp_dir, "mq_policy.yml")
        intercept_path = os.path.join(temp_dir, "intercept")
        intercept_assure_path = os.path.join(temp_dir, "intercept.assure.sarif.json")
        failed_checks_path = os.path.join(temp_dir, "failed_checks.txt")

        with open(mq_policy_path, "wb") as f:
            f.write(await mq_policy_file.read())

        shutil.copy(intercept_binary_path, intercept_path)
        os.chmod(intercept_path, 0o755)

        try:
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