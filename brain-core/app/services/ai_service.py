import os
import re
from typing import Dict, Any, Tuple
from app.core.event_bus import event_bus

# Tenta carregar LangChain/OpenAI se a chave estiver configurada
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HAS_OPENAI = len(OPENAI_API_KEY) > 0 and OPENAI_API_KEY != "your_key_here"

LANGCHAIN_AVAILABLE = False
OPENAI_MODEL_CLASS = None
if HAS_OPENAI:
    try:
        from langchain.chat_models import ChatOpenAI
        OPENAI_MODEL_CLASS = ChatOpenAI
        from langchain.schema import SystemMessage, HumanMessage, AIMessage
        LANGCHAIN_AVAILABLE = True
        print("[AI-SERVICE] Chave OpenAI ativa. LangChain ChatOpenAI inicializado.")
    except Exception as e1:
        try:
            from langchain.chat_models import OpenAI as ChatOpenAI
            OPENAI_MODEL_CLASS = ChatOpenAI
            from langchain.schema import SystemMessage, HumanMessage, AIMessage
            LANGCHAIN_AVAILABLE = True
            print("[AI-SERVICE] Chave OpenAI ativa. LangChain OpenAI inicializado.")
        except Exception as e2:
            try:
                from langchain import ChatOpenAI
                OPENAI_MODEL_CLASS = ChatOpenAI
                from langchain.schema import SystemMessage, HumanMessage, AIMessage
                LANGCHAIN_AVAILABLE = True
                print("[AI-SERVICE] Chave OpenAI ativa. LangChain import ChatOpenAI inicializado.")
            except Exception as e3:
                try:
                    from langchain import OpenAI as ChatOpenAI
                    OPENAI_MODEL_CLASS = ChatOpenAI
                    from langchain.schema import SystemMessage, HumanMessage, AIMessage
                    LANGCHAIN_AVAILABLE = True
                    print("[AI-SERVICE] Chave OpenAI ativa. LangChain import OpenAI inicializado.")
                except Exception as e4:
                    try:
                        from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage
                        from langchain.chat_models import OpenAI as ChatOpenAI
                        OPENAI_MODEL_CLASS = ChatOpenAI
                        LANGCHAIN_AVAILABLE = True
                        print("[AI-SERVICE] Chave OpenAI ativa. LangChain OpenAI (schema.messages) inicializado.")
                    except Exception as e5:
                        LANGCHAIN_AVAILABLE = False
                        print(f"[AI-SERVICE-ALERTA] Falha ao importar LangChain ({e1 if e1 else e2 if e2 else e3 if e3 else e4 if e4 else e5}). Usando NLP local.")


