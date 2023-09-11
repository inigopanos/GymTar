import json

# Ruta del archivo JSON original
# ruta_json = 'D:\\CosasInigo\\GymTar-Proyecto\\bodies.json' # UNI
ruta_json = 'D:\\GymTar\\GymTar\\bodies.json'

# Ruta del nuevo archivo JSON donde se guardarán los datos limpios
ruta_archivo_limpio = "D:\\GymTar\\GymTar\\MONGO\\sorted_joints.json"

# Lista para almacenar los objetos limpios
objetos_limpios = []

# Índices de los elementos que deseas conservar en local_orientation_per_joint
indices_deseados = [1, 3, 5, 6, 12, 13, 18, 19, 22, 23]

# Cargar el archivo JSON original
with open(ruta_json, "r") as archivo:
    datos_originales = json.load(archivo)
    print('Datos originales:', datos_originales)

# Recorrer los objetos en el archivo original
for orientation_data, value in datos_originales.items():

    print('Orientation_data: ', value)
    body_list = value.get("body_list", [])

    print('Body_list: ', type(body_list))

    local_orientation_per_joint_original = []
    body_list_original = []

    if body_list:
        body_list_original = body_list.copy()
        print('Orientación local: ', body_list_original, type(body_list_original))

    print('Longitud de dict: ', len(body_list_original))

    if body_list_original:
        primer_elemento = body_list_original[0]
        local_orientation_per_joint_original = primer_elemento["local_orientation_per_joint"]
        print('Local_Orientation_Original: ', local_orientation_per_joint_original)
    else:
        print('La lista body_list_original está vacía')

    if len(local_orientation_per_joint_original) >= max(indices_deseados) + 1:
        # Seleccionar solo los elementos deseados según los índices
        local_orientation_per_joint_limpio = [local_orientation_per_joint_original[i] for i in indices_deseados]
    else:
        # Si no hay suficientes elementos, deja la lista vacía
        local_orientation_per_joint_limpio = []
    # Seleccionar solo los elementos deseados según los índices

    # Crear un nuevo objeto con los elementos limpios
    objeto_limpio = {
        "local_orientation_per_joint": local_orientation_per_joint_limpio
    }
    print('Objeto limpio: ', objeto_limpio)
    # Agregar el nuevo objeto a la lista de objetos limpios
    objetos_limpios.append(objeto_limpio)

# Guardar la lista de objetos limpios en un nuevo archivo JSON
with open(ruta_archivo_limpio, "w") as archivo:
    json.dump(objetos_limpios, archivo, indent=4)
