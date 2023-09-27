import json

def compare_files(control_group_file, user_file):
    cg_data = json.load(open(control_group_file))
    user_data = json.load(open(user_file))

    # Límites de orientación de joints [1, 3] (espalda/abdomen y pecho superior)
    max_joint_3_limit = [-80.0, 12.5, -17.5]
    min_joint_3_limit = [15, -14.5, 11.30]

    difference = {}

    for i in range(len(user_data)):
        if min_joint_3_limit[i] <= cg_data[i] <= max_joint_3_limit[i]:
            print(f'El valor {user_data[i]} en la posición {i} está dentro de los límites.')
        else:
            print(f'El valor {user_data[i]} en la posición {i} está fuera de los límites.')

    return difference
