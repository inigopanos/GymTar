import pyzed.sl as sl
import ogl_viewer.viewer as gl
import json_export as json_export
import time

if __name__ == "__main__":

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
    # En 34 hay local_position y local_orientation, en 38 no, PERO en 34 falla la postura de los pies.
    body_tracking_parameters.body_format = sl.BODY_FORMAT.BODY_34
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

    # Contador para tiempo
    contador = 0
    tiempo_total = 100
    tiempo_inicial = time.time()
    tiempo_ejecucion_ejercicio = 30
    tiempo_pausa = 15

    while contador < tiempo_total:
        contador += 1
        time.sleep(1)

        # Ejecutar código durante los 30 segundos del ejercicio
        if contador <= tiempo_ejecucion_ejercicio:

            tiempo_anterior = time.time()
            tiempo_actual = time.time()
            tiempo_transcurrido = tiempo_actual - tiempo_anterior
            contador = tiempo_transcurrido
            # print('Tiempo transcurrido: ', tiempo_transcurrido, 'y contador:', contador)

            for serial in senders:
                zed = senders[serial]
                if zed.grab() == sl.ERROR_CODE.SUCCESS:
                    zed.retrieve_bodies(bodies)

            if fusion.process() == sl.FUSION_ERROR_CODE.SUCCESS and tiempo_transcurrido >= 1:
                # Con 0.5 segundos es igual da 15 datos en vez de 30.
                # Retrieve detected objects
                fusion.retrieve_bodies(bodies, rt)

                json_export.saveData(bodies)  # saveData() convierte skeleton_file_data en {}

                viewer.update_bodies(bodies)

        # Pausa al acabar, en principio 15 segundos
        else:
            print('Pausa...', contador)
            # Una vez llegado al
            if contador >= 45:
                contador = 0

    for sender in senders:
        senders[sender].close()

    viewer.exit()
