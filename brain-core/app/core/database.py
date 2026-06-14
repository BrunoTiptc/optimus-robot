# app/core/database.py
import os
from typing import Optional

from app.core.config import Config

try:
    from google.auth.exceptions import DefaultCredentialsError
    from google.cloud import firestore
    FIRESTORE_SDK_AVAILABLE = True
except ImportError:
    firestore = None  # type: ignore
    DefaultCredentialsError = Exception  # type: ignore
    FIRESTORE_SDK_AVAILABLE = False
    print(
        "[FIRESTORE-ALERTA]: google-cloud-firestore ou google-auth"
        " não está instalado."
    )
    print(
        "O servidor seguirá em modo local sem suporte ao Firestore."
    )


def get_firestore_client() -> Optional["firestore.Client"]:
    """
    Inicializa e retorna o cliente do Firestore configurado corretamente.
    Suporta o Emulador Local se a env FIRESTORE_EMULATOR_HOST existir.
    """
    if not FIRESTORE_SDK_AVAILABLE:
        return None

    emulator_host = os.getenv("FIRESTORE_EMULATOR_HOST")

    if emulator_host:
        print(
            f"[FIRESTORE]: Conectando ao Emulador Local em {emulator_host}"
        )
        # O SDK do Google reconhece FIRESTORE_EMULATOR_HOST automaticamente.

    elif not Config.GOOGLE_APPLICATION_CREDENTIALS:
        print(
            "⚠️ [FIRESTORE-ALERTA]: GOOGLE_APPLICATION_CREDENTIALS "
            "não foi definida."
        )
        print(
            "O SDK tentará usar as Application Default Credentials "
            "(ADC) do sistema."
        )

    try:
        return firestore.Client(project=Config.FIREBASE_PROJECT_ID)
    except DefaultCredentialsError as e:
        print(
            "⚠️ [FIRESTORE-ALERTA]: Não foi possível obter credenciais do "
            "Google Cloud."
        )
        print(f"   {e}")
        print(
            "O servidor seguirá em modo local sem suporte ao Firestore remoto."
        )
        return None
    except Exception as e:
        print("⚠️ [FIRESTORE-ALERTA]: Falha ao inicializar o Firestore.")
        print(f"   {e}")
        print("O servidor seguirá em modo local sem suporte ao Firestore.")
        return None


# Instância única para ser importada nos serviços (Singleton)
db = get_firestore_client()