class AIService:
    """
    Serviço Inteligente do Cérebro do Optimus.
    Realiza o processamento híbrido: LangChain GPT ou NLP Local baseada no Watson Assistant.
    """

    @staticmethod
    def process_message(user_input: str, session: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Processa o input do usuário usando IA (OpenAI) ou o motor local Watson,
        realizando extração de variáveis de contexto (Slot-Filling) e publicando eventos.
        """
        extracted_vars = {}
        user_name = session.get("contextVariables", {}).get("user_name")
        current_intent = "idle"

        # 1. MOTOR DE EXTRAÇÃO DE SLOTS LOCAL (Watson Assistant Concept)
        name_match = re.search(
            r"(?:meu nome é|me chamo|sou o|sou a|aqui é o|aqui é a)\s+([a-zA-Záéíóúãõç]+)",
            user_input,
            re.IGNORECASE,
        )
        if name_match:
            extracted_name = name_match.group(1).capitalize()
            extracted_vars["user_name"] = extracted_name
            user_name = extracted_name
            current_intent = "identificacao"

        pref_match = re.search(
            r"(?:gosto de|minha preferência é|mude para o modo)\s+([a-zA-Z]+)",
            user_input,
            re.IGNORECASE,
        )
        if pref_match:
            preference_val = pref_match.group(1).lower()
            current_prefs = session.get("contextVariables", {}).get("preferences", {})
            current_prefs["last_extracted_preference"] = preference_val
            extracted_vars["preferences"] = current_prefs
            current_intent = "preferencia"

        # 2. SELEÇÃO DO PROVEDOR DE INTELIGÊNCIA ARTIFICIAL
        if LANGCHAIN_AVAILABLE:
            response = AIService._query_openai(user_input, session, user_name)
        else:
            response, detected_intent = AIService._query_local_watson_nlp(user_input, user_name)
            if detected_intent != "idle":
                current_intent = detected_intent

        # Atualiza a intenção atual identificada
        extracted_vars["current_intent"] = current_intent

        # 3. MENSAGERIA ASSÍNCRONA (Redis)
        try:
            event_bus.publish_event(
                channel="optimus:hologram:speech",
                event_type="hologram_speech_triggered",
                data={
                    "userId": session.get("userId"),
                    "sessionId": session.get("sessionId"),
                    "input": user_input,
                    "intent": current_intent,
                    "responseSnippet": (response[:40] + "...") if isinstance(response, str) else str(response)[:40] + "...",
                },
            )
        except Exception:
            # Silencia falhas de publish (ex.: DummyRedis em dev)
            pass

        return response, extracted_vars

    @staticmethod
    def _query_openai(user_input: str, session: Dict[str, Any], user_name: str) -> str:
        """
        Executa uma consulta inteligente via OpenAI usando LangChain ChatOpenAI.
        """
        try:
            if OPENAI_MODEL_CLASS is None:
                raise RuntimeError("OPENAI_MODEL_CLASS não foi inicializado")
            chat = OPENAI_MODEL_CLASS(model_name="gpt-3.5-turbo", temperature=0.7)

            system_prompt = (
                "Você é o cérebro virtual do Optimus Robot, um assistente de IA holográfico "
                "que atua como um 'Espelho Mágico' cyberpunk premium.\n"
                "Mantenha as respostas concisas, inteligentes, cativantes e sempre em português brasileiro.\n"
            )
            if user_name:
                system_prompt += f"O operador atual se chama {user_name}. Trate-o por esse nome.\n"
            else:
                system_prompt += "Você ainda não sabe o nome do operador. Se ele disser o nome, agradeça e grave.\n"

            recent_turns = session.get("recentTurns", [])
            messages = [SystemMessage(content=system_prompt)]

            for turn in recent_turns:
                # adiciona histórico de usuário e resposta do assistente ao contexto
                messages.append(HumanMessage(content=turn.get("input", "")))
                messages.append(HumanMessage(content=turn.get("response", "")))

            messages.append(HumanMessage(content=user_input))

            response = chat(messages)

            # ChatOpenAI pode retornar AIMessage ou um objeto mais complexo
            if hasattr(response, "content"):
                return response.content
            try:
                # tentativa para acessar geração em versões diferentes do LangChain
                return response.generations[0][0].text
            except Exception:
                return str(response)

        except Exception as e:
            print(f"[AI-SERVICE-ERRO] Falha ao consultar OpenAI ({e}). Usando NLP local de contingência.")
            res, _ = AIService._query_local_watson_nlp(user_input, user_name)
            return res

    @staticmethod
    def _query_local_watson_nlp(user_input: str, user_name: str) -> Tuple[str, str]:
        """
        Motor NLP local baseado em regras (contingência amigável).
        """
        text = user_input.lower()
        operator = user_name if user_name else "Operador"

        if any(greet in text for greet in ["olá", "oi", "bom dia", "boa tarde", "boa noite", "hello", "hi"]):
            return (
                f"Olá, {operator}! Eu sou o cérebro virtual do Optimus. "
                "Estou pronto e com conexão WebSocket ativa para receber suas instruções!",
                "saudacao",
            )

        if "meu nome é" in text or "me chamo" in text:
            return (
                f"Entendido perfeitamente, {operator}! Salvei o seu nome na minha memória "
                "de contexto do Watson Assistant. O Firestore foi atualizado na nuvem!",
                "identificacao",
            )

        if any(word in text for word in ["status", "diagnóstico", "operação", "como você está", "funcionamento"]):
            return (
                f"Diagnóstico do hospedeiro virtual Optimus completo: "
                "Cérebro FastAPI online, WebSockets em sub-milissegundos ativos e Firebase Firestore sincronizado. "
                f"Estou pronto para servir você, {operator}!",
                "diagnostico",
            )

        if "espelho" in text:
            return (
                f"Espelho, espelho meu... Existe algum robô mais avançado do que eu neste ecossistema distribuído? "
                f"Brincadeiras à parte, {operator}, sinto orgulho de ser o seu hospedeiro virtual!",
                "espelho_magico",
            )

        if any(word in text for word in ["inteligência", "ia", "artificial", "tecnologia", "watson", "firestore"]):
            return (
                "Minha inteligência é baseada em sessões otimizadas baseadas nas melhores práticas de IA do IBM Watson. "
                "Isso me permite consolidar nossa conversa e evitar o lag ou lixo no Firestore!",
                "tecnologia",
            )

        if any(bye in text for bye in ["tchau", "adeus", "até logo", "encerrar", "fechar", "sair"]):
            return (
                f"Até logo, {operator}! Vou manter o canal de holograma em modo de respiração suave. "
                "Quando quiser falar, basta me acionar!",
                "despedida",
            )

        return (
            f"Recebi seu comando, {operator}: '{user_input}'. Meu motor Watson NLP "
            "processou seu evento e registrou o log no Firestore na nuvem! O que faremos a seguir?",
            "contingencia",
        )


ai_service = AIService()
