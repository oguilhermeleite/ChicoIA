# 🤖 ChicoIA - Bot Telegram com IA Conversacional

Bot oficial do Telegram da plataforma ChicoIA de apostas esportivas, com inteligência artificial conversacional powered by Google Gemini.

## 📋 Sobre o Projeto

O Chico é um assistente virtual empático e estratégico que ajuda usuários a tomar decisões mais inteligentes em apostas esportivas através de:

- ✅ Análise detalhada de jogos e times
- ✅ Sugestões de mercados de apostas
- ✅ Orientações sobre gestão de banca
- ✅ Identificação de value bets
- ✅ Conversação natural em português

## 🚀 Tecnologias

- **Python 3.11+**
- **python-telegram-bot 20.8** - Framework para Telegram Bot API
- **Google Gemini API** - IA conversacional
- **PostgreSQL** - Banco de dados
- **SQLAlchemy** - ORM
- **Docker** - Containerização

## 📁 Estrutura do Projeto

```
chicobot-telegram/
├── bot/
│   ├── main.py              # Ponto de entrada do bot
│   ├── handlers.py          # Handlers de comandos e mensagens
│   ├── gemini_service.py    # Integração com Gemini API
│   ├── database.py          # Gerenciamento do banco de dados
│   ├── onboarding.py        # Fluxo de onboarding (7 dias)
│   └── prompts.py           # Prompts do sistema (personalidade do Chico)
├── models/
│   └── user.py              # Modelo de usuário
├── utils/
│   └── helpers.py           # Funções auxiliares
├── tests/
│   └── __init__.py          # Testes unitários
├── .env.example             # Exemplo de variáveis de ambiente
├── requirements.txt         # Dependências Python
├── Dockerfile               # Configuração Docker
├── docker-compose.yml       # Orquestração de containers
└── README.md                # Este arquivo
```

## ⚙️ Configuração e Instalação

### Pré-requisitos

- Python 3.11 ou superior
- PostgreSQL 12+
- Conta no Google Cloud (para Gemini API)
- Bot Token do Telegram

### 1. Criar Bot no Telegram

1. Abra o Telegram e procure por `@BotFather`
2. Envie `/newbot` e siga as instruções
3. Escolha um nome para o bot (ex: "ChicoIA Bot")
4. Escolha um username (ex: "chicoia_bot")
5. Copie o **Bot Token** fornecido (ex: `8522357760:AAHn60ZJPYZ4rz4aO51k7O0GUPV8ivm7JCE`)

### 2. Obter Gemini API Key

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a API Key gerada

### 3. Configurar PostgreSQL

**Opção A: PostgreSQL Local**

```bash
# Instalar PostgreSQL
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Criar banco de dados
sudo -u postgres psql
CREATE DATABASE chicobot;
CREATE USER chicouser WITH PASSWORD 'sua_senha_segura';
GRANT ALL PRIVILEGES ON DATABASE chicobot TO chicouser;
\q
```

**Opção B: PostgreSQL com Docker**

```bash
docker run --name chicobot-postgres \
  -e POSTGRES_DB=chicobot \
  -e POSTGRES_USER=chicouser \
  -e POSTGRES_PASSWORD=sua_senha_segura \
  -p 5432:5432 \
  -d postgres:15
```

### 4. Clonar e Configurar o Projeto

```bash
# Clonar o repositório (ou extrair os arquivos)
cd chicobot-telegram

# Criar ambiente virtual Python
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 5. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas credenciais
# Windows
notepad .env

# Linux/Mac
nano .env
```

**Configuração do .env:**

```env
# Token do seu bot do Telegram
TELEGRAM_BOT_TOKEN=8522357760:AAHn60ZJPYZ4rz4aO51k7O0GUPV8ivm7JCE

# API Key do Google Gemini
GEMINI_API_KEY=AIzaSyCE0Bw-t0LsMacnxt-FjajyuHBzYiVNBaA

# URL de conexão do PostgreSQL
DATABASE_URL=postgresql://chicouser:sua_senha_segura@localhost:5432/chicobot

# URL da plataforma ChicoIA
PLATFORM_URL=https://chicoia.com.br

# Ambiente (development ou production)
ENVIRONMENT=development
```

### 6. Executar o Bot

**Modo Desenvolvimento:**

```bash
# Com ambiente virtual ativado
python bot/main.py
```

**Com Docker:**

```bash
# Build e start
docker-compose up -d

# Ver logs
docker-compose logs -f chicobot

# Parar
docker-compose down
```

## 🎯 Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/start` | Iniciar conversa e onboarding |
| `/ajuda` | Ver comandos disponíveis |
| `/analisar [time1] vs [time2]` | Analisar jogo específico |
| `/palpites` | Ver sugestões de apostas do dia |
| `/meusdados` | Ver estatísticas e histórico |
| `/premium` | Conhecer ChicoIA Premium |

