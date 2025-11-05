from fastapi import FastAPI, Header, Depends, Response, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class CammonHeaders(BaseModel):
    user_aggent: str
    accept_language: str

async def get_cammon_headers(user_agent: str = Header(..., alias="User-Agent"),accept_language: str = Header(..., alias="Accept-Language"),) -> CammonHeaders:
    if not user_agent:
        raise HTTPException(status_code=400, detail="Missing required header: User-Agent")
    if not accept_language:
        raise HTTPException(status_code=400, detail="Missing required header: Accept-Language")
    return CammonHeaders(user_aggent=user_agent, accept_language=accept_language)

@app.get("/headers")
async def headers(cammon: CammonHeaders = Depends(get_cammon_headers)):
    return {
        "User_Agent": cammon.user_aggent,
        "Accept_Language": cammon.accept_language
    }

@app.get("/info")
async def info(response: Response, cammon: CammonHeaders = Depends(get_cammon_headers)):
    response.headers["X-Server-Time"] = datetime.now().isoformat()
    return {
        "msg": "your headers are updated",
        "headers": {
            "User-Agent": cammon.user_aggent,
            "Accept-Language": cammon.accept_language
        }
    }
