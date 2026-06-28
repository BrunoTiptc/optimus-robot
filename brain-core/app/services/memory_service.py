# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any, Dict, List

from app.core.database import db

_local_sessions: Dict[str, Dict[str, Any]] = {}
_local_users: Dict[str, Dict[str, Any]] = {}
_local_conversations: List[Dict[str, Any]] = []


def _firestore_available() -> bool:
    return db is not None


def _build_initial_session(userId: str, sessionId: str) -> Dict[str, Any]:
    return {
        "sessionId": sessionId,
        "userId": userId,
        "createdAt": datetime.utcnow(),
        "lastInteraction": datetime.utcnow(),
        "turnCount": 0,
        "contextVariables": {
            "user_name": None,
            "current_intent": "idle",
            "flow_step": "start",
            "preferences": {},
        },
        "recentTurns": [],
    }


class WatsonSessionMemory:
    """
    Serviço de memória inspirado no IBM Watson Assistant.
    Garante estado de sessão consolidado e evita lixo no Firestore.
    """

    @staticmethod
    def get_or_create_session(userId: str, sessionId: str) -> Dict[str, Any]:
        """
        Recupera ou inicializa o contexto de uma sessão única.
        Mantém um único documento de estado em vez de criar muitos registros.
        """
        if not _firestore_available():
            session = _local_sessions.get(sessionId)
            if session:
                return session

            initial_context = _build_initial_session(userId, sessionId)
            _local_sessions[sessionId] = initial_context
            return initial_context

        doc_ref = db.collection("sessions").document(sessionId)
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()

        initial_context = _build_initial_session(userId, sessionId)
        doc_ref.set(initial_context)
        return initial_context

    @staticmethod
    def update_session(
        userId: str,
        sessionId: str,
        user_input: str,
        bot_response: str,
        extracted_variables: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Atualiza o contexto de uma sessão existente.
        Mantém apenas as cinco últimas interações para NLP leve.
        """
        if not _firestore_available():
            session = _local_sessions.get(sessionId)
            if not session:
                session = WatsonSessionMemory.get_or_create_session(
                    userId,
                    sessionId,
                )

            session["turnCount"] += 1
            session["lastInteraction"] = datetime.utcnow()

            if extracted_variables:
                session["contextVariables"].update(extracted_variables)

            new_turn = {
                "input": user_input,
                "response": bot_response,
                "timestamp": datetime.utcnow(),
            }
            recent_turns: List[Dict[str, Any]] = session.get("recentTurns", [])
            recent_turns.append(new_turn)
            if len(recent_turns) > 5:
                recent_turns.pop(0)
            session["recentTurns"] = recent_turns
            _local_sessions[sessionId] = session
            return session

        doc_ref = db.collection("sessions").document(sessionId)
        session = doc_ref.get().to_dict()
        if not session:
            session = WatsonSessionMemory.get_or_create_session(
                userId,
                sessionId,
            )

        session["turnCount"] += 1
        session["lastInteraction"] = datetime.utcnow()

        if extracted_variables:
            session["contextVariables"].update(extracted_variables)

        new_turn = {
            "input": user_input,
            "response": bot_response,
            "timestamp": datetime.utcnow(),
        }
        recent_turns: List[Dict[str, Any]] = session.get("recentTurns", [])
        recent_turns.append(new_turn)
        if len(recent_turns) > 5:
            recent_turns.pop(0)
        session["recentTurns"] = recent_turns

        doc_ref.set(session)
        return session

    @staticmethod
    def consolidate_to_summary(userId: str, sessionId: str) -> Dict[str, Any]:
        """
        Consolida a sessão em um resumo de perfil e limpa o estado temporário.
        """
        if not _firestore_available():
            session = _local_sessions.pop(sessionId, None)
            if not session:
                return {"status": "error", "message": "Session not found"}

            context_vars = session.get("contextVariables", {})
            recent_turns = session.get("recentTurns", [])
            summary_text = (
                f"Sessão finalizada com {session['turnCount']} turnos. "
            )
            if recent_turns:
                summary_text += (
                    f"Último comando recebido: '{recent_turns[-1]['input']}'."
                )

            existing_data = _local_users.get(userId, {})
            existing_prefs = existing_data.get("preferences", {})
            user_data = {
                "userId": userId,
                "lastInteraction": datetime.utcnow(),
                "preferences": {
                    **existing_prefs,
                    **context_vars.get("preferences", {}),
                },
                "name": context_vars.get("user_name") or "Optimus Operator",
            }
            _local_users[userId] = {**existing_data, **user_data}

            summary_id = f"summary_{sessionId}"
            _local_conversations.append(
                {
                    "sessionId": sessionId,
                    "userId": userId,
                    "summary": summary_text,
                    "contextVariables": context_vars,
                    "consolidatedAt": datetime.utcnow(),
                }
            )

            return {
                "status": "success",
                "message": (
                    "Sessão Watson consolidada e memória limpa "
                    "com sucesso!"
                ),
                "summaryId": summary_id,
            }

        session_ref = db.collection("sessions").document(sessionId)
        session = session_ref.get().to_dict()
        if not session:
            return {"status": "error", "message": "Session not found"}

        context_vars = session.get("contextVariables", {})
        recent_turns = session.get("recentTurns", [])
        summary_text = (
            f"Sessão finalizada com {session['turnCount']} turnos. "
        )
        if recent_turns:
            summary_text += (
                f"Último comando recebido: '{recent_turns[-1]['input']}'."
            )

        user_ref = db.collection("users").document(userId)
        user_doc = user_ref.get()

        user_data = {
            "userId": userId,
            "lastInteraction": datetime.utcnow(),
            "preferences": context_vars.get("preferences", {}),
            "name": context_vars.get("user_name") or "Optimus Operator",
        }

        if user_doc.exists:
            existing_data = user_doc.to_dict()
            existing_prefs = existing_data.get("preferences", {})
            existing_prefs.update(context_vars.get("preferences", {}))
            user_data["preferences"] = existing_prefs

        user_ref.set(user_data, merge=True)

        summary_id = f"summary_{sessionId}"
        db.collection("summaries").document(summary_id).set(
            {
                "sessionId": sessionId,
                "userId": userId,
                "summary": summary_text,
                "contextVariables": context_vars,
                "consolidatedAt": datetime.utcnow(),
            }
        )

        session_ref.delete()
        return {
            "status": "success",
            "message": (
                "Sessão Watson consolidada e memória limpa "
                "com sucesso!"
            ),
            "summaryId": summary_id,
        }


# Compatibilidade com as rotas FastAPI existentes
def save_user(memory: Any):
    if not _firestore_available():
        _local_users[memory.userId] = memory.dict()
        return

    db.collection("users").document(memory.userId).set(memory.dict())


def save_conversation(memory: Any):
    if not _firestore_available():
        _local_conversations.append(memory.dict())
        return

    db.collection("conversations").document(
        memory.timestamp.isoformat()
    ).set(memory.dict())


def get_context(userId: str):
    if not _firestore_available():
        user = _local_users.get(userId)
        conv_list = [
            c for c in _local_conversations if c.get("userId") == userId
        ]
        return {"user": user, "conversations": conv_list}

    user = db.collection("users").document(userId).get().to_dict()
    conversations = db.collection("conversations").where(
        "userId",
        "==",
        userId,
    ).stream()
    conv_list = [c.to_dict() for c in conversations]
    return {"user": user, "conversations": conv_list}