## 💬 Conversação Livre

O bot aceita conversação natural em português! Exemplos:

- "Quero analisar Flamengo x Palmeiras"
- "Como funciona over/under?"
- "Me dá dicas de gestão de banca"
- "Quais os melhores jogos de hoje?"

## 🔄 Fluxo de Onboarding

O bot implementa um onboarding de 7 dias:

- **Dia 1**: Boas-vindas + explicação das funcionalidades
- **Dia 2**: Convite para analisar jogos
- **Dia 3**: Compartilha caso de sucesso
- **Dia 4**: Ensina sobre mercados de apostas
- **Dia 5**: Explica gestão de banca
- **Dia 7**: Convite para Premium

## 🎁 Lead Magnet

Ao usar `/start`, o usuário recebe oferta de **alertas gratuitos de value bets**.

## 🗄️ Banco de Dados

### Tabelas

**telegram_users**
- `telegram_id` (PK) - ID do usuário no Telegram
- `username` - Username do Telegram
- `first_name` - Primeiro nome
- `joined_at` - Data de entrada
- `last_interaction` - Última interação
- `onboarding_day` - Dia do onboarding (1-7)
- `is_premium` - Se é usuário premium
- `opted_in_alerts` - Se aceitou alertas

**conversations**
- `id` (PK) - ID da conversa
- `telegram_id` (FK) - ID do usuário
- `role` - Papel ('user' ou 'assistant')
- `message` - Mensagem
- `created_at` - Data/hora

## 🧪 Testes

```bash
# Executar testes
pytest

# Com cobertura
pytest --cov=bot --cov-report=html
```

## 📦 Deploy em Produção

### Opção 1: VPS (DigitalOcean, Linode, AWS EC2)

```bash
# 1. Conectar ao servidor
ssh user@seu-servidor.com

# 2. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Clonar projeto
git clone seu-repositorio.git
cd chicobot-telegram

# 4. Configurar .env
nano .env

# 5. Executar com Docker Compose
docker-compose up -d

# 6. Configurar auto-start (opcional)
sudo nano /etc/systemd/system/chicobot.service
```

### Opção 2: Heroku

```bash
# 1. Login no Heroku
heroku login

# 2. Criar app
heroku create chicobot-telegram

# 3. Adicionar PostgreSQL
heroku addons:create heroku-postgresql:mini

# 4. Configurar variáveis
heroku config:set TELEGRAM_BOT_TOKEN=seu_token
heroku config:set GEMINI_API_KEY=sua_key

# 5. Deploy
git push heroku main
```

### Opção 3: Railway / Render

1. Conectar repositório GitHub
2. Configurar variáveis de ambiente
3. Deploy automático

## 🔧 Troubleshooting

### Erro: "Failed to connect to database"

```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Testar conexão
psql -U chicouser -d chicobot -h localhost
```

### Erro: "Invalid token"

- Verifique se o token no `.env` está correto
- Certifique-se de não ter espaços extras
- Gere um novo token com o @BotFather se necessário

### Erro: "Gemini API rate limit"

- A API Gemini tem limites de taxa gratuitos
- Considere upgrade para plano pago
- Implemente retry com backoff exponencial

### Bot não responde

```bash
# Ver logs
docker-compose logs -f chicobot

# Ou se rodando direto
tail -f chicobot.log
```

## 🔐 Segurança

- ✅ Nunca commite o arquivo `.env` (já está no `.gitignore`)
- ✅ Use senhas fortes para PostgreSQL
- ✅ Mantenha as dependências atualizadas
- ✅ Limite taxas de requisições por usuário
- ✅ Sanitize inputs do usuário

## 📊 Monitoramento

Para produção, considere:

- **Logs**: Configurar agregação de logs (Papertrail, Loggly)
- **Métricas**: Prometheus + Grafana
- **Alertas**: Configurar alertas para erros críticos
- **Uptime**: UptimeRobot ou similar

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é propriedade da ChicoIA.

## 👥 Suporte

Para dúvidas ou problemas:

- 📧 Email: suporte@chicoia.com.br
- 🌐 Site: https://chicoia.com.br
- 💬 Telegram: @chicoia_suporte

## 🎯 Roadmap

- [ ] Integração com APIs de estatísticas esportivas
- [ ] Sistema de análise preditiva com ML
- [ ] Dashboard analytics para admins
- [ ] Suporte a múltiplos idiomas
- [ ] Integração com plataformas de apostas
- [ ] Sistema de rankings e badges

---

**Desenvolvido com ❤️ para a comunidade de apostas esportivas brasileira**
