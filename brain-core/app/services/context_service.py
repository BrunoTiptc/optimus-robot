from typing import Dict, Any, Optional
from datetime import datetime

from app.core.database import db


def _firestore_available() -> bool:
    return db is not None


class ContextService:
    """Serviço leve de contexto de usuário e enriquecimento de sessão.

    Fornece helpers para ler/atualizar perfil de usuário no Firestore e
    enriquecer sessões antes de enviar para a IA.
    """

    @staticmethod
    def get_user_profile(user_id: str) -> Dict[str, Any]:
        """Retorna o documento do usuário ou um dicionário vazio se não existir."""
        if not _firestore_available():
            return {}

        try:
            doc = db.collection("users").document(user_id).get()
            if doc.exists:
                return doc.to_dict()
        except Exception as e:
            print(f"[CONTEXT_SERVICE] erro ao ler perfil do usuário: {e}")
        return {}

    @staticmethod
    def update_user_preferences(user_id: str, preferences: Dict[str, Any]) -> bool:
        """Merge simples das preferências fornecidas no documento do usuário."""
        if not _firestore_available():
            print("[CONTEXT_SERVICE] Firestore indisponível: preferências não serão persistidas.")
            return False

        try:
            user_ref = db.collection("users").document(user_id)
            user_doc = user_ref.get()
            base = user_doc.to_dict() if user_doc.exists else {}
            existing = base.get("preferences", {}) if base else {}
            existing.update(preferences or {})
            user_ref.set({"preferences": existing}, merge=True)
            return True
        except Exception as e:
            print(f"[CONTEXT_SERVICE] falha ao atualizar preferencias: {e}")
            return False

    @staticmethod
    def enrich_session_with_profile(session: Dict[str, Any]) -> Dict[str, Any]:
        """Anexa dados do perfil do usuário à sessão (por referência) e retorna a sessão enriquecida.

        Use quando for enviar contexto rico para `ai_service`.
        """
        try:
            user_id = session.get("userId")
            if not user_id:
                return session

            profile = ContextService.get_user_profile(user_id)
            # Merge preferencias e nome se existirem
            context_vars = session.get("contextVariables", {})
            profile_prefs = profile.get("preferences", {}) if profile else {}
            merged_prefs = {**profile_prefs, **context_vars.get("preferences", {})}
            context_vars.setdefault("preferences", {})
            context_vars["preferences"] = merged_prefs

            # Se o usuário tiver nome salvo, assegura que fique no contexto
            if profile.get("name") and not context_vars.get("user_name"):
                context_vars["user_name"] = profile.get("name")

            session["contextVariables"] = context_vars
            return session
        except Exception as e:
            print(f"[CONTEXT_SERVICE] erro ao enriquecer sessão: {e}")
            return session


__all__ = ["ContextService"]
# context_service.py (Continuação / Extensão para Agregação de Perfil)
import time
from typing import Dict, Any, List

class ProfileAggregationService:
    """
    Serviço de agregação de perfil focado em analisar históricos consolidados 
    do Firestore (summaries) para extrair padrões de comportamento e enriquecer 
    a experiência em primeira pessoa com o Optimus Robot.
    """
    def __init__(self, firestore_client=None):
        # Injeção do cliente do Firestore (ou use sua abstração de banco de dados)
        self.db = firestore_client

    def fetch_user_session_summaries(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Busca no Firestore os resumos consolidados de todas as sessões anteriores 
        para evitar ter que ler o histórico bruto de mensagens toda vez.
        """
        try:
            # Conceito de leitura otimizada no Firestore para mitigar custos de leitura/lag
            if self.db:
                summaries_ref = self.db.collection("users").document(user_id).collection("session_summaries")
                docs = summaries_ref.order_by("timestamp", direction="DESCENDING").limit(10).stream()
                return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"[PROFILE-SERVICE-ERRO] Falha ao ler summaries do Firestore: {e}")
        
        # Mock/Fallback para desenvolvimento local ou falhas de rede
        return [
            {"summary": "Usuário estudou Playwright cansado e reclamou de boletos.", "mood": "tired", "timestamp": time.time() - 86400},
            {"summary": "Usuário configurou o .env.example e testou o emulador local.", "mood": "focused", "timestamp": time.time() - 172800}
        ]

    def extract_behavioral_traits(self, session_summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Varre os summaries consolidados usando NLP baseado em regras ou heurísticas 
        para extrair os traços comportamentais, preferências de longa data e tópicos frequentes.
        """
        text_pool = " ".join([s.get("summary", "").lower() for s in session_summaries])
        
        traits = {
            "frequent_topics": [],
            "predominant_mood": "neutral",
            "interaction_style": "premium_cyberpunk",
            "detected_routines": []
        }

        # Heurísticas locais de Slot-Filling/Agregação (Watson Assistant Concept para Longo Prazo)
        if any(word in text_pool for word in ["estudar", "playwright", "pydantic", "fastapi", "code"]):
            traits["frequent_topics"].append("desenvolvimento_software")
        if any(word in text_pool for word in ["arthur", "filho", "cuidar"]):
            traits["frequent_topics"].append("familia")
        if any(word in text_pool for word in ["holograma", "película", "led", "motores"]):
            traits["frequent_topics"].append("hardware_robotica")

        # Análise simples de humor agregado
        moods = [s.get("mood") for s in session_summaries if s.get("mood")]
        if moods:
            traits["predominant_mood"] = max(set(moods), key=moods.count)

        # Detectando rotinas implícitas relatadas nos históricos
        if "duolingo" in text_pool:
            traits["detected_routines"].append("estudo_idiomas_noturno")
        if "cansado" in text_pool or "boleto" in text_pool:
            traits["detected_routines"].append("rotina_exaustiva_pos_servico")

        return traits

    def enrich_ai_context(self, user_id: str, current_session_ctx: Dict[str, Any]) -> Dict[str, Any]:
        """
        Consolida a memória de curto prazo (sessão ativa) com o perfil de longo prazo
        extraído do Firestore, gerando a base final de conhecimento para o ai_service.py.
        """
        # 1. Recupera históricos salvos
        summaries = self.fetch_user_session_summaries(user_id)
        
        # 2. Extrai traços de comportamento de longo prazo
        long_term_traits = self.extract_behavioral_traits(summaries)
        
        # 3. Une com os metadados da sessão atual
        enriched_context = {
            **current_session_ctx,
            "user_profile_traits": long_term_traits,
            "last_aggregated_update": time.time()
        }
        
        return enriched_context

# Instanciação global do serviço
profile_aggregation_service = ProfileAggregationService()