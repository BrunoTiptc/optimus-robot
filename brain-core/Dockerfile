FROM python:3.11-slim

# Evita arquivos .pyc e garante logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. Cria usuário de sistema (Segurança: Princípio do Menor Privilégio)
RUN adduser --disabled-password --gecos '' optimus_user

WORKDIR /app

# 2. Instala dependências como root (aproveitando o cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia o código e já define o dono como o usuário restrito
COPY --chown=optimus_user:optimus_user app ./app

# 4. Muda para o usuário sem privilégios antes de rodar
USER optimus_user

# Documenta a porta interna
EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
