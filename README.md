# 🤖 Optimus Robot

**Sistema Robótico Distribuído com IA, Mensageria Assíncrona e QA de Nível Profissional**

O **Optimus Robot** é um projeto de arquitetura de sistemas reais, combinando IA, Edge Computing, Sistemas Distribuídos e DevOps. O projeto foi estruturado para refletir cenários de produção que exigem alta resiliência e escalabilidade.

---

## 📚 Fundamentação Teórica

O desenvolvimento deste sistema é pautado pelos pilares da Engenharia de Software moderna:

* **Engenharia de Software Evolucionária (Roger Pressman):** A arquitetura foi desenhada para permitir o crescimento incremental. O uso de containers e mensageria garante que o sistema evolua organicamente de um protótipo inicial para uma infraestrutura complexa sem comprometer o núcleo do sistema.
* **Sistemas Sócio-Técnicos (Ian Sommerville):** O projeto considera a integração entre hardware, software e o contexto de operação real. A estrutura Master-Worker reflete a necessidade de um sistema que seja resiliente a falhas parciais, mantendo a operação contínua mesmo sob condições adversas.

---

## 🧠 Visão Geral da Arquitetura

O sistema utiliza um padrão **Master–Worker / Orquestrador + Edge**:

* **Master (Raspberry Pi):** Responsável pela tomada de decisão de alto nível (IA).
* **Edge (Jetson Nano):** Processamento de visão computacional e eventos em tempo real.
* **Mensageria:** Comunicação desacoplada e assíncrona.

---

## 🧩 Estrutura do Repositório (Atualizada)

A organização atual reflete a separação de responsabilidades para facilitar a manutenção e o QA:

```text
optimus-robot/
├── brain-core/            # IA e tomada de decisão (Python/FastAPI)
│   ├── app/               # Lógica interna (main.py, api.py)
│   ├── Dockerfile         # Containerização do cérebro
│   └── requirements.txt   # Dependências Python
├── control-panel/         # Interface e orquestração (Node.js) - [Em breve]
├── contracts/             # Definição de mensagens entre serviços
├── docker-compose.yml     # Orquestração do ambiente completo
├── .env.example           # Configurações de ambiente
└── README.md              # Documentação técnica



 Roadmap de Desenvolvimento
​[x] Fase 1 - Foundation: Estrutura base com FastAPI e Docker.
​[ ] Fase 2 - Mensageria: Integração com Redis para eventos assíncronos.
​[ ] Fase 3 - QAOps: Implementação de testes de resiliência com Cypress.
​[ ] Fase 4 - Edge Integration: Conexão com módulos de visão computacional.
​📊 Diferencial de Engenharia
​Este projeto demonstra competências em:
​Arquitetura orientada a eventos.
​Containerização de microserviços.
​Garantia de qualidade profissional aplicada a sistemas complexos.
​<!-- end list -->





















