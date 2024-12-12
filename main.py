from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

# Model to accept request payload
class CodeRequest(BaseModel):
    language: str
    code: str

@app.post("/execute")
def execute_code(request: CodeRequest):
    try:
        if request.language == "python":
            # Execute Python code
            process = subprocess.run(
                ["python3", "-c", request.code],
                text=True,
                capture_output=True,
                timeout=5
            )
            return {"output": process.stdout, "error": process.stderr}
        else:
            raise HTTPException(status_code=400, detail="Unsupported language")
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Execution timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
