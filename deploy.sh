#!/bin/bash
# ChicoIA Telegram Bot - Production Deployment Script

set -e

echo "================================"
echo "ChicoIA Bot - Production Deploy"
echo "================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/opt/chicobot-telegram"
APP_USER="chicobot"
LOG_DIR="/var/log/chicobot"
SYSTEMD_SERVICE="/etc/systemd/system/chicobot.service"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Por favor, execute como root ou com sudo${NC}"
    exit 1
fi

echo -e "${YELLOW}1. Criando usuário do sistema...${NC}"
if ! id "$APP_USER" &>/dev/null; then
    useradd -r -s /bin/false $APP_USER
    echo -e "${GREEN}✓ Usuário criado${NC}"
else
    echo -e "${GREEN}✓ Usuário já existe${NC}"
fi

echo -e "${YELLOW}2. Criando diretórios...${NC}"
mkdir -p $APP_DIR
mkdir -p $LOG_DIR
chown -R $APP_USER:$APP_USER $LOG_DIR
echo -e "${GREEN}✓ Diretórios criados${NC}"

echo -e "${YELLOW}3. Copiando arquivos...${NC}"
cp -r . $APP_DIR/
chown -R $APP_USER:$APP_USER $APP_DIR
echo -e "${GREEN}✓ Arquivos copiados${NC}"

echo -e "${YELLOW}4. Instalando dependências...${NC}"
cd $APP_DIR
sudo -u $APP_USER python3 -m venv venv
sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r requirements.txt
echo -e "${GREEN}✓ Dependências instaladas${NC}"

echo -e "${YELLOW}5. Configurando .env...${NC}"
if [ ! -f "$APP_DIR/.env" ]; then
    echo -e "${RED}ATENÇÃO: Arquivo .env não encontrado!${NC}"
    echo -e "${YELLOW}Por favor, crie $APP_DIR/.env com as configurações necessárias${NC}"
    echo "Pressione Enter para continuar..."
    read
else
    echo -e "${GREEN}✓ Arquivo .env encontrado${NC}"
fi

echo -e "${YELLOW}6. Instalando serviço systemd...${NC}"
cp chicobot.service $SYSTEMD_SERVICE
systemctl daemon-reload
echo -e "${GREEN}✓ Serviço instalado${NC}"

echo -e "${YELLOW}7. Inicializando banco de dados...${NC}"
sudo -u $APP_USER $APP_DIR/venv/bin/python -c "
from bot.database import DatabaseManager
import os
from dotenv import load_dotenv

load_dotenv('$APP_DIR/.env')
db = DatabaseManager(os.getenv('DATABASE_URL'))
db.init_db()
print('Banco de dados inicializado!')
"
echo -e "${GREEN}✓ Banco de dados inicializado${NC}"

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Deploy concluído com sucesso!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Para gerenciar o bot, use:"
echo ""
echo "  Iniciar:    sudo systemctl start chicobot"
echo "  Parar:      sudo systemctl stop chicobot"
echo "  Reiniciar:  sudo systemctl restart chicobot"
echo "  Status:     sudo systemctl status chicobot"
echo "  Logs:       sudo journalctl -u chicobot -f"
echo "  Auto-start: sudo systemctl enable chicobot"
echo ""
echo -e "${YELLOW}Deseja iniciar o bot agora? (s/n)${NC}"
read -r response
if [[ "$response" =~ ^[Ss]$ ]]; then
    systemctl start chicobot
    systemctl enable chicobot
    echo ""
    echo -e "${GREEN}✓ Bot iniciado e configurado para auto-start${NC}"
    echo ""
    echo "Verificando status..."
    sleep 2
    systemctl status chicobot --no-pager
fi

echo ""
echo -e "${GREEN}Deploy finalizado!${NC}"
