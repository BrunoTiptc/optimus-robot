# redis_client.py
import json
from app.core.config import Config

# Tenta importar o pacote real do Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class DummyRedis:
    """Fallback seguro caso o Redis real não esteja rodando ou instalado"""
    def __init__(self):
        print("⚠️  [REDIS-FALLBACK]: Usando Mock interno (DummyRedis). Mensageria offline ativa.")
        self.storage = {}
        self.pubsub_channels = {}

    def get(self, key):
        return self.storage.get(key)

    def set(self, key, value, ex=None):
        self.storage[key] = value
        return True

    def publish(self, channel, message):
        # Apenas simula o log do evento rodando localmente
        # print(f"📢 [Dummy Pub/Sub] Canal '{channel}': {message[:60]}...")
        return 1 # Simula que 1 cliente ouviu

    def ping(self):
        return True


def initialize_redis():
    """Inicializa o cliente do Redis real ou cai no Dummy de contingência"""
    if not REDIS_AVAILABLE:
        return DummyRedis()

    try:
        # Puxa os dados validados do nosso config.py centralizado
        client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASSWORD,
            decode_responses=True, # Facilita pegando strings direto em vez de bytes
            socket_timeout=2.0     # Se o Redis real sumir, ele desiste em 2s e vai pro dummy
        )
        # Testa a conexão real disparando um ping
        client.ping()
        print(f"🧠 [REDIS]: Conectado com sucesso em {Config.REDIS_HOST}:{Config.REDIS_PORT}")
        return client
    except Exception as e:
        print(f"⚠️  [REDIS-ERRO]: Falha ao conectar no servidor Redis ({e}).")
        return DummyRedis()

# Instância global do cliente para o event_bus e services usarem
redis_client = initialize_redis()