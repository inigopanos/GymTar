import json

# Ruta del archivo JSON original
ruta_json = 'D:\\CosasInigo\\GymTar-Proyecto\\bodies.json'

# Ruta del nuevo archivo JSON donde se guardarán los datos limpios
ruta_archivo_limpio = "MONGO/sorted_joints.json"

# Lista para almacenar los objetos limpios
objetos_limpios = []

# Índices de los elementos que deseas conservar en local_orientation_per_joint
indices_deseados = [1, 3, 5, 6, 12, 13, 18, 19, 22, 23]

# Cargar el archivo JSON original
with open(ruta_json, "r") as archivo:
    datos_originales = json.load(archivo)

# Recorrer los objetos en el archivo original
for clave, objeto in datos_originales.items():
    # Verificar si la clave es un número (como "1694079900854")
    if clave.isdigit():
        # Obtener local_orientation_per_joint del objeto actual
        local_orientation_per_joint_original = objeto.get("local_orientation_per_joint", [])

        # Seleccionar solo los elementos deseados según los índices
        local_orientation_per_joint_limpio = [local_orientation_per_joint_original[i] for i in indices_deseados]

        # Crear un nuevo objeto con los elementos limpios
        objeto_limpio = {
            "local_orientation_per_joint": local_orientation_per_joint_limpio
        }

        # Agregar el nuevo objeto a la lista de objetos limpios
        objetos_limpios.append(objeto_limpio)

# Guardar la lista de objetos limpios en un nuevo archivo JSON
with open(ruta_archivo_limpio, "w") as archivo:
    json.dump(objetos_limpios, archivo, indent=4)
