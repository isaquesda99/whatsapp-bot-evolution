import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

INSTANCE = "minha_sessao"  # nome da instância criada no painel Evolution
BASE_URL = "https://api.evolutionapi.com.br"  # URL do Evolution hospedado
TOKEN = "SEU_TOKEN_AQUI"  # token gerado no painel Evolution

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Função para enviar mensagem
def send_message(phone, message):
    data = {"number": phone, "text": message}
    url = f"{BASE_URL}/message/sendText/{INSTANCE}"
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# Rota para receber mensagens
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data and 'messages' in data:
        for msg in data['messages']:
            phone = msg['key']['remoteJid']
            text = msg['message']['conversation']
            print(f"Mensagem recebida de {phone}: {text}")

            if "oi" in text.lower():
                send_message(phone, "Olá! 👋 Sou seu bot Python no Render usando Evolution API.")
            elif "pdf" in text.lower():
                send_message(phone, "Envie o PDF e eu posso analisá-lo futuramente 📄.")
            else:
                send_message(phone, "Desculpe, não entendi. Envie 'oi' para começar 😊")

    return jsonify({"status": "ok"}), 200

@app.route('/')
def home():
    return "✅ Bot Evolution API Python ativo no Render!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
