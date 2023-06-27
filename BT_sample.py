import pyzed.sl as sl

def main():
    # Create ZED objects
    print('Hola')
    zed = sl.Camera()
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.camera_fps = 30
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        # Quit if an error occurred
        print(err)
        exit()

    # Define the Object Detection module parameters
    obj_param = sl.BodyTrackingParameters()
    # Different model can be chosen, optimizing the runtime or the accuracy
    obj_param.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_FAST
    # run detection for every Camera grab
    obj_param.image_sync = True
    # Enable tracking to detect objects across time and space
    obj_param.enable_tracking = True
    # Optimize the person joints position, requires more computations
    obj_param.enable_body_fitting = True

    # If you want to have object tracking you need to enable positional tracking first
    if obj_param.enable_tracking:
        positional_tracking_param = sl.PositionalTrackingParameters()
        zed.enable_positional_tracking(positional_tracking_param)

    print("Body Tracking: Loading Module...")
    print(type(obj_param), 'Objeto parámetro')

    # err = zed.enable_object_detection(obj_param)
    err = zed.enable_body_tracking(obj_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        zed.close()
        exit(1)

    # Set runtime parameter confidence to 40
    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    obj_runtime_param.detection_confidence_threshold = 40

    objects = sl.Objects()


    runtime_parameters = sl.RuntimeParameters()

    # https://www.stereolabs.com/docs/tutorials/image-capture/
    # Grab new frames and detect objects
    while zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        err = zed.retrieve_objects(objects, obj_runtime_param)
        print('Debug 1', err)

        if objects.is_new:
            # Count the number of objects detected
            obj_array = objects.object_list
            print(str(len(obj_array)) + " Person(s) detected\n")

            if len(obj_array) > 0:
                first_object = objects.object_list[0]
                # Display the 3D keypoint coordinates of the first detected person
                print("\n Keypoint 3D ")
                keypoint = first_object.keypoint
                for it in keypoint:
                    print("    " + str(it))

    # Disable body tracking and close the camera
    zed.disable_body_tracking()
    zed.close()


main()