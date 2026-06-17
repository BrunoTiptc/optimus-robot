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
├── brain-core/            # IA, Memória e API Central (Python/FastAPI)
│   ├── app/               # Lógica de rotas, services e core
│   ├── tests/             # Suíte de testes (Pytest + HTTPX)
│   ├── Dockerfile         # Conteinerização do cérebro
│   └── requirements.txt   # Dependências (FastAPI, Redis, LangChain)
├── firmware/              # Código embarcado (Arduino/C++)
├── ai-accelerator/        # Integração com hardware de IA (40 TOPS)
├── control-panel/         # Interface de telemetria (Node.js) - [Em breve]
├── contracts/             # Definição de esquemas de mensagens JSON
├── docker-compose.yml     # Orquestração do ecossistema (FastAPI + Redis)
├── .env.example           # Template de chaves de ambiente (OpenAI, Firebase)
└── README.md              # Documentação do projeto
