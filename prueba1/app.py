from flask import Flask, render_template, request
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

app = Flask(__name__)

# Callback que se ejecuta cuando se recibe un mensaje en el topic "esp32/analog1"
def on_message1(client, userdata, message):
    # Actualizar el valor actual de la entrada analógica
    app.config['MSG_ANALOG_01'] = message.payload.decode('utf-8')

def on_message2(client, userdata, message):
    # Actualizar el valor actual de la entrada analógica
    app.config['MSG_ANALOG_02'] = message.payload.decode('utf-8')

# Callback que se ejecuta cuando se recibe un mensaje en los topics "esp32/analog1" y "Salida/02"
def on_message(client, userdata, message):
    if message.topic == "Variable/01":
        on_message1(client, userdata, message)
    elif message.topic == "Variable/02":
        on_message2(client, userdata, message)

# Conectar al broker MQTT y suscribirse al topic "Salida/01" al inicio de la aplicación
def on_connect(client, userdata, flags, rc):
    print('Conectado al broker MQTT')
    client.subscribe('Variable/01')
    client.subscribe('Variable/02')

# Configuración inicial de la aplicación
def init_app():
    # Configuración del valor actual de la entrada analógica
    app.config['MSG_ANALOG_01'] = '0'
    app.config['MSG_ANALOG_02'] = '0'

    # Conexión al broker MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('broker.emqx.io', 1883, 60)

    # Arrancar el loop para recibir mensajes del broker MQTT en un hilo separado
    client.loop_start()

# Ruta principal
@app.route('/')
def index():
    # Renderizar la plantilla HTML y pasar el valor actual de la entrada analógica
    return render_template('index.html', msg_analog_01=app.config['MSG_ANALOG_01'], msg_analog_02=app.config['MSG_ANALOG_02'])

# Ruta para activar la salida 1
@app.route('/salida1_on')
def salida1_on():
    publish.single("actuador/01", "1", hostname="broker.emqx.io")
    return 'Salida 1 activada'

# Ruta para desactivar la salida 1
@app.route('/salida1_off')
def salida1_off():
    publish.single("actuador/01", "0", hostname="broker.emqx.io")
    return 'Salida 1 desactivada'

# Ruta para activar la salida 2
@app.route('/salida2_on')
def salida2_on():
    publish.single("actuador/02", "1", hostname="broker.emqx.io")
    return 'Salida 2 activada'

# Ruta para desactivar la salida 2
@app.route('/salida2_off')
def salida2_off():
    publish.single("actuador/02", "0", hostname="broker.emqx.io")
    return 'Salida 2 desactivada'

if __name__ == '__main__':
    init_app()
    app.run(debug=True)