import numpy as np
import json
import time

ruta_json = 'D:\\CosasInigo\\GymTar-Proyecto\\MONGO\\GRUPO_CONTROL\\souleve_de_terre.json'

tiempo_inicial = time.time()
print('Tiempo inicial: ', tiempo_inicial)

def addIntoOutput(out, identifier, tab):
    out[identifier] = []
    for element in tab:
        out[identifier].append(element)
    return out

def serializeBodyData(body_data):
    """Serialize BodyData into a JSON like structure"""
    out = {}
    out["id"] = body_data.id
    out["unique_object_id"] = str(body_data.unique_object_id)
    out["tracking_state"] = str(body_data.tracking_state)
    out["action_state"] = str(body_data.action_state)
    addIntoOutput(out, "position", body_data.position)
    out["confidence"] = body_data.confidence
    addIntoOutput(out, "keypoint", body_data.keypoint)
    addIntoOutput(out, "keypoint_confidence", body_data.keypoint_confidence)
    # addIntoOutput(out, "local_position_per_joint", body_data.local_position_per_joint)
    # addIntoOutput(out, "local_orientation_per_joint", body_data.local_orientation_per_joint)
    out["local_position_per_joint"] = body_data.local_position_per_joint
    out["local_orientation_per_joint"] = body_data.local_orientation_per_joint

    return out

def serializeBodies(bodies):
    """Serialize Bodies objects into a JSON like structure"""
    "Esto escribe el json, lo otro no hace nada"

    out = {}
    out["is_new"] = bodies.is_new
    out["is_tracked"] = bodies.is_tracked
    out["timestamp"] = [bodies.timestamp.get_seconds() - tiempo_inicial]
    out["body_list"] = []

    for sk in bodies.body_list:
        out["body_list"].append(serializeBodyData(sk))

    return out

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

skeleton_file_data = {}

def saveData(bodies):
    # Save data into JSON file:

    # ruta_json = 'D:\\CosasInigo\\GymTar-Proyecto\\bodies.json'
    # ruta_json = 'D:\\CosasInigo\\GymTar-Proyecto\\MONGO\\GRUPO_CONTROL\\souleve_de_terre.json'
    with open(ruta_json, 'w') as file_sk:
        skeleton_file_data[str(bodies.timestamp.get_seconds())] = serializeBodies(bodies)
        # print('SkeletonFile: ', skeleton_file_data)

        file_sk = open(ruta_json, 'w')

        file_sk.write(json.dumps(skeleton_file_data, cls=NumpyEncoder, indent=4))

        file_sk.close()