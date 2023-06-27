# Create a ZED camera object
import pyzed.sl as sl

def main():
    zed = sl.Camera()

    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.camera_fps = 30

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Get camera information (ZED Serial Number)
    zed_serial = zed.get_camera_information().serial_number
    print('Hello! This is my serial number: {0}'.format(zed_serial))

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()