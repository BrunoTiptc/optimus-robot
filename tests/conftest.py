import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient

# Garante o loop de eventos correto para testes assíncronos
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Mock do serviço de IA para não gastar tokens de API real nos testes
@pytest.fixture
def mock_ai_service():
    service = MagicMock()
    service.generate_response = AsyncMock(return_value="Olá! Eu sou o Optimus.")
    service.analyze_image = AsyncMock(return_value={"status": "success", "detected": "human face"})
    return service

# Mock do serviço de memória/banco de dados de contexto
@pytest.fixture
def mock_memory_service():
    service = MagicMock()
    service.get_context = AsyncMock(return_value="Contexto: Holograma ativado.")
    service.save_interaction = AsyncMock(return_value=True)
    return service