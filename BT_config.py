import pyzed.sl as sl


# Set initialization parameters
detection_parameters = sl.BodyTrackingParameters()
detection_parameters.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_ACCURATE
detection_parameters.enable_tracking = True
detection_parameters.enable_body_fitting = True
detection_parameters.body_format = sl.BODY_FORMAT.BODY_34

# Set runtime parameters
detection_parameters_rt = sl.BodyTrackingRuntimeParameters()
detection_parameters_rt.detection_confidence_threshold = 40

zed = sl.Camera()
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD720
init_params.depth_mode = sl.DEPTH_MODE.ULTRA

# Open the camera
err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    # Quit if an error occurred
    exit()

if detection_parameters.enable_tracking:
    # Set positional tracking parameters
    positional_tracking_parameters = sl.PositionalTrackingParameters()
    # Enable positional tracking
    zed.enable_positional_tracking(positional_tracking_parameters)

# Enable body tracking with initialization parameters
zed_error = zed.enable_body_tracking(detection_parameters)
if zed_error != sl.ERROR_CODE.SUCCESS:
    print("enable_body_tracking", zed_error, "\nExit program.")
    zed.close()
    exit(-1)
