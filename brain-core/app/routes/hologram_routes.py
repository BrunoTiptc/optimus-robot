import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.redis_client import redis_client

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
                # Remove conexões fantasmas ou corrompidas
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
            # Verifica se há novas mensagens no Redis de forma não-bloqueante
            message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and message.get("type") == "message":
                event_data = json.loads(message["data"])
                
                # Encaminha o evento limpo para o front-end (main.js)
                await manager.broadcast_json({
                    "event": event_data.get("event_type"),
                    "payload": event_data.get("data")
                })
            
            # 👇 LINHA CRUCIAL ADICIONADA: Libera o Event Loop para o FastAPI respirar e aceitar conexões
            await asyncio.sleep(0.1)
            
        except Exception as e:
            # Evita que erros matem o loop infinito
            await asyncio.sleep(1)
            
@router.websocket("/ws/hologram")
async def websocket_endpoint(websocket: WebSocket):
    """Rota que o index.html e o main.js chamam para abrir o canal de luz"""
    await manager.connect(websocket)
    try:
        # Envia uma mensagem inicial de boas-vindas assim que conecta
        await websocket.send_json({"event": "system_ready", "payload": {"status": "online"}})
        
        while True:
            # Mantém a conexão viva ouvindo possíveis comandos vindos do Front (se houver)
            data = await websocket.receive_text()
            # Se o front enviar um ping, respondemos com pong para manter o túnel aberto
            if data == "ping":
                await websocket.send_text("pong")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
