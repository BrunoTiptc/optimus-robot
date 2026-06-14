import pytest
from unittest.mock import AsyncMock, patch
# Supondo a localização do seu serviço de IA
from app.services.ai_service import AIService 

@pytest.mark.asyncio
async def test_ai_generation_success():
    """Garante que o processador de texto da IA retorna a string limpa esperada"""
    ai_service = AIService()
    
    # Mockando a chamada interna da API do Gemini/OpenAI
    with patch.object(ai_service, 'client', new_callable=AsyncMock) as mock_client:
        mock_client.generate_content.return_value.text = "Presença confirmada."
        
        response = await ai_service.process_user_input("Você está aí, Optimus?")
        assert response == "Presença confirmada."

@pytest.mark.asyncio
async def test_ai_fallback_on_failure():
    """Testa se o sistema tem uma resposta de contingência (fallback) se a API da IA cair"""
    ai_service = AIService()
    
    with patch.object(ai_service, 'client', side_effect=Exception("API Down")):
        # O robô não pode quebrar se a internet/API falhar, deve retornar uma resposta segura
        response = await ai_service.process_user_input("Alô?")
        assert "modo de segurança" in response.lower() or "sistema temporariamente indisponível" in response.lower()