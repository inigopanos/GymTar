import numpy as np
import json
from fused_cameras import json_export
from scipy.spatial.transform import Rotation
from comprobation import compare_files

# Ruta del archivo JSON original
# ruta_json = 'D:\\CosasInigo\\GymTar-Proyecto\\bodies.json' # UNI
# ruta_json = 'D:\\GymTar\\GymTar\\bodies.json' # CASA

# Ruta del nuevo archivo JSON donde se guardarán los datos limpios
# ruta_archivo_limpio = "D:\\GymTar\\GymTar\\MONGO\\sorted_joints_pesoMuerto1.json" # CASA
ruta_archivo_limpio = "D:\\CosasInigo\\GymTar-Proyecto\\MONGO\\json\\sorted_joints_pesoMuerto1.json" # UNI


ruta_json_original = json_export.ruta_json
# Lista para almacenar los objetos limpios
objetos_limpios = []

# Índices de los elementos que deseas conservar en local_orientation_per_joint
indices_deseados = [3]
# indices_deseados = [1, 3, 5, 6, 12, 13, 18, 19, 22, 23]


# Crear un objeto JSONEncoder personalizado
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return json.JSONEncoder.default(self, obj)


# Cargar el archivo JSON original
with open(ruta_json_original, "r") as archivo:
    datos_originales = json.load(archivo)

# Recorrer los objetos en el archivo original. Por cada objeto se añade el timestamps y las
# orientaciones en Euler.
for orientation_data, value in datos_originales.items():

    body_list = value.get("body_list", [])

    timestamp_original = 0
    local_orientation_per_joint_original = []
    body_list_original = []
    nombre_ejercicio = ''

    objeto_timestamp = {
        "timestamp": [],
        "joint_rotations": {}
    }

    if body_list:
        body_list_original = body_list.copy()
        timestamp_original = value.get("timestamp", 0)
        objeto_timestamp.update({
            "timestamp": timestamp_original
        })
        # print('Body local: ', body_list_original, type(body_list_original))

    if body_list_original:
        primer_elemento = body_list_original[0]
        local_orientation_per_joint_original = primer_elemento["local_orientation_per_joint"]
    else:
        print('La lista body_list_original está vacía')

    if len(local_orientation_per_joint_original) >= max(indices_deseados) + 1:
        # Añadir etiqueta de nombre de ejercicio
        # nombre_ejercicio = datosPasadosPorThomas.nombre_ejercicio
        # Seleccionar solo los elementos deseados según los índices
        local_orientation_per_joint_limpio = [local_orientation_per_joint_original[i] for i in indices_deseados]
        print('Local orientation per joint limpio: ', local_orientation_per_joint_limpio)
    else:
        # Si no hay suficientes elementos, deja la lista vacía
        local_orientation_per_joint_limpio = []

    rot_euler = []
    list_rot_euler = []

    for joint in local_orientation_per_joint_limpio:
        # Cambiar los objetos de quaterniones a Euler
        rot = Rotation.from_quat(joint)
        rot_euler = rot.as_euler('xyz', degrees=True)
        list_rot_euler.append(rot_euler)
        print('Rotación Euler:', rot_euler)
        objeto_timestamp.update({
            "joint_rotations": [list_rot_euler],
        })

    objetos_limpios.append(objeto_timestamp)

# Guardar la lista de objetos limpios en un nuevo archivo JSON
with open(ruta_archivo_limpio, "w") as archivo:
    json.dump(objetos_limpios, archivo, cls=NumpyEncoder, indent=4)


control_group_data = ruta_archivo_limpio
compare_files()