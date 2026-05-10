from google.cloud import firestore
from app.models.user_memory import UserMemory
from app.models.conversation import ConversationMemory

db = firestore.Client()

def save_user(memory: UserMemory):
    db.collection("users").document(memory.userId).set(memory.dict())

def save_conversation(memory: ConversationMemory):
    db.collection("conversations").document(memory.timestamp.isoformat()).set(memory.dict())

def get_context(userId: str):
    user = db.collection("users").document(userId).get().to_dict()
    conversations = db.collection("conversations").where("userId", "==", userId).stream()
    conv_list = [c.to_dict() for c in conversations]
    return {"user": user, "conversations": conv_list}
