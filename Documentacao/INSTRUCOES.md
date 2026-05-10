# 🚀 Como Rodar o Optimus Robot

Siga esta ordem sempre que abrir o projeto para garantir que tudo funcione!

### 1️⃣ Ligar o Motor (Docker)
- Abra o **Docker Desktop**.
- Espere até que a barra inferior fique **verde** (Running).

### 2️⃣ Preparar o Ambiente (VS Code)
- Abra a pasta `optimus-robot` no VS Code.
- Verifique se o arquivo `brain-core/optimus-key.json` (sua chave do Firebase) está lá.

### 3️⃣ Subir o Sistema
No terminal do VS Code, digite:
```bash
docker compose up -d

### 🌐 Interface Visual (Swagger)
O Optimus roda "escondido" no Docker, então para ver a interface de testes:
- Abra o Chrome em: http://localhost:8000/docs
- Aqui você pode testar todos os comandos visualmente!
