# 🤖 Optimus Robot

> **Sistema Robótico Distribuído com IA, Mensageria Assíncrona e QA de Nível Profissional**

O **Optimus Robot** é um projeto âncora de portfólio focado em **Arquitetura de Sistemas Reais**, combinando **IA**, **Edge Computing**, **Sistemas Distribuídos**, **DevOps** e **Qualidade de Software**.

Este projeto não é um protótipo simples. Ele foi pensado para refletir **cenários reais de produção**, similares aos exigidos por empresas que pedem experiência com **Sistemas Assíncronos, Mensageria, Observabilidade, QA e Infraestrutura**.

---

## 🎯 Objetivo do Projeto

Construir um **Agente Robótico Distribuído**, onde:

* Um nó central (Raspberry Pi) toma decisões inteligentes
* Um nó de borda (Jetson Nano) processa visão computacional
* A comunicação ocorre de forma **assíncrona e resiliente**
* Toda a arquitetura é **testável, observável e containerizada**

---

## 🧠 Visão Geral da Arquitetura

**Padrão:** Master–Worker / Orquestrador + Edge

### Componentes principais:

* **Raspberry Pi (Master / Orquestrador)**

  * IA de alto nível (LangChain / LangGraph)
  * API de controle (Node.js)
  * Mensageria (Redis)
  * Observabilidade

* **Jetson Nano (Worker / Edge)**

  * Visão computacional
  * Processamento de eventos visuais
  * Envio de eventos assíncronos

* **Comunicação**

  * Arquitetura orientada a eventos
  * Mensagens desacopladas via Redis

---

## 🧩 Tecnologias Utilizadas

### IA & Backend

* Python
* LangChain / LangGraph
* FastAPI
* Ollama (opcional / LLM local)

### Controle & QA

* Node.js
* Cypress (automação e testes de sistema)

### Infraestrutura & DevOps

* Docker
* Docker Compose
* Redis (mensageria assíncrona)

### Hardware

* Raspberry Pi 4/5
* NVIDIA Jetson Nano

---

## 📁 Estrutura do Repositório

```
optimus-robot/
├── brain-core/            # IA e tomada de decisão (Python)
│   ├── main.py
│   ├── api.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── control-panel/         # Interface e orquestração (Node.js)
│   ├── src/
│   │   └── server.js
│   ├── cypress/           # Testes automatizados (QA)
│   ├── package.json
│   └── Dockerfile
│
├── contracts/             # Contratos de mensagens (event-driven)
│   └── vision-event.json
│
├── docker-compose.yml     # Orquestração dos serviços
├── .env                   # Variáveis de ambiente
└── README.md
```

---

## 🔄 Arquitetura Orientada a Eventos

O sistema utiliza **mensageria assíncrona** para evitar acoplamento direto entre serviços.

### Exemplo de evento:

```json
{
  "source": "jetson",
  "type": "vision_event",
  "payload": {
    "object": "person",
    "distance": 2.1
  }
}
```

Essa abordagem permite:

* Escalabilidade
* Resiliência
* Substituição futura do Redis por Kafka ou SQS sem mudança conceitual

---

## 🧪 Qualidade de Software (QA)

O projeto aplica QA **além da interface gráfica**:

* Testes de fluxo completo (end-to-end)
* Testes de falha (Redis indisponível, serviços fora do ar)
* Validação de contratos de mensagens
* Testes de resiliência do sistema

Ferramenta principal: **Cypress**

---

## 📊 Observabilidade

* Registro de decisões do agente (LangSmith)
* Logs estruturados por evento
* Rastreabilidade de ações do robô

Cada decisão do Optimus é **auditável**.

---

## 🚀 Roadmap (Feature-Based, estilo empresa)

### 🔹 Fase 1 – Foundation (Core)

* [ ] Brain-core com FastAPI + LangChain
* [ ] Redis como fila assíncrona
* [ ] Docker Compose funcional

### 🔹 Fase 2 – Controle & QA

* [ ] API Node.js de controle
* [ ] Dashboard simples
* [ ] Testes Cypress de fluxo

### 🔹 Fase 3 – Edge Computing

* [ ] Jetson Nano processando visão
* [ ] Envio de eventos visuais
* [ ] Integração com Brain-core

### 🔹 Fase 4 – Resiliência & Observabilidade

* [ ] Testes de falha
* [ ] Logs estruturados
* [ ] Monitoramento de decisões

### 🔹 Fase 5 – Evolução (Futuro)

* [ ] Substituição Redis → Kafka/SQS
* [ ] Migração para Kubernetes
* [ ] Expansão para múltiplos workers

---

## 🧠 Diferencial Profissional

Este projeto demonstra experiência prática em:

* Sistemas Distribuídos
* Arquitetura Orientada a Eventos
* IA aplicada a hardware real
* DevOps e Infraestrutura
* QA de sistemas complexos

> **Optimus Robot não é um chatbot. É um sistema inteligente real.**

---

## 📌 Status do Projeto

🚧 Em desenvolvimento ativo – 2026

---
