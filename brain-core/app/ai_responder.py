# ai_responder.py

def generate_response(user_message: str) -> str:
    # Lógica inicial simples
    if user_message.lower() == "Oi":
        return "Olá, Bruno!"
    elif user_message.lower() == "tchau":
        return "Até mais, Bruno!"
    else:
        return f"Você disse: {user_message}"
