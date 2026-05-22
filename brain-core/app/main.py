from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, memory, decision, robot_routes
from app.websocket.socket_manager import manager

app = FastAPI(title="Optimus Brain")

# Configuração de CORS para permitir conexões do frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(memory.router)
app.include_router(decision.router)
app.include_router(robot_routes.router)

@app.websocket("/ws/hologram")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Mantém a conexão ativa escutando heartbeats/mensagens do cliente
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

