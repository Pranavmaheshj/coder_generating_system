from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from llm_integration import CodeGenerator  # Must match exactly
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize with EXACT class name
generator = CodeGenerator()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/generate")
async def generate_code(prompt: str, language: str = "python"):
    code = generator.generate(prompt, language)
    return {"code": code}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)