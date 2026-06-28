import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, memory, decision, robot_routes, hologram_routes
from app.routes.hologram_routes import redis_event_listener
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Garanta que o middleware seja adicionado LOGO APÓS a criação do 'app'
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Libera qualquer porta/origem (tchau erro de CORS!)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/robot/chat")
async def chat():
    return {"message": "Conectado!"}

app.include_router(health.router)
app.include_router(memory.router)
app.include_router(decision.router)
app.include_router(robot_routes.router)
app.include_router(hologram_routes.router)

@app.on_event("startup")
async def startup_event():
    """Dispara o ouvinte do Redis em background sem travar o servidor HTTP"""
    asyncio.create_task(redis_event_listener())
    print("🚀 [SERVER]: Cérebro do Optimus totalmente operacional!")

