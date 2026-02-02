#!/usr/bin/env python
"""
ChicoIA Telegram Bot - Setup Verification Script
Verifica se todas as dependências e configurações estão corretas
"""

import sys
import os
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def check_python_version():
    """Check Python version"""
    print_header("Verificando versão do Python")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version_str} (OK)")
        return True
    else:
        print_error(f"Python {version_str} (Requer 3.11+)")
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    print_header("Verificando dependências Python")

    required_packages = {
        'telegram': 'python-telegram-bot',
        'google.generativeai': 'google-generativeai',
        'sqlalchemy': 'sqlalchemy',
        'psycopg2': 'psycopg2-binary',
        'dotenv': 'python-dotenv',
        'aiohttp': 'aiohttp',
    }

    all_installed = True

    for module, package in required_packages.items():
        try:
            __import__(module)
            print_success(f"{package}")
        except ImportError:
            print_error(f"{package} - NÃO INSTALADO")
            all_installed = False

    if not all_installed:
        print_warning("\nInstale as dependências com: pip install -r requirements.txt")

    return all_installed


def check_env_file():
    """Check if .env file exists and has required variables"""
    print_header("Verificando arquivo .env")

    env_path = Path('.env')

    if not env_path.exists():
        print_error(".env não encontrado")
        print_warning("Copie .env.example para .env e configure suas credenciais")
        return False

    print_success(".env encontrado")

    # Check required variables
    required_vars = {
        'TELEGRAM_BOT_TOKEN': 'Token do Bot Telegram',
        'GEMINI_API_KEY': 'API Key do Google Gemini',
        'DATABASE_URL': 'URL do PostgreSQL',
    }

    all_configured = True

    try:
        from dotenv import dotenv_values
        env_vars = dotenv_values('.env')

        print("\nVariáveis de ambiente:")

        for var, description in required_vars.items():
            value = env_vars.get(var, '')

            if not value or 'your_' in value or 'password' in value.lower():
                print_error(f"{var} - NÃO CONFIGURADO ({description})")
                all_configured = False
            else:
                # Mask sensitive values
                if len(value) > 20:
                    masked = value[:10] + '...' + value[-10:]
                else:
                    masked = value[:5] + '...'
                print_success(f"{var} - Configurado ({masked})")

    except Exception as e:
        print_error(f"Erro ao ler .env: {e}")
        all_configured = False

    return all_configured


def check_database_connection():
    """Check if can connect to PostgreSQL"""
    print_header("Verificando conexão com PostgreSQL")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        database_url = os.getenv('DATABASE_URL')

        if not database_url or 'your_' in database_url:
            print_error("DATABASE_URL não configurado corretamente")
            print_warning("Configure o PostgreSQL e atualize DATABASE_URL no .env")
            return False

        # Try to import psycopg2
        import psycopg2

        # Try to connect
        try:
            # Parse URL
            if database_url.startswith('postgresql://'):
                from sqlalchemy import create_engine
                engine = create_engine(database_url)

                with engine.connect() as conn:
                    print_success("Conexão com PostgreSQL estabelecida")
                    return True
            else:
                print_error("URL do PostgreSQL inválida")
                return False

        except Exception as e:
            print_error(f"Não foi possível conectar ao PostgreSQL: {e}")
            print_warning("Certifique-se de que o PostgreSQL está rodando")
            print_warning("Ou use: docker-compose up -d postgres")
            return False

    except ImportError:
        print_error("psycopg2 não instalado")
        return False
    except Exception as e:
        print_error(f"Erro: {e}")
        return False


def check_telegram_token():
    """Verify Telegram bot token format"""
    print_header("Verificando Token do Telegram")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        token = os.getenv('TELEGRAM_BOT_TOKEN')

        if not token or 'your_' in token:
            print_error("Token não configurado")
            return False

        # Basic token format check (should be like: 123456:ABC-DEF...)
        if ':' in token and len(token) > 40:
            print_success(f"Token formato válido ({token[:20]}...)")
            return True
        else:
            print_error("Token formato inválido")
            return False

    except Exception as e:
        print_error(f"Erro: {e}")
        return False


def check_project_structure():
    """Check if all required files exist"""
    print_header("Verificando estrutura do projeto")

    required_files = [
        'bot/main.py',
        'bot/handlers.py',
        'bot/gemini_service.py',
        'bot/database.py',
        'bot/onboarding.py',
        'bot/prompts.py',
        'models/user.py',
        'utils/helpers.py',
        'requirements.txt',
    ]

    all_exist = True

    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print_success(file_path)
        else:
            print_error(f"{file_path} - NÃO ENCONTRADO")
            all_exist = False

    return all_exist


def main():
    """Main verification function"""
    print(f"\n{Colors.BOLD}ChicoIA Telegram Bot - Verificação de Setup{Colors.END}")
    print(f"{Colors.BOLD}{'='*50}{Colors.END}")

    checks = [
        ("Python 3.11+", check_python_version),
        ("Dependências", check_dependencies),
        ("Arquivo .env", check_env_file),
        ("Token Telegram", check_telegram_token),
        ("Estrutura do Projeto", check_project_structure),
        ("PostgreSQL", check_database_connection),
    ]

    results = {}

    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print_error(f"Erro ao verificar {name}: {e}")
            results[name] = False

    # Summary
    print_header("Resumo da Verificação")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, result in results.items():
        if result:
            print_success(name)
        else:
            print_error(name)

    print(f"\n{Colors.BOLD}Resultado: {passed}/{total} verificações passaram{Colors.END}\n")

    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ Tudo pronto! Execute o bot com:{Colors.END}")
        print(f"{Colors.BLUE}  python bot/main.py{Colors.END}")
        print(f"{Colors.BLUE}  ou{Colors.END}")
        print(f"{Colors.BLUE}  run.bat (Windows) / ./run.sh (Linux/Mac){Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Algumas verificações falharam{Colors.END}")
        print(f"{Colors.YELLOW}Corrija os problemas acima antes de executar o bot{Colors.END}\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
