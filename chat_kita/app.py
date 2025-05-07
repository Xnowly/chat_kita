from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username
    send(f"🟢 {username} telah bergabung.", broadcast=True)

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, "Anonim")
    send(f"<b>{username}</b>: {msg}", broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = users.get(request.sid, "Anonim")
    send(f"🔴 {username} keluar dari chat.", broadcast=True)
    users.pop(request.sid, None)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
