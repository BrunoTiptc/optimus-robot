from fastapi import FastAPI
from app.routes import health, memory, decision

app = FastAPI(title="Optimus Brain")

app.include_router(health.router)
app.include_router(memory.router)
app.include_router(decision.router)
