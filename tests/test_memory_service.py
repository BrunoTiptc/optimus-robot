import pytest
# Supondo a localização do seu serviço de memória/vetores
from app.services.memory_service import MemoryService 

@pytest.mark.asyncio
async def test_save_and_retrieve_context():
    """Testa a persistência da memória de curto prazo e recuperação do contexto"""
    memory = MemoryService()
    session_id = "test_session_123"
    
    # Salva uma linha de contexto da conversa
    await memory.save_interaction(
        session_id=session_id, 
        user_msg="Lembrar que o holograma usa película reflexiva.", 
        robot_msg="Entendido, adicionado ao contexto."
    )
    
    # Recupera o contexto para ver se ele traz a informação de volta
    context = await memory.get_context(session_id=session_id)
    assert "holograma" in context.lower()
    assert "película" in context.lower()