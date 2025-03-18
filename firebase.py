import firebase_admin
from firebase_admin import credentials, firestore

# Cargar las credenciales
cred = credentials.Certificate("/nominas-c4e89-firebase-adminsdk-fbsvc-a5a6b7f161.json")  # Reemplaza con tu ruta real
firebase_admin.initialize_app(cred)

# Conectar a Firestore
db = firestore.client()

# Función para agregar un empleado
def agregar_empleado(id, nombre, apellidos, fecha_ingreso, puesto, sueldo):
    empleado = {
        "nombre": nombre,
        "apellidos": apellidos,
        "fecha_ingreso": fecha_ingreso,
        "puesto": puesto,
        "sueldo": sueldo
    }
    db.collection("empleados").document(id).set(empleado)
    print(f"Empleado {nombre} agregado con éxito.")

# Función para obtener todos los empleados
def obtener_empleados():
    empleados_ref = db.collection("empleados").stream()
    for empleado in empleados_ref:
        print(f"{empleado.id} => {empleado.to_dict()}")

# Ejemplo de uso
if __name__ == "__main__":
    agregar_empleado("001", "Angel", "Pérez", "2021-06-15", "Control de Calidad", 5000)
    obtener_empleados()
