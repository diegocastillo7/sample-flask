from flask import Flask, request, render_template, redirect, jsonify
import pymysql
app = Flask(__name__)

datos = {}
data_grafica = []

led_status = 'off'
valvx_status = 'off'
valvy_status = 'off'

def get_db_connection():
    # Establece la conexión a la base de datos
    conn = pymysql.connect(
        host='db-compostaje-do-user-14268783-0.b.db.ondigitalocean.com',
        user='doadmin',
        password='AVNS_WQGsJSdziwkjigSLoFk',
        database='defaultdb',
        port=25060,
        ssl={'ssl': {'sslmode': 'require'}}
    )
    return conn

@app.route('/')
def hello_world():  # put application's code here
    global datos
    return render_template('index.html', datos=datos)

@app.route('/datos', methods=['POST'])
def recibir_datos():
    global datos
    datos = request.json
    print(datos)
    temperatura_x = datos.get('PROM T-X', 0)
    temperatura_y = datos.get('PROM T-Y', 0)
    humedad_x = datos.get('PROM H-X', 0)
    humedad_y = datos.get('PROM H-Y', 0)

    # Establece la conexión a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Inserta los datos en la tabla "datos"
    query = "INSERT INTO Datos (TemperaturaX, TemperaturaY, HumedadX, HumedadY) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (temperatura_x, temperatura_y, humedad_x, humedad_y))

    # Guarda los cambios en la base de datos
    conn.commit()

    # Cierra la conexión a la base de datos
    cursor.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/led', methods=['GET', 'POST'])
def led():
    global led_status
    print(led_status)
    if request.method == 'GET':
        data = jsonify({'value': led_status})
        led_status = 'off'
        return data
    elif request.method == 'POST':
        data = request.get_json(force=True) # forzar el tipo de contenido a JSON
        led_status = data['value']
        return jsonify({'value': led_status})

@app.route('/valvx', methods=['GET', 'POST'])
def valvx():
    global valvx_status
    print(valvx_status)
    if request.method == 'GET':
        data = jsonify({'value': valvx_status})
        valvx_status = 'off'
        return data

    elif request.method == 'POST':
        data = request.get_json(force=True)  # forzar el tipo de contenido a JSON
        valvx_status = data['valuevx']
        return jsonify({'valuevx': valvx_status})

@app.route('/valvy', methods=['GET', 'POST'])
def valvy():
    global valvy_status
    print(valvy_status)
    if request.method == 'GET':
        data = jsonify({'value': valvy_status})
        valvy_status = 'off'
        return data

    elif request.method == 'POST':
        data = request.get_json(force=True)  # forzar el tipo de contenido a JSON
        valvy_status = data['valuevy']
        return jsonify({'valuevy': valvy_status})

@app.route('/datos_grafica', methods=['GET'])
def obtener_datos():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Obtiene los datos de la tabla "datos"
    query = "SELECT * FROM Datos"
    cursor.execute(query)
    return jsonify({'success': True})

    results = cursor.fetchall()
    global data_grafica
    for result in results:
        data_grafica.append({
            'id': result[0],
            'temperatura_x': result[1],
            'temperatura_y': result[2],
            'humedad_x': result[3],
            'humedad_y': result[4]
        })
    # Cierra la conexión a la base de datos
    cursor.close()
    conn.close()
    print(data_grafica)
    dataArray = data_grafica
    return jsonify(dataArray)

@app.route('/graficos')
def graficos():
    return render_template('graficos.html')
