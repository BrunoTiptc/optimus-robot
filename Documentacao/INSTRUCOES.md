## Instruções Gerais

Este documento reúne todas as instruções necessárias para o uso, desenvolvimento e manutenção do projeto Optimus Robot, de forma clara e sem emojis.

### Como rodar o Optimus Robot
1. Abra o Docker Desktop e aguarde até que esteja rodando.
2. Abra a pasta `optimus-robot` no VS Code.
3. Verifique se o arquivo `brain-core/optimus-key.json` (chave do Firebase) está presente.
4. No terminal do VS Code, execute:
	```bash
	docker compose up -d
	```
5. Para acessar a interface de testes (Swagger), abra o navegador em: http://localhost:8000/docs

### Como usar o sistema
1. Siga o guia de instalação no README.
2. Execute o ambiente conforme descrito no docker-compose.
3. Utilize a API conforme a documentação técnica.

### Como contribuir
- Faça um fork do repositório.
- Crie uma branch para sua feature ou correção.
- Envie um pull request detalhando as mudanças.

### Dicas e Boas Práticas
- Mantenha o código limpo e documentado.
- Sempre atualize este documento ao adicionar novas funcionalidades.

### Testar o Fluxo
1. Inicie todos os containers com `docker-compose up`.
2. Acesse a API na porta configurada.
3. Realize requisições de teste conforme exemplos na documentação.

### Atualizar Dependências
1. Acesse a pasta do serviço desejado.
2. Execute o comando de atualização de dependências (ex: `pip install -r requirements.txt`).

### Backup de Dados
1. Identifique os arquivos de dados importantes.
2. Realize cópias de segurança periodicamente.

### Contato
Em caso de dúvidas, entre em contato com o responsável pelo projeto.
