from fastapi import FastAPI, HTTPException
from copykit import create_branding, create_keywords
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)
MAX_INPUT_LENGTH = 32


@app.get("/create_snippet")
async def create_branding_api(prompt: str):
    validate_input_len(prompt)
    snippet = create_branding(prompt)
    return {"snippet": snippet, "keywords": []}

@app.get("/create_keywords")
async def create_keywords_api(prompt: str):
    validate_input_len(prompt)
    keywords = create_keywords(prompt)
    return {"snippet": None, "keywords": keywords}

@app.get("/generate_snippet_and_keywords")
async def create_keywords_api(prompt: str):
    validate_input_len(prompt)
    snippet = create_branding(prompt)
    keywords = create_keywords(prompt)
    return {"snippet": snippet, "keywords": keywords}
    

def validate_input_len(prompt:str):
    if len(prompt) >= MAX_INPUT_LENGTH:
        raise HTTPException(
            status_code=400, 
            detail=f"Character length too long, must be under {MAX_INPUT_LENGTH} characters.")
