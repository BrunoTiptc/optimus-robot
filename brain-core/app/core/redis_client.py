import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

class DummyRedis:
    """
    Mock do Redis para desenvolvimento local offline,
    garantindo que o sistema não trave se o Redis não estiver ativo.
    """
    def ping(self):
        return False
    def publish(self, channel, message):
        print(f"[MOCK-REDIS] Publicando no canal {channel}: {message}")
        return 0

try:
    # Tenta conectar ao Redis físico
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, socket_connect_timeout=2)
    # Testa se o Redis está respondendo
    redis_client.ping()
    redis_available = True
    print(f"[REDIS] Conectado com sucesso ao Redis em {REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    redis_client = DummyRedis()
    redis_available = False
    print(f"[REDIS-ALERTA] Redis indisponível ({e}). Usando MockRedis para estabilidade.")
