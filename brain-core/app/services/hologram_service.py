from app.websocket.socket_manager import manager

class HologramService:
    async def update_state(self, state: str, detail: str = None):
        """
        Updates the hologram state and broadcasts it to all connected WebSockets.
        Valid states: "idle", "processing", "success", "error"
        """
        valid_states = ["idle", "processing", "success", "error"]
        if state not in valid_states:
            raise ValueError(f"Invalid state: {state}. Must be one of {valid_states}")
        
        await manager.broadcast({
            "event": "state_change",
            "state": state,
            "detail": detail
        })

hologram_service = HologramService()
