import asyncio
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
#from google.genai import types

from app.routes import health, memory, decision, robot_routes, hologram_routes
from app.routes.hologram_routes import redis_event_listener, infra_status_monitor

# 1. Criação do App FastAPI (Essencial estar no topo!)
app = FastAPI(title="Optimus Brain API")

# 2. Configuração do Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Definição do Schema de dados do Chat
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

# 4. Inicialização do Cliente Gemini moderno
# Ele busca automaticamente a variável GOOGLE_API_KEY do seu .env
gemini_key = os.getenv("GOOGLE_API_KEY", "your_gemini_api_key_here")
if gemini_key == "your_gemini_api_key_here" or not gemini_key:
    print("⚠️ [IA-AVISO]: GOOGLE_API_KEY padrão ou ausente detectada. Respostas do robô usarão Fallback local.")
    client = None
else:
    # Cria o client oficial atualizado
    client = genai.Client(api_key=gemini_key)

@app.post("/robot/chat")
async def chat(payload: ChatRequest):
    """
    Endpoint principal de inteligência do Optimus.
    Processa a mensagem com diretrizes prontas e responde via IA.
    """
    user_message = payload.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

    # Se a chave da API não estiver configurada, cai no Fallback local
    if not client:
        return {
            "status": "fallback",
            "author": "Optimus Core Local",
            "message": "Desculpe, mestre. Meu link neural com os servidores externos falhou, mas continuo operacional localmente."
        }

    try:
        # Diretrizes prontas e regras de comportamento do robô (System Instruction)
        system_instruction = (
            "Você é o robô Optimus, uma inteligência artificial embarcada avançada. "
            "Seu hospedeiro e criador é o Bruno César Alves (Bruno Cts). "
            "Responda de forma prestativa, inteligente, focada em engenharia de software e robótica, "
            "e sempre mantendo a persona de um sistema operacional cibernético integrado."
        )

        # Configura as opções usando o novo SDK
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7
        )

        # Gera a resposta usando o modelo estável recomendado pelo Google
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=config
        )
        bot_response = response.text

        # Publica a resposta no Redis para o painel / holograma falar em tempo real
        try:
            from app.core.redis_client import redis_client
            import json
            redis_client.publish("optimus:hologram:speech", json.dumps({
                "event_type": "voice_broadcast",
                "data": {"text": bot_response}
            }))
        except Exception as redis_err:
            print(f"⚠️  [REDIS-CHAT]: Não foi possível enviar áudio para o Pub/Sub: {redis_err}")

        return {
            "status": "success",
            "author": "Gemini AI",
            "message": bot_response
        }

    except Exception as e:
        print(f"❌ [IA-ERRO]: Falha ao processar resposta com o Gemini: {e}")
        return {
            "status": "fallback",
            "author": "Optimus Core Local",
            "message": "Ocorreu uma oscilação nos meus subprocessos de linguagem. Sistema reiniciando barramento local."
        }

# 5. Inclusão das demais Rotas do Sistema
app.include_router(health.router)
app.include_router(memory.router)
app.include_router(decision.router)
app.include_router(robot_routes.router)
app.include_router(hologram_routes.router)

# 6. Evento de Inicialização dos Workers em Segundo Plano
@app.on_event("startup")
async def startup_event():
    """Dispara os ouvintes em background sem travar o servidor HTTP"""
    asyncio.create_task(redis_event_listener())
    asyncio.create_task(infra_status_monitor())
    print("🚀 [SERVER]: Cérebro do Optimus totalmente operacional com monitoramento de infra!")