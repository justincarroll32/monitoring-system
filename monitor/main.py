import argparse
from central_monitoring import CentralMonitoring
# https://pypi.org/project/pynput/ --> documentation for listeners

def get_parser():
    """Parser for arguments."""
    parser = argparse.ArgumentParser(description='Monitor specific aspects of users computer.')

    parser.add_argument("-s", '--monitoring_time', help='Monitoring length in seconds in increments of 20.', type=int, required=True)
    parser.add_argument("-f", '--recording_filename', help="Recording filename with current date.", type=str, required=False)
    parser.add_argument("-c", '--record_camera', help="Turn on camera function.", type=int, required=False)
    parser.add_argument("-m", '--record_mouse', help="Turn on only mouse recorder.", type=int, required=False)
    parser.add_argument("-k", '--record_keyboard', help="Turn on keyboard recorder.", type=int, required=False)


    args = parser.parse_args()

    return args.monitoring_time, args.recording_filename, args.record_camera, args.record_mouse, args.record_keyboard

def main():
    """
    Runs all listening objects at once.
    Outputs one large file called 'recording', then 4 sub files that have all data.
    """
    args = get_parser()

    # increments of 20 seconds because graphs get very crowded after 20 seconds and doesn't record as well
    monitoring_time, recording_filename, record_camera, record_mouse, record_keyboard = get_parser()

    # get all flags into boolean values
    record_camera = bool(record_camera) if record_camera is not None else False
    record_mouse = bool(record_mouse) if record_mouse is not None else False
    record_keyboard = bool(record_keyboard) if record_keyboard is not None else False

    print("cameraflag; ", record_camera)
    print("mouseflag: ", record_mouse)
    print("keyboardflag:", record_keyboard)

    if monitoring_time % 20 != 0:
        print("Error: monitoring time is not in an increment of 20.")
        exit()

    filename = f'{recording_filename}/keyboard/keystroke_tracking.txt'
    monitor = CentralMonitoring()

    # start recording

    if record_mouse and record_keyboard:
      monitor.start_recording_all(monitoring_time, filename, recording_filename, record_camera)
    elif record_mouse and not(record_keyboard):
        monitor.start_recording_mouse_only(monitoring_time, filename, recording_filename, record_camera)
    elif not(record_mouse) and record_keyboard:
        monitor.start_recording_keyboard_only(monitoring_time, filename, recording_filename, record_camera)
    elif not(record_mouse) and not(record_keyboard) and record_camera:
        monitor.start_recording_camera_only(monitoring_time, filename, recording_filename, record_camera)
    else:
        print("Error: you have to put items in to record.")
        exit()

    exit()

# example command for MacOS
# python3 main.py -s 20
if __name__ == "__main__":
    main()
