# Plano de Implementação: Cérebro IA, Inspetor Watson & Mensageria Redis (Fase 3)

Este plano detalha a implementação das opções 1, 2 e 3 aprovadas pelo operador, elevando o **Optimus Robot** a um patamar profissional de inteligência artificial de borda e arquitetura distribuída.

---

## 🚀 Escopo das Funcionalidades

### 1. 🧠 Cérebro Inteligente (`ai_service.py`)
* **Híbrido e Resiliente**: O cérebro será integrado à API da OpenAI (LangChain). Se nenhuma chave válida estiver configurada (`your_key_here`), o sistema automaticamente assumirá o **Motor NLP Local Watson**, permitindo o funcionamento inteligente completo offline.
* ** Watson Slot-Filling**: Se o usuário disser *"Meu nome é Bruno"*, o cérebro identificará o nome, atualizará as variáveis de contexto da sessão no Firestore e falará de volta usando o nome do usuário.

### 2. 📺 Inspetor Visual de Memória (Holograma UI)
* **Firestore Live Dashboard**: Adição de uma área premium translúcida no painel lateral esquerdo exibindo o estado interno da memória Watson em tempo real:
  - `Nome do Operador`
  - `Intenção Atual`
  - `Fila de Comandos Recentes`
  - `Contagem de Turnos`
* **Botão "Consolidar Memória"**: Permite disparar a compactação da sessão, gerando um resumo na coleção `summaries`, limpando o lixo da sessão do Firestore e atualizando a coleção `users`.

### 3. 🔄 Barramento de Eventos Redis (`event_bus.py`)
* **Mensageria Pronta para Hardware**: Configuração do cliente do Redis e do barramento de eventos (`event_bus.py`) para publicação de mensagens em segundo plano.
* **Inicialização Robusta**: Se o Redis não estiver rodando no host local (ex: durante testes rápidos fora do Docker), o sistema capturará a falha graciosamente e rodará em modo *"Local Event Bus"*, garantindo zero travamentos.

---

## 🛠️ Detalhes da Execução

### Arquivos Novos a Criar:
1. `brain-core/app/services/ai_service.py` -> Gerenciador de Inteligência Artificial e NLP Watson local.
2. `brain-core/app/core/redis_client.py` -> Cliente de conexão ao Redis.
3. `brain-core/app/core/event_bus.py` -> Publicador de eventos assíncronos.

### Arquivos a Modificar:
1. `HologramOptimus/index.html` -> Interface com Inspetor Watson visual e comandos de IA integrados.
2. `brain-core/app/routes/robot_routes.py` -> Adicionar endpoints para bate-papo com IA (`POST /robot/chat`) e consolidação de sessão (`POST /robot/session/consolidate`).
3. `brain-core/app/main.py` -> Inicializar e fechar as conexões do Redis graciosamente na inicialização do FastAPI.
