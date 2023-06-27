import cv2
import sys
import pyzed.sl as sl
import time
import ogl_viewer.viewer as gl
import numpy as np
import json

if __name__ == "__main__":

    # if len(sys.argv) < 2:
    #     print(sys.argv)
    #     print("This sample display the fused body tracking of multiple cameras.")
    #     print("It needs a Localization file in input. Generate it with ZED 360.")
    #     print("The cameras can either be plugged to your devices, or already running on the local network.")
    #     exit(1)

    ruta = 'D:\CosasInigo\ZedCalib\calibration.json'
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


    def addIntoOutput(out, identifier, tab):
        out[identifier] = []
        for element in tab:
            out[identifier].append(element)
        return out


    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
           if isinstance(obj, np.ndarray):
              return obj.tolist()
           return json.JSONEncoder.default(self, obj)

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
        out = {}
        out["is_new"] = bodies.is_new
        out["is_tracked"] = bodies.is_tracked
        out["timestamp"] = bodies.timestamp.data_ns
        out["body_list"] = []
        for sk in bodies.body_list:
            out["body_list"].append(serializeBodyData(sk))
        return out

    # warmup
    bodies = sl.Bodies()
    for serial in senders:
        zed = senders[serial]
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_bodies(bodies)

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

    camera_info = zed.get_camera_information()

    rt = sl.BodyTrackingFusionRuntimeParameters()
    rt.skeleton_minimum_allowed_keypoints = 7



    viewer = gl.GLViewer()
    viewer.init()

    # Create ZED objects filled in the main loopnntie
    bodies = sl.Bodies()
    single_bodies = [sl.Bodies]

    while (viewer.is_available()):
        for serial in senders:
            zed = senders[serial]
            if zed.grab() == sl.ERROR_CODE.SUCCESS:
                zed.retrieve_bodies(bodies)

        if fusion.process() == sl.FUSION_ERROR_CODE.SUCCESS:
            # Retrieve detected objects
            fusion.retrieve_bodies(bodies, rt)
            # for debug, you can retrieve the data send by each camera, as well as communication and process stat just to make sure everything is okay
            # for cam in camera_identifiers:
            #     fusion.retrieve_bodies(bodies, rt, cam)

            skeleton_file_data = {}
            if zed.grab() == sl.ERROR_CODE.SUCCESS:
                zed.retrieve_bodies(bodies)
                skeleton_file_data[str(bodies.timestamp.get_milliseconds())] = serializeBodies(bodies)
                viewer.update_bodies(bodies)

            viewer.update_bodies(bodies)

    # Save data into JSON file:
    file_sk = open("bodies.json", 'w')
    file_sk.write(json.dumps(skeleton_file_data, cls=NumpyEncoder, indent=4))
    file_sk.close()

    for sender in senders:
        senders[sender].close()

    viewer.exit()