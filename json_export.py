
import pyzed.sl as sl
import ogl_viewer.viewer as gl
import numpy as np
import json

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
    addIntoOutput(out, "local_position_per_joint", body_data.local_position_per_joint)
    addIntoOutput(out, "local_orientation_per_joint", body_data.local_orientation_per_joint)

    return out


def serializeBodies(bodies):
    """Serialize Bodies objects into a JSON like structure"""
    "Esto escribe el json, lo otro no hace nada"

    out = {}
    out["is_new"] = bodies.is_new
    out["is_tracked"] = bodies.is_tracked
    out["timestamp"] = [bodies.timestamp.data_ns]
    out["body_list"] = []

    for sk in bodies.body_list:
        prueba = serializeBodyData(sk)
        out["body_list"].append(serializeBodyData(sk))

        print('Body data serializado: ', prueba)

    return out


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def saveData(bodies):
    skeleton_file_data = {}
    # Save data into JSON file:
    ruta_json = 'D:\\CosasInigo\\GymTar-Proyecto\\bodies.json'
    with open(ruta_json, 'w') as file_sk:
        skeleton_file_data[str(bodies.timestamp.get_milliseconds())] = serializeBodies(bodies)
        print('SkeletonFile: ', skeleton_file_data)

        file_sk = open(ruta_json, 'w')

        file_sk.write(json.dumps(skeleton_file_data, cls=NumpyEncoder, indent=4))

        # json.dump(skeleton_file_data, file_sk, indent=4)

        # file_sk.write('\n')

        # file_sk.write(json.dumps(skeleton_file_data.tolist()))
        # file_sk.flush()
        file_sk.close()



# def saveData(bodies):
#     ruta_json = 'D:\\CosasInigo\\GymTar-Proyecto\\bodies.json'
#
#     try:
#         with open(ruta_json, 'r') as file_sk:
#             skeleton_file_data = json.load(file_sk)
#     except FileNotFoundError:
#         skeleton_file_data = []
#
#     timestamp_ms = int(bodies.timestamp.get_milliseconds())
#     serialized_data = serializeBodies(bodies)
#
#     # Agregar el nuevo dato a la lista usando append()
#     skeleton_file_data.append({
#         "timestamp": timestamp_ms,
#         "data": serialized_data
#     })
#
#     with open(ruta_json, 'w') as file_sk:
#         json.dump(skeleton_file_data, file_sk, cls=NumpyEncoder, indent=4)

