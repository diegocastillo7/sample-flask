from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import requests
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')
    while True:
        try:
            # Realizar una solicitud GET al servidor y obtener la respuesta
            r = requests.get('http://190.60.32.36/enviar-datos')
            humedad = float(request.args.get('humedad', 0))
            print(humedad)
            # Enviar el valor de humedad al cliente a través del socket
            socketio.emit('datos', {'datos': humedad})
        except:
            print('Error al obtener datos')
        time.sleep(1)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)