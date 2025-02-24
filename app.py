from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_inbox(email):
    url = f"https://inboxes.com/api/v2/inbox/{email}"
    response = requests.get(url)
    if response.ok:
        return response.json().get("msgs", [])
    return []

@app.route('/get-email', methods=['GET'])
def get_email():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Missing email parameter"}), 400
    
    inbox = get_inbox(email)
    return jsonify(inbox)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
