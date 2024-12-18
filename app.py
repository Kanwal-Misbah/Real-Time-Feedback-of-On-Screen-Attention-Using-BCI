from flask import Flask, render_template
from flask_socketio import SocketIO
from NeuroPy import NeuroPy
import time
from threading import Lock

app = Flask(__name__)
socketio = SocketIO(app)
lock = Lock()

# NeuroSky connection settings
neuropy = NeuroPy.NeuroPy("COM11", 57600)

@socketio.on('connect')
def handle_connection():
    def read_neuro_values():
        neuropy.start()
        while True:
            with lock:
                attention = neuropy.attention
                meditation = neuropy.meditation
            socketio.emit('neuro_data', {'attention': attention, 'meditation': meditation})
            time.sleep(0.5)

    socketio.start_background_task(read_neuro_values)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False)
