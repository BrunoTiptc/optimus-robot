import json
from datetime import datetime

from app.core.redis_client import redis_client


class EventBus:
    """Barramento de eventos assíncronos para integração interna do Optimus."""

    @staticmethod
    def publish_event(channel: str, event_type: str, data: dict):
        payload = {
            "eventType": event_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": data,
        }

        try:
            message = json.dumps(payload)
            redis_client.publish(channel, message)
            print(f"[EVENT_BUS] published event '{event_type}' on '{channel}'")
        except Exception as exc:
            print(f"[EVENT_BUS] failed to publish event: {exc}")


event_bus = EventBus()
