import joint_sorting
import json

ejercicios = ['peso_muerto', 'sentadilla', 'flexion']
current_exercise = joint_sorting.objeto_timestamp

nombres_archivos = []  # Se sacan de los ejercicios/series que elige el usuario, de Thomas
numero_series = [1, 2, 3, 4, 5, 6]  # Se sacan de los ejercicios/series que elige el usuario, de Thomas

for nombre_ejercicio in ejercicios:
    for numero in numero_series:
        print('Nombre ejercicio: ', nombre_ejercicio + ', número: ', numero)
        # Crear nuevo nombre de archivo json
        nombre_archivo = "joint_dtata" + nombre_ejercicio + "_" + str(numero)

        # Guardar el archivo JSON con el nuevo nombre
        with open(nombre_archivo, "w") as archivo:
            json.dump(current_exercise, archivo)

        # Añadir el nuevo nombre de archivo a la lista
        nombres_archivos.append(nombre_archivo)
