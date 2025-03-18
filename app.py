from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

app = Flask(__name__)

# Initialize Firebase Admin (only if not already initialized)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/empleados')
def get_empleados():
    try:
        empleados_ref = db.collection('empleados')
        docs = empleados_ref.stream()
        empleados = []
        for doc in docs:
            empleado = doc.to_dict()
            empleado['id'] = doc.id
            empleados.append(empleado)
        return jsonify(empleados)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/registrar_empleado', methods=['POST'])
def registrar_empleado():
    try:
        data = {
            'nombre': request.form['nombre'],
            'apellidos': request.form['apellidos'],
            'fecha_ingreso': request.form['fecha_ingreso'],
            'puesto': request.form['puesto'],
            'sueldo': float(request.form['sueldo']),
            'horas_extra': 0,
            'sueldo_x_hr_extra': 0,
            'material_asignado': []
        }
        db.collection('empleados').add(data)
        return jsonify({"message": "Empleado registrado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/agregar_horas', methods=['POST'])
def agregar_horas():
    try:
        empleado_id = request.form['empleado_id']
        horas_extra = int(request.form['horas_extra'])
        
        empleado_ref = db.collection('empleados').document(empleado_id)
        empleado = empleado_ref.get()
        
        if empleado.exists:
            sueldo = empleado.to_dict().get('sueldo', 0)
            sueldo_x_hr_extra = sueldo / 160  # Assuming 160 working hours per month
            
            empleado_ref.update({
                'horas_extra': horas_extra,
                'sueldo_x_hr_extra': sueldo_x_hr_extra
            })
            return jsonify({"message": "Horas extra registradas exitosamente"}), 200
        else:
            return jsonify({"error": "Empleado no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/asignar_materiales', methods=['POST'])
def asignar_materiales():
    try:
        empleado_id = request.form['empleado_id_material']
        material = request.form['materiales']
        
        empleado_ref = db.collection('empleados').document(empleado_id)
        empleado = empleado_ref.get()
        
        if empleado.exists:
            materiales_actuales = empleado.to_dict().get('material_asignado', [])
            if material not in materiales_actuales:
                materiales_actuales.append(material)
                empleado_ref.update({
                    'material_asignado': materiales_actuales
                })
            return jsonify({"message": "Material asignado exitosamente"}), 200
        else:
            return jsonify({"error": "Empleado no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)