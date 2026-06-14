import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, memory, decision, robot_routes, hologram_routes
from app.routes.hologram_routes import redis_event_listener

app = FastAPI(title="Optimus Virtual Brain")

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
app.include_router(hologram_routes.router)

@app.on_event("startup")
async def startup_event():
    """Dispara o ouvinte do Redis em background sem travar o servidor HTTP"""
    asyncio.create_task(redis_event_listener())
    print("🚀 [SERVER]: Cérebro do Optimus totalmente operacional!")

