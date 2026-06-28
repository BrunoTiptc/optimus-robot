# 🤖 Optimus Robot: Das Engrenagens às Nuvens

### Sistema Robótico Distribuído com IA, Edge Computing e Presença Holográfica

O **Optimus Robot** evoluiu de um conceito clássico de robótica física para um ecossistema de arquitetura de sistemas reais. Ele combina Inteligência Artificial, Edge Computing e Sistemas Distribuídos com uma interface holográfica de alta fidelidade visual, projetada para simular ambientes de produção que exigem resiliência, desacoplamento e escalabilidade.

> 💡 *"A presença não depende totalmente da matéria."* — O projeto documenta a transição de motores e rodas para uma presença de luz e lógica persistente.

---

## 📚 Fundamentação Teórica

*   **Engenharia de Software Evolucionária (Roger Pressman):** A arquitetura permite crescimento incremental, evoluindo de um protótipo físico simples para um sistema distribuído completo sem comprometer a base tecnológica.
*   **Sistemas Sócio-Técnicos (Ian Sommerville):** Integra hardware, software e o contexto operacional. Considera falhas de sensores, latência de rede e a comunicação duplex entre múltiplos dispositivos físicos.

---

## 🧠 Visão Geral da Arquitetura

O sistema adota o padrão **Master–Worker / Orquestrador + Edge + Firmware Layer**.

### 🔹 Componentes Principais

1.  **Master (Raspberry Pi - *brain-core*):** Orquestração central desenvolvida em FastAPI, gerenciando regras de negócio, memória de longo prazo no Firestore (Firebase) e decisões de IA.
2.  **AI Accelerator (40 TOPS):** Módulo dedicado para visão computacional, reconhecimento de voz e inferência de modelos de linguagem (OpenAI / LangChain) em tempo real.
3.  **Arduino (Firmware Layer):** Controle físico de baixo nível para sensores, motores e leitura de ambiente.
4.  **Mensageria Assíncrona (Redis):** Barramento de eventos que garante comunicação desacoplada e de sub-milissegundo entre o cérebro e os demais módulos.
5.  **Interface Holográfica (HologramOptimus):** Front-end em Three.js que renderiza a face do robô em tempo real, reagindo a estados via WebSockets.

### 🔄 Fluxo de Dados Integrado

*   **Captura:** Sensores físicos capturam dados do ambiente através do Arduino.
*   **Processamento:** O Arduino envia eventos para o Master (Raspberry Pi/FastAPI).
*   **Inteligência:** O Master processa o contexto (buscando memórias estruturadas no Firestore) e consulta o módulo de IA para tomada de decisões.
*   **Feedback Visual:** O *brain-core* publica o estado no Redis, que é transmitido via WebSocket para o holograma 3D alterar sua animação e cor instantaneamente.
*   **Ação Física:** O Master envia comandos de volta ao Arduino para execução no ambiente real.

---

## 🧩 Estrutura do Repositório

```text
optimus-robot/
├── brain-core/            # IA, Memória e API Central (Python/FastAPI) [10]
│   ├── app/               # Lógica de rotas, services e core [10]
│   ├── tests/             # Suíte de testes (Pytest + HTTPX) [11, 12]
│   ├── Dockerfile         # Conteinerização do cérebro [10]
│   └── requirements.txt   # Dependências (FastAPI, Redis, LangChain) [10, 13]
├── firmware/              # Código embarcado (Arduino/C++) [Query]
├── ai-accelerator/        # Integração com hardware de IA (40 TOPS) [Query]
├── control-panel/         # Interface de telemetria (Node.js) - [Em breve] [Query]
├── contracts/             # Definição de esquemas de mensagens JSON [Query, 134]
├── docker-compose.yml     # Orquestração do ecossistema (FastAPI + Redis) [2, 14]
├── .env.example           # Template de chaves (OpenAI, Firebase) [15, 16]
└── README.md
🧪 Estratégia de QA e Automação
O projeto utiliza uma pirâmide de testes para garantir a resiliência do sistema distribuído:
Testes de Unidade e Integração: Implementados com Pytest, validando WebSockets, serviços de IA e integridade da memória no Firestore
.
Gestão de Testes (Qase.io): Casos de teste mapeados para validar o ciclo de boot (1.8s), resiliência a erros e sincronia labial do holograma
.
Automação E2E (Playwright): Validação visual da interface 3D, garantindo que os shaders e cores reflitam o estado real do back-end
.
🚀 Como Executar
Pré-requisitos: Python 3.11 ou superior, Redis (localhost:6379) ou Docker, e opcionalmente FIRESTORE remoto com optimus-key.json.

1) Use o launcher Windows (recomendado):
   - Abra PowerShell
   - Navegue até `optimus-robot\brain-core`
   - Execute: `.\start.bat`

   O `start.bat` faz:
   - criação/ativação do `.venv`
   - inicialização do servidor FastAPI
   - definição automática de `GOOGLE_APPLICATION_CREDENTIALS`
     quando `brain-core\optimus-key.json` estiver presente

2) Ou rode manualmente:
   - Navegue até `optimus-robot\brain-core`
   - Crie e ative o venv:
     - `python -m venv .venv`
     - `.\.venv\Scripts\Activate.ps1`
   - Instale dependências:
     - `python -m pip install --upgrade pip`
     - `python -m pip install -r requirements.txt`
   - Defina variáveis de ambiente no PowerShell:
     - `$env:REDIS_URL='redis://localhost:6379'`
     - `$env:OPENAI_API_KEY='sua_chave_aqui'`  # opcional
     - `$env:GOOGLE_APPLICATION_CREDENTIALS='C:\Users\Bruno PC\Desktop\Materias\Programacao\🤖 Optimus Robot\optimus-robot\brain-core\optimus-key.json'`
   - Inicie o servidor:
     - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

Acesso: O backend ficará disponível em `http://localhost:8000` e a documentação Swagger em `/docs`.

Observação: se o `optimus-key.json` não estiver configurado, o servidor ainda iniciará em modo local/fallback, mas o Firestore remoto não funcionará.

Este projeto é o QG de estudos de Bruno, conectando a paixão pela robótica com a excelência em Engenharia de Software e QA.