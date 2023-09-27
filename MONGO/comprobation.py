import json

def compare_files(control_group_file, user_file):
    cg_data = json.load(open(control_group_file))
    user_data = json.load(open(user_file))

    # Límites de orientación de joints [1, 3] (espalda/abdomen y pecho superior)
    max_limit = 1
    min_limit = 0

    difference = {}

    for key in cg_data:
        if key not in user_data:
            difference[key] = "No existe en el archivo de usuario"
        elif cg_data[key] != user_data[key]:
            difference[key] = "Diferente"

    return difference

if __name__ == "__main__":
    control_group_file = "rutaarchivo/grupocontrol.json"
    user_file = "data/file2.json"

    difference = compare_files(control_group_file, user_file)

    for key, value in difference.items():
        print(f"{key}: {value}")
