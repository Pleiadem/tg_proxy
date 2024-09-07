# tg_proxy
在国内访问 Telegram 可能会遇到一些限制，因此我们可以通过自建代理服务器来解决这一问题。本文将介绍如何使用 Python 的 Flask 框架和 Telegram 的 Bot API 搭建一个简单的 Telegram Bot 代理服务，通过 HTTP 请求的方式，让 Telegram 机器人能够正常工作。我们还会展示如何通过 curl 命令来发送消息。
### 使用 Flask 构建一个 Telegram Bot 代理服务

在国内访问 Telegram 可能会遇到一些限制，因此我们可以通过自建代理服务器来解决这一问题。本文将介绍如何使用 Python 的 Flask 框架和 Telegram 的 Bot API 搭建一个简单的 Telegram Bot 代理服务，通过 HTTP 请求的方式，让 Telegram 机器人能够正常工作。我们还会展示如何通过 `curl` 命令来发送消息。

#### 先决条件

1. **Flask**：这是一个轻量级的 Python Web 框架，用于处理 HTTP 请求。
2. **requests**：用于向 Telegram API 发送请求。
3. **Telegram Bot**：通过 [BotFather](https://t.me/BotFather) 创建一个 Telegram 机器人，并获取 API token。
4. **Python 环境**：确保已经安装 Python 3.6 及以上版本。

### 代码实现

以下是 Flask 应用的完整代码，用于接收 HTTP 请求并将请求中的消息发送到指定的 Telegram 机器人。

```python
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
```

### 如何部署

你可以将此程序部署在 VPS 或云服务器上。确保服务器上的防火墙配置允许 3003 端口访问~~，并且你已经申请了域名或配置了 Nginx/Apache 来反向代理 HTTP 请求。~~

#### 通过 systemd 将 Flask 程序持久化

为了使程序在服务器重启后自动启动，你可以将其注册为 systemd 服务。

1. 创建服务文件：

   ```bash
   sudo nano /etc/systemd/system/tg_proxy.service
   ```

2. 添加如下内容：

   ```ini
   [Unit]
   Description=Flask Telegram Proxy Service
   After=network.target

   [Service]
   User=<your_username>
   WorkingDirectory=</path/to/your/flask/app>
   ExecStart=</usr/bin/python3> </path/to/your/flask/app/app.py>
   Restart=always
   Environment="FLASK_ENV=production"

   [Install]
   WantedBy=multi-user.target
   ```

3. 启用并启动服务：

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start tg_proxy
   sudo systemctl enable tg_proxy
   ```

### 使用示例

完成配置后，你可以通过 `curl` 命令发送 POST 请求，将消息转发到你的 Telegram 机器人。以下是一个示例：

```bash
curl -X POST https://your_domain_or_ip/notify \
-H "Content-Type: application/json" \
-d '{"message":"这是测试消息"}'
```

此命令会通过 `/notify` 接口向你的 Flask 应用发送请求，并将 `{"message":"这是测试消息"}` 作为数据传递，最终会在 Telegram 上收到该消息。

### 小结

通过使用 Flask 和 Telegram 的 Bot API，我们可以轻松地搭建一个 Telegram Bot 代理服务，帮助国内的机器访问 Telegram 服务。此程序允许你通过 HTTP 请求发送消息到 Telegram，可以集成到你的内部服务或脚本中，帮助实现消息通知的功能。

---

*注意：文中的 Bot Token 和 Chat ID 请替换为你自己的实际值。*

对于更复杂的功能，你可以在这个基础上添加更多的业务逻辑。
