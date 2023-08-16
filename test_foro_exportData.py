############################################################################

'''

Ce code prend en entrée le fichier de calibration des caméras et permet de :

- détecter et visualiser le squelette fusionné dans le viewer de Stereolabs

- enregistrer un grand nombre de données des squelettes fusionnés à chaque

  timestamps (position, bounding box, keypoints, ...)

- visualiser en temps réel la position actuelle du squelette (poit rouge)

  ainsi que ses précédentes (trajectoire bleu)

- visualiser en temps réel la Heatmap basée sur la position du squelette

'''

############################################################################


import cv2

import sys

import pyzed.sl as sl

import time

import ogl_viewer.viewer as gl

import numpy as np

import json

import matplotlib.pyplot as plt


#######################################################################

#

# Fonctions permettant l'enregistrement de l'ensemble des données des

# squelettes dans un fichier .json

#

#######################################################################


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

    # addIntoOutput(out, "velocity", body_data.velocity)

    #addIntoOutput(out, "bounding_box_2d", body_data.bounding_box_2d)

    out["confidence"] = body_data.confidence

    #addIntoOutput(out, "bounding_box", body_data.bounding_box)

    # addIntoOutput(out, "dimensions", body_data.dimensions)

    # addIntoOutput(out, "keypoint_2d", body_data.keypoint_2d)

    addIntoOutput(out, "keypoint", body_data.keypoint)

    # addIntoOutput(out, "keypoint_cov", body_data.keypoints_covariance)

    # addIntoOutput(out, "head_bounding_box_2d", body_data.head_bounding_box_2d)

    # addIntoOutput(out, "head_bounding_box", body_data.head_bounding_box)

    # addIntoOutput(out, "head_position", body_data.head_position)

    addIntoOutput(out, "keypoint_confidence", body_data.keypoint_confidence)

    addIntoOutput(out, "local_position_per_joint", body_data.local_position_per_joint)

    addIntoOutput(out, "local_orientation_per_joint", body_data.local_orientation_per_joint)

    # addIntoOutput(out, "global_root_orientation", body_data.global_root_orientation)

    # print(dir(body_data))

    return out


def serializeBodies(bodies):
    """Serialize Bodies objects into a JSON like structure"""

    out = {}

    out["is_new"] = bodies.is_new

    out["is_tracked"] = bodies.is_tracked

    out["timestamp"] = bodies.timestamp.data_ns

    out["body_list"] = []

    for sk in bodies.body_list:
        out["body_list"].append(serializeBodyData(sk))

    return out


class NumpyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return json.JSONEncoder.default(self, obj)


#######################################################################

#

#  Visualisation du déplacement du squelette sur une map 2D

#  et

#  Création d'une HeatMap

#

#######################################################################


def create_visualization():
    global heatmap_data

    global fig

    global heatmap_plot

    '''# Initialiser la fenêtre OpenGL

    viewer = gl.GLViewer()

    viewer.init()'''

    # Créer une figure pour la carte de chaleur

    fig = plt.figure()

    fig.suptitle("Room Visualization")

    ax_heatmap = fig.add_subplot(121)

    ax_heatmap.set_title("Heatmap")

    heatmap_plot = ax_heatmap.imshow(heatmap_data, cmap='hot', origin='lower', extent=[0, ROOM_WIDTH, 0, ROOM_HEIGHT])

    plt.colorbar(heatmap_plot)

    # Créer une figure pour la carte 2D et la trajectoire

    ax_map2d = fig.add_subplot(122)

    ax_map2d.set_title("2D Map")

    ax_map2d.set_xlabel("X")

    ax_map2d.set_ylabel("Y")

    ax_map2d.set_xlim([0, ROOM_WIDTH])

    ax_map2d.set_ylim([0, ROOM_HEIGHT])

    ax_map2d.grid(True)


