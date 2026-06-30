import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.redis_client import redis_client
# Importe o seu cliente do Firebase se já tiver ele configurado, ex:
# from app.core.firebase_client import firestore_db
from app.core.redis_client import redis_client
from app.core.firebase_client import firestore_db 

router = APIRouter() 

class ConnectionManager:
    """Gerencia as conexões ativas de WebSockets do Holograma"""
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✨ [WEBSOCKET]: Holograma conectado! Total de telas ativos: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"❌ [WEBSOCKET]: Holograma desconectado. Telas ativas: {len(self.active_connections)}")

    async def broadcast_json(self, data: dict):
        """Dispara os dados para todas as telas ou projetores conectados simultaneamente"""
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                print(f"⚠️  [WEBSOCKET-ERRO]: Falha ao enviar dados para uma tela: {e}")

manager = ConnectionManager()

async def redis_event_listener():
    """
    Worker assíncrono em background (Pub/Sub).
    Ele intercepta o evento 'optimus:hologram:speech' e repassa via WebSocket.
    """
    pubsub = redis_client.pubsub()
    pubsub.subscribe("optimus:hologram:speech")
    
    print("📢 [WORKER]: Ouvindo eventos de voz do Optimus no Redis...")
    
    while True:
        try:
            message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and message.get("type") == "message":
                event_data = json.loads(message["data"])
                
                await manager.broadcast_json({
                    "event": event_data.get("event_type"),
                    "payload": event_data.get("data")
                })
            
            await asyncio.sleep(0.1)
            
        except Exception as e:
            await asyncio.sleep(1)


async def infra_status_monitor():
    """
    Worker assíncrono que monitora o Redis e as sessões reais do Firestore.
    """
    print("🔋 [WORKER]: Monitor de Infraestrutura (Redis/Firestore) Ativo!")
    while True:
        try:
            # 1. Checa status e busca chaves do Redis
            redis_status = "disconnected"
            redis_keys = []
            try:
                if redis_client.ping():
                    # Se o Redis for a classe real (não o Dummy), ele retorna conectado
                    if not hasattr(redis_client, 'storage'): 
                        redis_status = "connected"
                        keys_bytes = redis_client.keys("optimus:*")
                        redis_keys = [k.decode("utf-8") if isinstance(k, bytes) else k for k in keys_bytes]
                    else:
                        redis_status = "fallback_mock"
            except Exception:
                redis_status = "disconnected"

            # 2. Checa status e busca sessões reais do Firestore
            firestore_status = "disconnected"
            real_sessions = []
            
            if firestore_db is not None:
                try:
                    firestore_status = "connected"
                    # Supondo que sua coleção no Firestore se chame 'sessions'
                    sessions_ref = firestore_db.collection("sessions").limit(5).stream()
                    for doc in sessions_ref:
                        doc_data = doc.to_dict()
                        real_sessions.append({
                            "id": doc.id,
                            "userId": doc_data.get("userId", "Desconhecido")
                        })
                except Exception as fs_err:
                    print(f"⚠️ [FIRESTORE-SAÚDE]: Erro ao ler coleção: {fs_err}")
                    firestore_status = "error"
            else:
                firestore_status = "disconnected"

            # 3. Dispara para o front-end se houver telas conectadas
            if manager.active_connections:
                await manager.broadcast_json({
                    "event": "infra_status",
                    "payload": {
                        "firestore": firestore_status,
                        "redis": redis_status,
                        "sessions": real_sessions,
                        "redis_keys": redis_keys
                    }
                })

        except Exception as e:
            print(f"⚠️ [MONITOR-ERRO]: Falha ao coletar dados de infra: {e}")
            
        await asyncio.sleep(5)

@router.websocket("/ws/hologram")
async def websocket_endpoint(websocket: WebSocket):
    """Rota que o index.html e o main.js chamam para abrir o canal de luz"""
    await manager.connect(websocket)
    try:
        await websocket.send_json({"event": "system_ready", "payload": {"status": "online"}})
        
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)