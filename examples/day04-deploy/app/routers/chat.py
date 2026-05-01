from fastapi import APIRouter,HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.agent import chat_stream

router = APIRouter()

class ChatRequest(BaseModel):
    message:str

@router.post("/chat")
async def chat(req:ChatRequest):
    try:
        return StreamingResponse(chat_stream(req.message),media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"出错了：{str(e)}")