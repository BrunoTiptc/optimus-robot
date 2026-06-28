import pytest
from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

def test_hologram_status_endpoint():
    """Testa se o endpoint HTTP do status do holograma responde corretamente"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"]

def test_websocket_hologram_connection():
    """Testa a conexao WebSocket do holograma e a troca de mensagens/eventos estruturados"""
    with client.websocket_connect("/ws/hologram") as websocket:
        # Recebe mensagem inicial de boas-vindas
        data = websocket.receive_json()
        assert data["event"] == "system_ready"
        assert data["payload"]["status"] == "online"
        
        # Envia um ping para testar keepalive
        websocket.send_text("ping")
        response = websocket.receive_text()
        assert response == "pong"
