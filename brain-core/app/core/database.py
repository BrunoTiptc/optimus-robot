# app/core/database.py
import os
from google.cloud import firestore
from app.core.config import Config

def get_firestore_client() -> firestore.Client:
    """
    Inicializa e retorna o cliente do Firestore configurado corretamente.
    Suporta automaticamente o Emulador Local se a env FIRESTORE_EMULATOR_HOST existir.
    """
    emulator_host = os.getenv("FIRESTORE_EMULATOR_HOST")
    
    if emulator_host:
        print(f"🔥 [FIRESTORE]: Conectando ao Emulador Local em {emulator_host}")
        # O próprio SDK do Google reconhece a env FIRESTORE_EMULATOR_HOST, 
        # mas precisamos garantir que o project_id esteja setado.
        return firestore.Client(project=Config.FIREBASE_PROJECT_ID)
    
    # Validação para Produção
    if not Config.GOOGLE_APPLICATION_CREDENTIALS:
        print("⚠️ [FIRESTORE-ALERTA]: GOOGLE_APPLICATION_CREDENTIALS não foi definida.")
        print("O SDK tentará usar as Application Default Credentials (ADC) do sistema.")
        
    return firestore.Client(project=Config.FIREBASE_PROJECT_ID)

# Instância única para ser importada nos serviços (Singleton)
db = get_firestore_client()