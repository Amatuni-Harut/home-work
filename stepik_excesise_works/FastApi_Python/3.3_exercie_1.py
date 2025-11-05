from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.get("/headers")
async def  get_headers(request: Request):
    user_agent= request.headers.get("User-Agent")
    accept_language=request.headers.get("Assept-Language")
    if not user_agent:
        raise HTTPException(status_code=400, detail="Missing required header: User-Agent")
    if not accept_language:
        raise HTTPException( status_code=400, detail="Missing required header: Accept-Language")
    
    return {"User-Agent": user_agent, "Accept-Language": accept_language}
