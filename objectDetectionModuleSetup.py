import pyzed.sl as sl

# Crear cámara
zed = sl.Camera()
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD720
init_params.depth_mode = sl.DEPTH_MODE.ULTRA

# Set initialization parameters
detection_parameters = sl.ObjectDetectionParameters()
detection_parameters.enable_tracking = True # Objects will keep the same ID between frames
detection_parameters.enable_segmentation = True # Outputs 2D masks over detected objects

# Set runtime parameters
detection_parameters_rt = sl.ObjectDetectionRuntimeParameters()
detection_parameters_rt.detection_confidence_threshold = 25

# Open the camera
err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    # Quit if an error occurred
    exit()

# # choose a detection model
# detection_parameters.detection_model = sl.OBJECT_DETECTION_MODEL.MULTI_CLASS_BOX

if detection_parameters.enable_tracking :
    # Set positional tracking parameters
    positional_tracking_parameters = sl.PositionalTrackingParameters()
    # Enable positional tracking
    zed.enable_positional_tracking(positional_tracking_parameters)

# Enable object detection with initialization parameters
zed_error = zed.enable_object_detection(detection_parameters)
if zed_error != sl.ERROR_CODE.SUCCESS:
    print("enable_object_detection", zed_error, "\nExit program.")
    zed.close()
    exit(-1)