def update_visualization(positions):
    global heatmap_data

    global fig

    global heatmap_plot

    global previous_positions

    # Mettre à jour la carte de chaleur

    heatmap_data *= 0.95  # Diminuer progressivement les valeurs existantes pour l'effet de fondu

    for x, y in positions:
        heatmap_x = int(x / ROOM_WIDTH * HEATMAP_RESOLUTION)

        heatmap_y = int(y / ROOM_HEIGHT * HEATMAP_RESOLUTION)

        # heatmap_x = int(min(x / ROOM_WIDTH, 1) * HEATMAP_RESOLUTION)

        # heatmap_y = int(min(y / ROOM_HEIGHT, 1) * HEATMAP_RESOLUTION)

        heatmap_data[heatmap_y, heatmap_x] += 1

    # Mettre à jour l'affichage de la carte de chaleur

    heatmap_plot.set_data(heatmap_data)

    plt.pause(0.001)

    # Mettre à jour la carte 2D et la trajectoire

    fig.clf()

    ax_heatmap = fig.add_subplot(121)

    ax_heatmap.set_title("Heatmap")

    heatmap_plot = ax_heatmap.imshow(heatmap_data, cmap='hot', origin='lower', extent=[0, ROOM_WIDTH, 0, ROOM_HEIGHT])

    plt.colorbar(heatmap_plot)

    ax_map2d = fig.add_subplot(122)

    ax_map2d.set_title("2D Map")

    ax_map2d.set_xlabel("X")

    ax_map2d.set_ylabel("Y")

    ax_map2d.set_xlim([0, ROOM_WIDTH])

    ax_map2d.set_ylim([0, ROOM_HEIGHT])

    ax_map2d.grid(True)

    # Trajectoire

    if len(previous_positions) > 0:
        x_coords, y_coords = zip(*previous_positions)

        ax_map2d.plot(x_coords, y_coords, 'b-', label='Trajectory')

    # Position actuelle

    if len(positions) > 0:
        x, y = positions[-1]

        ax_map2d.plot(x, y, 'ro', label='Current Position')

    ax_map2d.legend()

    plt.pause(0.001)


#######################################################################

#

# MAIN

#

#######################################################################


