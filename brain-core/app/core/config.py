# app/core/config.py
from enum import Enum
from pathlib import Path
from typing import Optional
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Localiza a raiz do projeto para o arquivo .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_CANDIDATES = [
    BASE_DIR / ".env",
    BASE_DIR.parent / ".env",
]
ENV_FILE = next((path for path in ENV_FILE_CANDIDATES if path.exists()), BASE_DIR / ".env")


class AppEnvironment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Configurações e Gerenciamento de Variáveis de Ambiente do Optimus Core.
    A validação de tipos e dados é feita de forma estrita pelo Pydantic.
    """
    
    # --- CONFIGURAÇÕES GERAIS ---
    APP_ENV: AppEnvironment = Field(default=AppEnvironment.DEVELOPMENT)
    PORT: int = Field(default=8000)
    
    # --- INTELIGÊNCIA ARTIFICIAL (Modelos de Linguagem) ---
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    GOOGLE_API_KEY: Optional[str] = Field(default=None)

    # --- BANCO DE DADOS (Google Cloud / Firebase / Firestore) ---
    FIREBASE_PROJECT_ID: str = Field(default="optimus-robot-dev")
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = Field(default=None)

    # --- INFRAESTRUTURA & MENSAGERIA (Redis) ---
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_PASSWORD: Optional[str] = Field(default=None)

    # Propriedade computada dinamicamente com base nas credenciais inseridas
    @computed_field
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    # Flag utilitária rápida
    @property
    def DEBUG(self) -> bool:
        return self.APP_ENV == AppEnvironment.DEVELOPMENT

    # Configuração do comportamento do Pydantic Settings
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore" # Ignora variáveis extras que estejam no .env mas não usamos aqui
    )

    def validate_critical_services(self):
        """
        Garante avisos explícitos no terminal caso chaves fundamentais 
        para o funcionamento básico da IA e do Banco estejam ausentes.
        """
        warnings = []
        if not self.OPENAI_API_KEY and not self.GOOGLE_API_KEY:
            warnings.append("OPENAI_API_KEY ou GOOGLE_API_KEY (Nenhum provedor de IA configurado)")
        if not self.FIREBASE_PROJECT_ID:
            warnings.append("FIREBASE_PROJECT_ID (O Firestore local ou remoto falhará)")
            
        if warnings:
            print("\n[CONFIG-ALERTA]: Componentes vitais ausentes no ambiente:")
            for warn in warnings:
                print(f"   - {warn}")
            print("O cérebro do robô iniciará em modo de degradação parcial.\n")
        else:
            print(f"[CONFIG]: Variáveis validadas com sucesso para o ambiente: [{self.APP_ENV.value.upper()}]")


# Instancia o objeto global de configurações (Singleton)
Config = Settings()

# Roda o check de sanidade inicial
Config.validate_critical_services()