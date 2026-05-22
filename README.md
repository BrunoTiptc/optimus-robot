# 🤖 Optimus Robot

## Sistema Robótico Distribuído com IA, Edge Computing e Controle Físico em Tempo Real

O **Optimus Robot** é um projeto de arquitetura de sistemas reais, combinando Inteligência Artificial, Edge Computing, Sistemas Distribuídos e integração com hardware embarcado.  
O sistema é projetado para simular ambientes de produção que exigem alta resiliência, desacoplamento e escalabilidade.

---

## 📚 Fundamentação Teórica

- **Engenharia de Software Evolucionária (Roger Pressman):**  
  Arquitetura permite crescimento incremental, evoluindo de protótipo simples para sistema distribuído completo sem comprometer a base.

- **Sistemas Sócio-Técnicos (Ian Sommerville):**  
  Integra hardware, software e contexto operacional real. Considera falhas, latência e comunicação entre múltiplos dispositivos físicos.

---

## 🧠 Visão Geral da Arquitetura

**Padrão:** Master–Worker / Orquestrador + Edge + Firmware Layer

### 🔹 Componentes principais
- 🧠 **Master (Raspberry Pi):** Orquestração, regras de negócio e decisões de alto nível.  
- 🚀 **AI Accelerator (40 TOPS):** Modelos de IA para visão computacional, reconhecimento de voz e inferência em tempo real.  
- ⚙️ **Arduino (Firmware Layer):** Controle físico (sensores, motores, atuadores, leitura de ambiente).  
- 🔗 **Mensageria Assíncrona (Redis / MQTT - futuro):** Comunicação desacoplada entre módulos.  

---

## 🔄 Fluxo de Dados (Alto Nível)

1. Sensores capturam dados via Arduino  
2. Arduino envia eventos para o Master (Raspberry Pi)  
3. Master processa ou encaminha para o módulo de IA  
4. Módulo de IA retorna decisão  
5. Master envia comandos de volta ao Arduino  
6. Arduino executa ações físicas no ambiente  

---

## 🧩 Estrutura do Repositório

```plaintext
optimus-robot/
├── brain-core/            # IA e tomada de decisão (Python/FastAPI)
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── firmware/              # Código embarcado (Arduino/C++)
├── ai-accelerator/        # Integração com módulo de IA (40 TOPS)
├── control-panel/         # Interface e monitoramento (Node.js) - [Em breve]
├── contracts/             # Definição de eventos/mensagens
├── docker-compose.yml
├── .env.example
└── README.md
