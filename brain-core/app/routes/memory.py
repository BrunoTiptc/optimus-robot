from fastapi import APIRouter
from app.models.conversation import ConversationMemory
from app.models.user_memory import UserMemory
from app.services import memory_service

router = APIRouter(prefix="/memory", tags=["memory"])

@router.post("/user")
def save_user_memory(memory: UserMemory):
    memory_service.save_user(memory)
    return {"status": "ok", "saved": memory.dict()}

@router.post("/conversation")
def save_conversation(memory: ConversationMemory):
    memory_service.save_conversation(memory)
    return {"status": "ok", "saved": memory.dict()}

@router.get("/context/{userId}")
def get_context(userId: str):
    return memory_service.get_context(userId)
