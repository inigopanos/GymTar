
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
    addIntoOutput(out, "velocity", body_data.velocity)
    addIntoOutput(out, "bounding_box_2d", body_data.bounding_box_2d)
    out["confidence"] = body_data.confidence
    addIntoOutput(out, "bounding_box", body_data.bounding_box)
    addIntoOutput(out, "dimensions", body_data.dimensions)
    addIntoOutput(out, "keypoint_2d", body_data.keypoint_2d)
    addIntoOutput(out, "keypoint", body_data.keypoint)
    addIntoOutput(out, "keypoint_cov", body_data.keypoints_covariance)
    addIntoOutput(out, "head_bounding_box_2d", body_data.head_bounding_box_2d)
    addIntoOutput(out, "head_bounding_box", body_data.head_bounding_box)
    addIntoOutput(out, "head_position", body_data.head_position)
    addIntoOutput(out, "keypoint_confidence", body_data.keypoint_confidence)
    addIntoOutput(out, "local_position_per_joint", body_data.local_position_per_joint)
    addIntoOutput(out, "local_orientation_per_joint", body_data.local_orientation_per_joint)
    addIntoOutput(out, "global_root_orientation", body_data.global_root_orientation)
    return out


def serializeBodies(bodies):
    """Serialize Bodies objects into a JSON like structure"""
    "Esto escribe el json, lo otro no hace nada"

    out = {}
    out["is_new"] = bodies.is_new
    out["is_tracked"] = bodies.is_tracked
    out["timestamp"] = bodies.timestamp.data_ns
    out["body_list"] = []
    out["prueba-json"] = []
    for sk in bodies.body_list:
        prueba = serializeBodyData(sk)
        out["body_list"].append(serializeBodyData(sk))
        # out["prueba-json"].append(prueba.local_position_per_joint)

        print('Body data serializado: ', prueba)

    return out


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def saveData(bodies):
    skeleton_file_data = {}
    skeleton_file_data[str(bodies.timestamp.get_milliseconds())] = serializeBodies(bodies)

    ruta_json = 'D:\\CosasInigo\\GymTar-Proyecto\\bodies.json'
    # Save data into JSON file:
    file_sk = open(ruta_json, 'w')
    file_sk.write(json.dumps(skeleton_file_data, cls=NumpyEncoder, indent=4))
    file_sk.write('\n')
    file_sk.write(json.dumps(skeleton_file_data))
    # print('Skeleton file data: ', skeleton_file_data)
    file_sk.flush()
    file_sk.close()
