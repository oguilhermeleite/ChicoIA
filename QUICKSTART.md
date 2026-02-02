# 🚀 Início Rápido - ChicoIA Telegram Bot

Guia de 5 minutos para colocar o bot no ar!

## ✅ Pré-requisitos

- Python 3.11+ instalado
- PostgreSQL instalado (ou use Docker)
- Token do Telegram Bot (já configurado: `8522357760:AAHn60ZJPYZ4rz4aO51k7O0GUPV8ivm7JCE`)
- Gemini API Key (já configurado: `AIzaSyCE0Bw-t0LsMacnxt-FjajyuHBzYiVNBaA`)

## 📦 Instalação Rápida

### Método 1: Script Automatizado (Windows)

```bash
# Abra o terminal na pasta do projeto
run.bat
```

### Método 2: Script Automatizado (Linux/Mac)

```bash
# Torne o script executável
chmod +x run.sh

# Execute
./run.sh
```

### Método 3: Manual

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar (Windows)
venv\Scripts\activate

# 2. Ativar (Linux/Mac)
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar banco de dados
# Edite o arquivo .env e configure a URL do PostgreSQL
# Exemplo: DATABASE_URL=postgresql://user:password@localhost:5432/chicobot

# 5. Executar bot
python bot/main.py
```

## 🗄️ Configurar PostgreSQL

### Opção A: PostgreSQL Local

```bash
# Windows - Baixe e instale:
# https://www.postgresql.org/download/windows/

# Linux
sudo apt-get install postgresql postgresql-contrib

# Mac
brew install postgresql

# Criar banco de dados
psql -U postgres
CREATE DATABASE chicobot;
CREATE USER chicouser WITH PASSWORD 'senha123';
GRANT ALL PRIVILEGES ON DATABASE chicobot TO chicouser;
\q
```

Atualize no `.env`:
```
DATABASE_URL=postgresql://chicouser:senha123@localhost:5432/chicobot
```

### Opção B: Docker (Mais Fácil!)

```bash
# Iniciar PostgreSQL + Bot
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

## ✅ Verificação

Após executar o bot, você deve ver:

```
2024-02-01 10:00:00 - INFO - Starting ChicoIA Telegram Bot...
2024-02-01 10:00:01 - INFO - Initializing database...
2024-02-01 10:00:01 - INFO - Database connection established
2024-02-01 10:00:01 - INFO - Database tables created successfully
2024-02-01 10:00:02 - INFO - Initializing Gemini AI service...
2024-02-01 10:00:02 - INFO - Gemini service initialized successfully
2024-02-01 10:00:03 - INFO - Bot started successfully! Press Ctrl+C to stop.
```

## 🧪 Testar o Bot

1. Abra o Telegram
2. Procure pelo seu bot (ou use o link do BotFather)
3. Envie `/start`
4. O bot deve responder com a mensagem de boas-vindas!

## 🎯 Comandos Básicos para Testar

```
/start - Ver mensagem de boas-vindas
/ajuda - Ver lista de comandos
/palpites - Ver sugestões do dia (teste o Gemini AI!)
/analisar Flamengo vs Palmeiras - Analisar jogo
```

## ❌ Problemas Comuns

### "Failed to connect to database"

```bash
# Verifique se PostgreSQL está rodando
# Windows
services.msc (procure por PostgreSQL)

# Linux
sudo systemctl status postgresql

# Mac
brew services list
```

### "Invalid bot token"

- Verifique o token no arquivo `.env`
- Certifique-se de não ter espaços extras
- O token correto já está configurado: `8522357760:AAHn60ZJPYZ4rz4aO51k7O0GUPV8ivm7JCE`

### "Module not found"

```bash
# Certifique-se de estar no ambiente virtual
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Reinstale as dependências
pip install -r requirements.txt
```

### Bot não responde

```bash
# Verifique os logs
tail -f chicobot.log

# Ou no Windows
type chicobot.log
```

## 📊 Próximos Passos

Depois que o bot estiver funcionando:

1. ✅ Teste todos os comandos
2. ✅ Configure o webhook (opcional, para produção)
3. ✅ Customize as mensagens em `bot/prompts.py`
4. ✅ Adicione usuários de teste
5. ✅ Configure monitoramento
6. ✅ Deploy em servidor de produção

## 🔧 Desenvolvimento

Para desenvolvimento, use o modo debug:

```python
# Em bot/main.py, adicione antes de application.run_polling():
logging.getLogger().setLevel(logging.DEBUG)
```

## 📚 Documentação Completa

Para informações detalhadas, consulte o [README.md](README.md) completo.

## 🆘 Suporte

- 📧 suporte@chicoia.com.br
- 💬 Telegram: @chicoia_suporte
- 🌐 https://chicoia.com.br

---

**Boa sorte! 🚀**
