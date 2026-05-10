from fastapi import APIRouter

router = APIRouter(prefix="/decision", tags=["decision"])

@router.post("/")
def decide_action(userId: str, input: str):
    if "motor" in input.lower():
        return {"decision": "ligar motor", "validated": True}
    return {"decision": "responder via IA", "validated": False}
