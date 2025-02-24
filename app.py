from flask import Flask, jsonify
from flask_socketio import SocketIO
import requests
import json
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép WebSocket kết nối từ mọi nơi

def get_inbox(email):
    """Hàm lấy danh sách email từ getnada"""
    url = f"https://inboxes.com/api/v2/inbox/{email}"
    response = requests.get(url)
    return response.json() if response.ok else {}

@app.route("/<email>")
def inbox(email):
    """Trả về hộp thư khi gọi API"""
    emails = get_inbox(email)
    return jsonify(emails)

@socketio.on("listen_email")
def listen_email(data):
    """Lắng nghe email mới qua WebSocket"""
    email = data.get("email")
    if not email:
        return

    last_email_id = None

    while True:
        inbox = get_inbox(email)
        if inbox and "msgs" in inbox:
            latest_email = inbox["msgs"][0]
            email_id = latest_email["uid"]

            if email_id != last_email_id:  # Nếu có email mới
                socketio.emit("new_email", latest_email)  # Gửi email qua WebSocket
                last_email_id = email_id

        eventlet.sleep(5)  # Kiểm tra mỗi 5 giây

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
