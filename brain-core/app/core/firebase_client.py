import os
import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import Config

_firestore_db = None

def initialize_firestore():
    global _firestore_db
    if _firestore_db is not None:
        return _firestore_db

    try:
        # Puxa o caminho do arquivo JSON validado pelo Pydantic Config
        key_path = Config.GOOGLE_APPLICATION_CREDENTIALS
        
        if key_path and os.path.exists(key_path):
            print(f"🔥 [FIREBASE]: Inicializando via arquivo de credenciais: '{key_path}'...")
            cred = credentials.Certificate(key_path)
        else:
            # Fallback caso o arquivo não seja encontrado na raiz
            alternative_path = "optimus-key.json"
            if os.path.exists(alternative_path):
                print(f"🔥 [FIREBASE]: Inicializando via fallback local '{alternative_path}'...")
                cred = credentials.Certificate(alternative_path)
            else:
                print("⚠️ [FIREBASE-AVISO]: Arquivo de credenciais não encontrado. Firestore operando em modo offline.")
                return None

        # Inicializa o app do Firebase
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'projectId': Config.FIREBASE_PROJECT_ID,
            })
            
        _firestore_db = firestore.client()
        print(f"🔥 [FIREBASE]: Conectado ao Firestore com sucesso no projeto: [{Config.FIREBASE_PROJECT_ID}]")
        return _firestore_db

    except Exception as e:
        print(f"❌ [FIREBASE-ERRO]: Falha ao inicializar SDK: {e}")
        return None

firestore_db = initialize_firestore()