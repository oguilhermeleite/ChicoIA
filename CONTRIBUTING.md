# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o ChicoIA Telegram Bot!

## 📋 Como Contribuir

### 1. Reportar Bugs

Encontrou um bug? Abra uma issue com:

- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Screenshots (se aplicável)
- Versão do Python e do bot
- Sistema operacional

### 2. Sugerir Melhorias

Tem uma ideia? Abra uma issue com:

- Descrição detalhada da feature
- Caso de uso
- Benefícios esperados
- Mockups ou exemplos (se aplicável)

### 3. Pull Requests

#### Setup para Desenvolvimento

```bash
# 1. Fork o repositório

# 2. Clone seu fork
git clone https://github.com/seu-usuario/chicobot-telegram.git
cd chicobot-telegram

# 3. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 4. Instale dependências de dev
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# 5. Configure pre-commit hooks (opcional)
pip install pre-commit
pre-commit install
```

#### Processo de PR

1. **Crie uma branch**
   ```bash
   git checkout -b feature/minha-feature
   # ou
   git checkout -b fix/meu-bug-fix
   ```

2. **Faça suas alterações**
   - Siga o estilo de código existente
   - Adicione testes para novas features
   - Atualize a documentação

3. **Teste suas alterações**
   ```bash
   # Executar testes
   pytest

   # Verificar cobertura
   pytest --cov=bot --cov-report=html

   # Linting
   flake8 bot/ models/ utils/

   # Formatação
   black bot/ models/ utils/

   # Type checking
   mypy bot/ models/ utils/
   ```

4. **Commit suas alterações**
   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade X"
   ```

   Use conventional commits:
   - `feat:` - Nova feature
   - `fix:` - Bug fix
   - `docs:` - Documentação
   - `style:` - Formatação
   - `refactor:` - Refatoração
   - `test:` - Testes
   - `chore:` - Manutenção

5. **Push para seu fork**
   ```bash
   git push origin feature/minha-feature
   ```

6. **Abra um Pull Request**
   - Descreva claramente as mudanças
   - Referencie issues relacionadas
   - Aguarde review

## 📝 Estilo de Código

### Python

- Siga PEP 8
- Use type hints
- Docstrings em todas as funções públicas
- Máximo 100 caracteres por linha

```python
def exemplo_funcao(parametro: str, opcional: int = 0) -> bool:
    """
    Descrição curta da função

    Args:
        parametro: Descrição do parâmetro
        opcional: Descrição do parâmetro opcional

    Returns:
        Descrição do retorno
    """
    # Implementação
    return True
```

### Mensagens em Português

- Todas as mensagens do bot devem estar em português brasileiro
- Mantenha o tom empático e amigável do Chico
- Evite gírias muito informais

## 🧪 Testes

### Escrever Testes

```python
# tests/test_nova_feature.py
import pytest
from bot.minha_feature import MinhaClasse


class TestMinhaFeature:
    """Testes para minha feature"""

    def test_caso_basico(self):
        """Testa caso básico"""
        resultado = MinhaClasse().metodo()
        assert resultado == esperado

    @pytest.mark.asyncio
    async def test_caso_assincrono(self):
        """Testa caso assíncrono"""
        resultado = await MinhaClasse().metodo_async()
        assert resultado == esperado
```

### Executar Testes

```bash
# Todos os testes
pytest

# Teste específico
pytest tests/test_nova_feature.py

# Com verbosidade
pytest -v

# Com cobertura
pytest --cov=bot --cov-report=html
```

## 📚 Documentação

### Atualizar README

Se sua mudança afeta o uso do bot:

1. Atualize `README.md`
2. Atualize `QUICKSTART.md` se necessário
3. Adicione exemplos de uso

### Docstrings

```python
def analisar_jogo(time1: str, time2: str, campeonato: str = None) -> dict:
    """
    Analisa um jogo entre dois times

    Esta função utiliza o Gemini AI para analisar o confronto entre
    dois times, considerando histórico, estatísticas e momento atual.

    Args:
        time1: Nome do primeiro time
        time2: Nome do segundo time
        campeonato: Campeonato/liga (opcional)

    Returns:
        Dicionário com análise completa:
        {
            'contexto': str,
            'mercados': list,
            'confianca': str
        }

    Raises:
        ValueError: Se os nomes dos times forem inválidos
        APIError: Se houver erro na API do Gemini

    Examples:
        >>> analisar_jogo("Flamengo", "Palmeiras", "Brasileirão")
        {'contexto': '...', 'mercados': [...], 'confianca': 'alta'}
    """
    # Implementação
    pass
```

## 🐛 Debug

### Logs

```python
import logging

logger = logging.getLogger(__name__)

# Use níveis apropriados
logger.debug("Informação detalhada para debug")
logger.info("Informação geral")
logger.warning("Aviso sobre algo inesperado")
logger.error("Erro que não impediu execução")
logger.critical("Erro crítico")
```

### Variáveis de Ambiente de Dev

```env
# .env.development
TELEGRAM_BOT_TOKEN=seu_token_de_teste
GEMINI_API_KEY=sua_key_de_teste
DATABASE_URL=postgresql://localhost/chicobot_test
ENVIRONMENT=development
DEBUG=True
```

## 🔒 Segurança

### Nunca Commite

- ❌ Tokens ou API keys
- ❌ Senhas
- ❌ Dados de usuários reais
- ❌ Arquivo `.env`

### Sempre

- ✅ Use `.env.example` para templates
- ✅ Sanitize inputs do usuário
- ✅ Valide dados antes de processar
- ✅ Use prepared statements para SQL

## 🎨 Personalização do Chico

### Adicionar Novas Respostas

```python
# bot/prompts.py
NOVA_CATEGORIA_PROMPT = """
Seu prompt aqui mantendo o tom do Chico:
- Empático
- Direto
- Amigável
"""
```

### Novos Comandos

```python
# bot/handlers.py
async def novo_comando(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /novocomando

    Args:
        update: Telegram update
        context: Callback context
    """
    # Implementação
    await update.message.reply_text("Resposta")

# bot/main.py
application.add_handler(CommandHandler("novocomando", handlers.novo_comando))
```

## 📊 Performance

### Considerações

- Use async/await para operações I/O
- Cache respostas quando apropriado
- Limite tamanho de histórico de conversas
- Implemente rate limiting

### Exemplo de Cache

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def funcao_cacheable(parametro: str) -> str:
    # Computação custosa
    return resultado
```

## 📞 Contato

Dúvidas sobre contribuição?

- 📧 dev@chicoia.com.br
- 💬 Abra uma issue de discussão

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas
sob a mesma licença do projeto.

---

**Obrigado por contribuir! 🙏**
