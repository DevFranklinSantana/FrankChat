from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

messages = []

@app.route("/")

def index():
    return render_template("index.html", title="Home")

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    user = data.get('user')
    message = data.get('message')
    if user and message:
        messages.append({'user': user, 'message': message})
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

@app.route('/poll', methods=['GET'])
def poll_messages():
    return jsonify(messages), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





