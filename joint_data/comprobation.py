import json

def compare_files(control_group_file, user_file):
    cg_data = json.load(open(control_group_file))
    user_data = json.load(open(user_file))

    # Límites de orientación de joints [1, 3] (espalda/abdomen y pecho superior)
    limites_max = [-80.0, 12.5, -17.5]
    limites_min = [15, -14.5, 11.30]

    difference = {}

    for i in user_data:
        timestamp = i.get("timestamp", [])  # Usa get para obtener una lista vacía si no existe timestamp
        joint_rotations = i.get("joint_rotations",
                                [])  # Usa get para obtener una lista vacía si no existe joint_rotations

        # Verifica si la lista timestamp no está vacía y tiene al menos un elemento
        if timestamp and timestamp[0] and joint_rotations and joint_rotations[0]:
            # Accede a los valores de joint_rotations
            values = joint_rotations[0][0]

            if all(limites_min[i] <= values[i] <= limites_max[i] for i in range(3)):
                print(f'En timestamp {timestamp[0]}, los valores {joint_rotations[0][0]} están dentro de los límites.')
            else:
                print(f'En timestamp {timestamp[0]}, los valores {joint_rotations[0][0]} están fuera de los límites.')
        else:
            print("Datos faltantes en la entrada.")