if __name__ == "__main__":

    ruta = 'D:\CosasInigo\ZedCalib\calibration2.json'
    filepath = ruta
    fusion_configurations = sl.read_fusion_configuration_file(filepath, sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP,
                                                              sl.UNIT.METER)

    if len(fusion_configurations) <= 0:
        print("Invalid file.")

        exit(1)

    senders = {}

    network_senders = {}

    # common parameters

    init_params = sl.InitParameters()

    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

    init_params.coordinate_units = sl.UNIT.METER

    init_params.depth_mode = sl.DEPTH_MODE.ULTRA

    init_params.camera_resolution = sl.RESOLUTION.HD720

    communication_parameters = sl.CommunicationParameters()

    communication_parameters.set_for_shared_memory()

    positional_tracking_parameters = sl.PositionalTrackingParameters()

    positional_tracking_parameters.set_as_static = True

    body_tracking_parameters = sl.BodyTrackingParameters()

    body_tracking_parameters.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_ACCURATE

    body_tracking_parameters.body_format = sl.BODY_FORMAT.BODY_18

    body_tracking_parameters.enable_body_fitting = False

    body_tracking_parameters.enable_tracking = False

    for conf in fusion_configurations:

        print("Try to open ZED", conf.serial_number)

        init_params.input = sl.InputType()

        # network cameras are already running, or so they should

        if conf.communication_parameters.comm_type == sl.COMM_TYPE.LOCAL_NETWORK:

            network_senders[conf.serial_number] = conf.serial_number



        # local camera needs to be run form here, in the same process than the fusion

        else:

            init_params.input = conf.input_type

            senders[conf.serial_number] = sl.Camera()

            init_params.set_from_serial_number(conf.serial_number)

            status = senders[conf.serial_number].open(init_params)

            if status != sl.ERROR_CODE.SUCCESS:
                print("Error opening the camera", conf.serial_number, status)

                del senders[conf.serial_number]

                continue

            status = senders[conf.serial_number].enable_positional_tracking(positional_tracking_parameters)

            if status != sl.ERROR_CODE.SUCCESS:
                print("Error enabling the positional tracking of camera", conf.serial_number)

                del senders[conf.serial_number]

                continue

            status = senders[conf.serial_number].enable_body_tracking(body_tracking_parameters)

            if status != sl.ERROR_CODE.SUCCESS:
                print("Error enabling the body tracking of camera", conf.serial_number)

                del senders[conf.serial_number]

                continue

            senders[conf.serial_number].start_publishing(communication_parameters)

        print("Camera", conf.serial_number, "is open")

    if len(senders) + len(network_senders) < 1:
        print("No enough cameras")

        exit(1)

    print("Senders started, running the fusion...")

    init_fusion_parameters = sl.InitFusionParameters()

    init_fusion_parameters.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

    init_fusion_parameters.coordinate_units = sl.UNIT.METER

    init_fusion_parameters.output_performance_metrics = False

    init_fusion_parameters.verbose = True

    communication_parameters = sl.CommunicationParameters()

    fusion = sl.Fusion()

    camera_identifiers = []

    fusion.init(init_fusion_parameters)

    print("Cameras in this configuration : ", len(fusion_configurations))

    # warmup

    bodies = sl.Bodies()

    for serial in senders:

        zed = senders[serial]

        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_bodies(bodies)

            # print(bodies)

    for i in range(0, len(fusion_configurations)):

        conf = fusion_configurations[i]

        uuid = sl.CameraIdentifier()

        uuid.serial_number = conf.serial_number

        print("Subscribing to", conf.serial_number, conf.communication_parameters.comm_type)

        status = fusion.subscribe(uuid, conf.communication_parameters, conf.pose)

        if status != sl.FUSION_ERROR_CODE.SUCCESS:

            print("Unable to subscribe to", uuid.serial_number, status)

        else:

            camera_identifiers.append(uuid)

            print("Subscribed.")

    if len(camera_identifiers) <= 0:
        print("No camera connected.")

        exit(1)

    body_tracking_fusion_params = sl.BodyTrackingFusionParameters()

    body_tracking_fusion_params.enable_tracking = True

    body_tracking_fusion_params.enable_body_fitting = False

    fusion.enable_body_tracking(body_tracking_fusion_params)

    rt = sl.BodyTrackingFusionRuntimeParameters()

    rt.skeleton_minimum_allowed_keypoints = 7

    viewer = gl.GLViewer()

    viewer.init()

    # Create ZED objects filled in the main loop

    bodies = sl.Bodies()

    single_bodies = [sl.Bodies]

    # Dimensions de la pièce (à adapter selon votre cas)

    ROOM_WIDTH = 10  # Largeur de la pièce en mètres

    ROOM_HEIGHT = 10  # Hauteur de la pièce en mètres

    # Résolution de la carte de chaleur

    HEATMAP_RESOLUTION = 10000  # Nombre de points en x et y pour la carte de chaleur

    # Initialiser la carte de chaleur

    heatmap_data = np.zeros((HEATMAP_RESOLUTION, HEATMAP_RESOLUTION))

    # Positions précédentes pour la trajectoire

    previous_positions = []

    positions = []

    # Initialiser le visualiseur

    # create_visualization()

    while (viewer.is_available()):

        for serial in senders:

            zed = senders[serial]

            if zed.grab() == sl.ERROR_CODE.SUCCESS:
                zed.retrieve_bodies(bodies)

        if fusion.process() == sl.FUSION_ERROR_CODE.SUCCESS:

            print('Fusion Code Success')

            # Retrieve detected objects

            fusion.retrieve_bodies(bodies, rt)

            # for debug, you can retrieve the data send by each camera, as well as communication and process stat just to make sure everything is okay

            # for cam in camera_identifiers:

            #     fusion.retrieveBodies(single_bodies, rt, cam);

            if bodies.is_new:
                body_array = bodies.body_list

                print(str(len(body_array)) + " Person(s) detected\n")

            skeleton_file_data = {}

            contador = 0

            while (viewer.is_available()):

                if zed.grab() == sl.ERROR_CODE.SUCCESS and contador <= 50:

                    contador += 1

                    zed.retrieve_bodies(bodies)

                    # enregistrement des données du squelette en fichier json

                    skeleton_file_data[str(bodies.timestamp.get_milliseconds())] = serializeBodies(bodies)

                    print('Skeleton file data: ', skeleton_file_data)

                    if contador == 50:

                        file_sk = open("bodies.json", 'w')

                        json.dump(skeleton_file_data, sort_keys=True, indent=4)

                        file_sk.close()

                    # permet de voir le squelette dans le viewer

                    viewer.update_bodies(bodies)

                    # Récupération des données de positions pour la map2D et la HeatMap

                    positions = []

                    for sk in bodies.body_list:
                        x = abs(sk.position[0])  # Coordonnée X du squelette

                        y = abs(sk.position[2])  # Coordonnée Y du squelette

                        positions.append((x, y))

                        # print(positions)

                    # Ajouter les positions précédentes à la trajectoire

                    previous_positions.extend(positions)

                    """# Limiter la taille de la trajectoire

                    if len(previous_positions) > 100:

                        previous_positions = previous_positions[-100:]"""

            break


            # Save data into JSON file:


            file_sk = open("bodies.json", 'w')

            file_sk.write(json.dumps(skeleton_file_data))

            print('Se ha escrito data en bodies.json', skeleton_file_data)

            file_sk.close()

            viewer.update_bodies(bodies)

    for sender in senders:
        senders[sender].close()

    viewer.exit()