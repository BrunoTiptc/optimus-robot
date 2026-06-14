from datetime import datetime
from typing import Any, Dict, Optional
import asyncio

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from app.core.database import db
from app.services.ai_service import ai_service
from app.services.hologram_service import hologram_service
from app.services.memory_service import WatsonSessionMemory

router = APIRouter(prefix="/robot", tags=["robot"])


def _firestore_available() -> bool:
    return db is not None


class RobotAction(BaseModel):
    actionId: str
    userId: str
    command: str
    status: Optional[str] = "pending"
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    userId: str
    sessionId: str
    message: str


class ChatResponse(BaseModel):
    response: str
    userId: str
    sessionId: str
    session: Dict[str, Any]


class ConsolidateRequest(BaseModel):
    userId: str
    sessionId: str


async def simulate_action_execution(action: RobotAction):
    """
    Simulates physical execution of a robot action.
    Atualiza o Hologram e o documento de status no Firestore.
    """
    # 1. Inform Hologram we are processing
    execution_message = f"Executing: {action.command}"
    await hologram_service.update_state("processing", execution_message)

    # Simulate work delay (e.g., 2 seconds for motor rotation or IA processing)
    await asyncio.sleep(2.0)

    # 2. Determine success/failure based on command
    command_lower = action.command.lower()
    success = (
        "fail" not in command_lower
        and "error" not in command_lower
    )
    final_status = "success" if success else "failed"
    hologram_final_state = "success" if success else "error"

    # 3. Update Firestore Document
    if _firestore_available():
        try:
            doc_ref = db.collection("actions").document(action.actionId)
            doc_ref.update(
                {
                    "status": final_status,
                    "completedAt": datetime.utcnow(),
                }
            )
        except Exception as e:
            print(f"Firestore update error: {e}")
    else:
        print(
            "[ROBOT-ROUTES] Firestore indisponível: atualização de "
            "ação omitida para "
            f"{action.actionId}."
        )

    # 4. Update Hologram visual state
    finish_message = f"Action finished: {final_status}"
    await hologram_service.update_state(hologram_final_state, finish_message)

    # 5. Hold visual success/error state for 3 seconds, then return to idle
    await asyncio.sleep(3.0)
    await hologram_service.update_state("idle", "Ready for next command")


@router.post("/action")
async def trigger_robot_action(
    action: RobotAction,
    background_tasks: BackgroundTasks,
):
    """
    Triggers a robot action, saves it to Firestore, and delegates execution.
    """
    if not action.timestamp:
        action.timestamp = datetime.utcnow()

    if _firestore_available():
        try:
            db.collection("actions").document(action.actionId).set(
                {
                    "actionId": action.actionId,
                    "userId": action.userId,
                    "command": action.command,
                    "status": "pending",
                    "timestamp": action.timestamp,
                }
            )
        except Exception as exc:
            detail = f"Firebase connection failed: {exc}"
            raise HTTPException(status_code=500, detail=detail)
    else:
        print(
            "[ROBOT-ROUTES] Firestore indisponível: registro de ação omitido "
            f"para {action.actionId}."
        )

    background_tasks.add_task(simulate_action_execution, action)

    return {
        "status": "received",
        "actionId": action.actionId,
        "message": "Action dispatched and logged to Firestore",
    }


@router.post("/chat", response_model=ChatResponse)
async def robot_chat(chat: ChatRequest):
    """
    Recebe uma mensagem do usuário, processa com IA e atualiza a sessão.
    """
    session = WatsonSessionMemory.get_or_create_session(
        chat.userId,
        chat.sessionId,
    )

    response_text, extracted_vars = ai_service.process_message(
        chat.message,
        session,
    )

    updated_session = WatsonSessionMemory.update_session(
        chat.userId,
        chat.sessionId,
        chat.message,
        response_text,
        extracted_vars,
    )

    return {
        "response": response_text,
        "userId": chat.userId,
        "sessionId": chat.sessionId,
        "session": updated_session,
    }


@router.post("/session/consolidate")
def consolidate_session(request: ConsolidateRequest):
    """
    Consolida a sessão em um resumo e limpa o documento temporário.
    """
    result = WatsonSessionMemory.consolidate_to_summary(
        request.userId,
        request.sessionId,
    )

    if result.get("status") != "success":
        raise HTTPException(
            status_code=404,
            detail=result.get("message", "Session not found"),
        )
    return result
