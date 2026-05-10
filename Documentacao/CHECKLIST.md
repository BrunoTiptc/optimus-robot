# ✅ Checklist Próximos Passos - Optimus Robot

Quando você voltar descansado, aqui está o que falta para o Optimus ganhar corpo:

### 1️⃣ Fase 2 - Mensageria (Prioridade)
- [ ] Implementar a conexão do `brain-core` com o Redis.
- [ ] Criar um serviço de eventos (ex: `event_service.py`) para publicar mensagens.
- [ ] Testar a latência da comunicação Redis.

### 2️⃣ Preparação de Hardware (O Futuro)
- [ ] Assim que o **Arduino Ventuno** chegar: criar a pasta `firmware/` para o código C++.
- [ ] Integrar a **Jetson Nano**: preparar o módulo `ai-accelerator/` para processamento pesado (40 TOPS).
- [ ] Configurar a **Raspberry Pi** como o Master (Orquestrador) físico.

### 3️⃣ Expansão da Inteligência
- [ ] Implementar o `ai_service.py` (que deixamos o placeholder).
- [ ] Conectar com a API da OpenAI (já temos a chave no `.env.example`).
- [ ] Criar o `context_service.py` para análise de longo prazo do usuário.

### 4️⃣ Interface de Controle
- [ ] Iniciar a pasta `control-panel/` (Node.js) para monitorar o robô via web ou mobile.

---
**Dica de mestre:** Sempre que fizer uma grande mudança, dê um `git push` para não perdermos o progresso se o VS Code "resolver dar trabalho" de novo! 😉
