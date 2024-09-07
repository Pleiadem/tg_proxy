from flask import Flask, request
import requests

app = Flask(__name__)

# Telegram bot token from BotFather (需要替换为你自己的Bot Token)
BOT_TOKEN = 'your_bot_token_here'
# Your chat_id (需要替换为你的chat_id)
CHAT_ID = 'your_chat_id_here'

# Function to send message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

# Route to handle requests from your internal server
@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()  # Get the data sent by your server
    if 'message' in data:
        send_telegram_message(data['message'])  # Send the message to Telegram
        return 'Message sent!\n', 200
    return 'No message found\n', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3003)
