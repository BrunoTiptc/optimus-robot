# Documento de Requisitos

Este documento reúne todos os requisitos essenciais e próximos passos do projeto Optimus Robot. Use esta lista para acompanhar o progresso e garantir que todas as etapas importantes sejam cumpridas.

## Requisitos Funcionais
- [ ] Descrever as funcionalidades principais do sistema
- [ ] Definir fluxos de usuário
- [ ] Especificar integrações necessárias
- [ ] Implementar a conexão do `brain-core` com o Redis
- [ ] Criar um serviço de eventos (ex: `event_service.py`) para publicar mensagens
- [ ] Testar a latência da comunicação Redis
- [ ] Implementar o `ai_service.py` (placeholder)
- [ ] Conectar com a API da OpenAI (chave no `.env.example`)
- [ ] Criar o `context_service.py` para análise de longo prazo do usuário

## Requisitos Não Funcionais
- [ ] Definir requisitos de desempenho
- [ ] Estabelecer padrões de segurança
- [ ] Documentar requisitos de usabilidade

## Critérios de Aceitação
- [ ] Listar critérios claros para cada requisito

## Preparação de Hardware (O Corpo Físico do Robô)
- [ ] Assim que o Arduino Ventuno Q chegar: criar a pasta `firmware/` para o código C++
- [ ] Integrar a Jetson Nano: preparar o módulo `ai-accelerator/` para processamento de borda pesado (40 TOPS)
- [ ] Configurar a Raspberry Pi como o Master (Orquestrador) físico distribuído

## Interface e Hospedeiro Virtual (O Espelho Mágico)
- [x] Conectar o holograma 3D ao back-end via WebSockets para sincronização de estados em tempo real
- [x] Adicionar o painel de telemetria e controle local das ações do Firestore
- [ ] Integrar síntese de voz (fala) com movimento síncrono da boca do robô 3D

## Observações
- [ ] Adicionar observações relevantes durante o desenvolvimento

brain-core/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── event_bus.py
│   │   ├── state.py
│   │   └── redis_client.py
│   │
│   ├── routes/
│   │   ├── health_routes.py
│   │   ├── chat_routes.py
│   │   └── robot_routes.py
│   │
│   ├── services/
│   │   ├── brain_service.py
│   │   ├── emotion_service.py
│   │   ├── memory_service.py
│   │   ├── speech_service.py
│   │   └── hologram_service.py
│   │
│   ├── websocket/
│   │   └── socket_manager.py
│   │
│   ├── models/
│   │   ├── chat_model.py
│   │   ├── emotion_model.py
│   │   └── robot_model.py
│   │
│   └── utils/
│       ├── logger.py
│       └── helpers.py
│
├── requirements.txt
├── Dockerfile
└── docker-compose.yml


**Dica:** Sempre que fizer uma grande mudança, dê um `git push` para não perder o progresso!
