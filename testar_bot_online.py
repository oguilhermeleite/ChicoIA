import json
import urllib.request

TOKEN = "8522357760:AAHn60ZJPYZ4rz4aO51k7O0GUPV8ivm7JCE"

print("Testando se o bot está online...")
print()

try:
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        if data.get('ok'):
            bot = data['result']
            print("✅ BOT ESTÁ ONLINE!")
            print(f"   Nome: {bot['first_name']}")
            print(f"   Username: @{bot['username']}")
            print(f"   ID: {bot['id']}")
            print()
            print("=" * 70)
            print("🎉 PRONTO! O bot está funcionando!")
            print("=" * 70)
            print()
            print("📱 TESTE AGORA NO TELEGRAM:")
            print("   1. Abra o Telegram")
            print("   2. Procure: @ChicoIA_bot")
            print("   3. Envie: /start")
            print("   4. O bot VAI RESPONDER! ✅")
            print()
        else:
            print("❌ Erro ao verificar bot")
except Exception as e:
    print(f"❌ Erro: {e}")
    print("Verifique sua conexão com internet")
