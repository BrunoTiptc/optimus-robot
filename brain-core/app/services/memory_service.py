from google.cloud import firestore
from datetime import datetime
from typing import Dict, Any, List

db = firestore.Client()

class WatsonSessionMemory:
    """
    Serviço de Memória inspirado no IBM Watson Assistant.
    Gerencia estados e variáveis de contexto de forma consolidada por sessão,
    evitando a geração de registros avulsos (lixo) no Firestore e acelerando a NLP.
    """

    @staticmethod
    def get_or_create_session(userId: str, sessionId: str) -> Dict[str, Any]:
        """
        Recupera ou inicializa o contexto de uma sessão única no Firestore.
        Em vez de criar dezenas de linhas no banco, mantemos um único documento de estado.
        """
        doc_ref = db.collection("sessions").document(sessionId)
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        
        # Inicializa o contexto padrão da sessão (Watson Context Variables)
        initial_context = {
            "sessionId": sessionId,
            "userId": userId,
            "createdAt": datetime.utcnow(),
            "lastInteraction": datetime.utcnow(),
            "turnCount": 0,
            # Variáveis de contexto dinâmicas da conversa (Intenções, preferências capturadas)
            "contextVariables": {
                "user_name": None,
                "current_intent": "idle",
                "flow_step": "start",
                "preferences": {}
            },
            # Histórico rotativo leve (sliding window) para NLP sem lixo
            "recentTurns": []
        }
        doc_ref.set(initial_context)
        return initial_context

    @staticmethod
    def update_session(userId: str, sessionId: str, user_input: str, bot_response: str, extracted_variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Atualiza o contexto de uma sessão existente. 
        Mantém apenas as últimas 5 interações em memória rápida (recentTurns) para a NLP do cérebro.
        """
        doc_ref = db.collection("sessions").document(sessionId)
        session = doc_ref.get().to_dict()
        
        if not session:
            session = WatsonSessionMemory.get_or_create_session(userId, sessionId)

        # 1. Incrementa contagem de turnos
        session["turnCount"] += 1
        session["lastInteraction"] = datetime.utcnow()

        # 2. Atualiza variáveis de contexto (Watson Context Slots)
        if extracted_variables:
            session["contextVariables"].update(extracted_variables)

        # 3. Adiciona a nova interação ao sliding window
        new_turn = {
            "input": user_input,
            "response": bot_response,
            "timestamp": datetime.utcnow()
        }
        
        recent_turns: List[Dict[str, Any]] = session.get("recentTurns", [])
        recent_turns.append(new_turn)
        
        # Mantém no máximo as últimas 5 mensagens para NLP leve e sem lag
        if len(recent_turns) > 5:
            recent_turns.pop(0)
            
        session["recentTurns"] = recent_turns

        # 4. Atualiza o documento único na nuvem
        doc_ref.set(session)
        return session

    @staticmethod
    def consolidate_to_summary(userId: str, sessionId: str) -> Dict[str, Any]:
        """
        Consolida a conversa inteira em um resumo estruturado de perfil do usuário.
        Limpa os logs temporários de conversa e grava apenas os fatos cruciais na coleção 'users' e 'summaries',
        garantindo um banco de dados limpo e performante.
        """
        session_ref = db.collection("sessions").document(sessionId)
        session = session_ref.get().to_dict()

        if not session:
            return {"status": "error", "message": "Session not found"}

        # Extrai os dados consolidados coletados na sessão
        context_vars = session.get("contextVariables", {})
        recent_turns = session.get("recentTurns", [])
        
        # Cria um resumo conciso das decisões/assuntos discutidos
        summary_text = f"Sessão finalizada com {session['turnCount']} turnos. "
        if recent_turns:
            summary_text += f"Último comando recebido: '{recent_turns[-1]['input']}'."

        # 1. Atualiza dados globais na coleção de Usuários
        user_ref = db.collection("users").document(userId)
        user_doc = user_ref.get()
        
        user_data = {
            "userId": userId,
            "lastInteraction": datetime.utcnow(),
            "preferences": context_vars.get("preferences", {}),
            "name": context_vars.get("user_name") or "Optimus Operator"
        }
        
        if user_doc.exists:
            # Merge das preferências existentes
            existing_data = user_doc.to_dict()
            existing_prefs = existing_data.get("preferences", {})
            existing_prefs.update(context_vars.get("preferences", {}))
            user_data["preferences"] = existing_prefs
            
        user_ref.set(user_data, merge=True)

        # 2. Salva o resumo consolidado na coleção de Resumos para futuras consultas NLP
        summary_id = f"summary_{sessionId}"
        db.collection("summaries").document(summary_id).set({
            "sessionId": sessionId,
            "userId": userId,
            "summary": summary_text,
            "contextVariables": context_vars,
            "consolidatedAt": datetime.utcnow()
        })

        # 3. Limpa o documento de sessão temporário para evitar desperdício de espaço no Firestore
        session_ref.delete()

        return {
            "status": "success",
            "message": "Sessão Watson consolidada e memória limpa com sucesso!",
            "summaryId": summary_id
        }

# Compatibilidade com as rotas FastAPI existentes
def save_user(memory: Any):
    db.collection("users").document(memory.userId).set(memory.dict())

def save_conversation(memory: Any):
    db.collection("conversations").document(memory.timestamp.isoformat()).set(memory.dict())

def get_context(userId: str):
    user = db.collection("users").document(userId).get().to_dict()
    conversations = db.collection("conversations").where("userId", "==", userId).stream()
    conv_list = [c.to_dict() for c in conversations]
    return {"user": user, "conversations": conv_list}
