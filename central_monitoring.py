from pynput import mouse
import time
import datetime
import cv2
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pynput import keyboard
from pynput.keyboard import Key

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

# trackers for data
keyboard_movements = []
mouse_movements = []
click_movements = []
scroll_movements = []

class CentralMonitoring:
    def press(self, key: Key) -> None:
        """Appends to the keyboard tracker when a key is pressed."""
        try:
            keyboard_movements.append( [key.char, datetime.now().strftime('%Y-%m-%d %H:%M:%S')] )
        except AttributeError:
            keyboard_movements.append( [key, datetime.now().strftime('%Y-%m-%d %H:%M:%S')] )

    def rel(self, key: Key):
        """On escape key press then stop listener."""
        if key == keyboard.Key.esc:
            return False

    def combine_keyboard_strokes(self, filename: str) -> None:
        """Combine all keyboard strokes into text file to make more readable."""
        # check if there is data to be combined
        if not(keyboard_movements):
            with open(filename, "w") as file:
                file.write("No activity recorded.")

        total = []
        only_words = []
        current = ""
        # append to total list to be outputted to txt file
        for character in keyboard_movements:
            if str(type(character[0])) == "<enum 'Key'>":
                total.append([current, character[1]])
                total.append([str(character[0]), character[1]])
                only_words.append(current)
                only_words.append(str(character[0]))
                current = ""
            else:
                current = current + character[0]

        # gets rid of '' that appears after special keys
        final_record = [[keystroke, official_time] for keystroke, official_time in total if keystroke != '']

        # write out keyboard stroke data to txt file and return file as filename
        with open(filename, "w") as file:
            only_words.append("Keystrokes")
            max_len = max(len(word) for word in only_words)
            file.write(f'{"Keystrokes".ljust(max_len)} | Time\n')
            file.write("--------------------------------\n")
            for piece in final_record:
                formatted_line = f"{piece[0].ljust(max_len)} | {piece[1]}\n"
                file.write(formatted_line)

    def move(self, x, y) -> None:
        """Tracks x, y coordinates of mouse."""
        mouse_movements.append((x, y))

    def click(self, x, y, button, pressed) -> None:
        """Tracks x, y coordinates of clicks on screen."""
        click_movements.append((x, y, str(button).split(".")[1]))

    def scroll(self, x, y, dx, dy) -> None:
        """Tracks x, y coordinates of scroll movement on screen"""
        if dy < 0:
            scroll_movements.append((x, y, 'down'))
        else:
            scroll_movements.append((x, y, 'up'))

    def sort_movement_types(self, data: list, label: str) -> tuple:
        """Determines if click was right or left click and sorts accordingly."""
        one = []
        two = []
        for x, y, click_side in data:
            if click_side == label:
                one.append((x,y))
            else:
                two.append((x,y))

        return (one, two)

    def rem_dup(self, data: list) -> list:
        """Duplicates end up in data so removes all duplicates."""
        converted_set = [frozenset(t) for t in data]
        unique_list = list(set(converted_set))
        return [tuple(s) for s in unique_list]

    def plot_movements(self, data: list, flag: str, graph_count: int, exact_time: str, recording_filename: str) -> None:
        """Plots all movement trackers."""

        match flag:
            case "mouse":
                # need to take inverse of y coordinates because of how screen is set up (x and y coordinate wise)
                x_coordinates = [(1 * x) for x,y in data]
                y_coordinates = [(-1 * y) for x,y in data]

                plt.scatter(x_coordinates[1:-1], y_coordinates[1:-1], marker='o', color='blue')
                plt.scatter(x_coordinates[0], y_coordinates[0], marker='o', color='green', label="Start point") # start point
                plt.scatter(x_coordinates[-1], y_coordinates[-1], marker='o', color='red', label='End point') # end point

                plt.xlabel('Horizontal Axis of Screen')
                plt.ylabel('Vertical Axis of Screen')

                plt.title('Mouse Tracking')

                plt.xlim(0, 1440)
                plt.ylim(-900, 0)

                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

                plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: int(abs(x))))

                plt.savefig(f'{recording_filename}/mouse/{graph_count}_mouse_{exact_time}', bbox_inches='tight')

                plt.close()

                plt.clf()

            case "click":
                right, left = self.sort_movement_types(data, "right")

                right_x = [(1 * x) for x,y in right]
                right_y = [(-1 * y) for x,y in right] # its supposed to be y

                left_x = [(1 * x) for x,y in left]
                left_y = [(-1 * y) for x,y in left]

                # right is red
                plt.scatter(right_x, right_y, marker='o', color='red', label="Right Click")
                # left is blue
                plt.scatter(left_x, left_y, marker='o', color='blue', label="Left Click")

                plt.xlabel('Horizontal Axis of Screen')
                plt.ylabel('Vertical Axis of Screen')

                plt.title('Click Tracking')

                plt.xlim(0, 1440)
                plt.ylim(-900, 0)

                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

                plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: int(abs(x))))

                plt.savefig(f'{recording_filename}/mouse/{graph_count}_click_{exact_time}', bbox_inches='tight')

                plt.close()

                plt.clf()

            case "scroll":
                upper, downer = self.sort_movement_types(data, "up")

                up = self.rem_dup(upper)
                down = self.rem_dup(downer)


                up_x = [(1 * x) for x,y in up]
                up_y = [(-1 * y) for x,y in up]

                down_x = [(1 * x) for x,y in down]
                down_y = [(-1 * y) for x,y in down]

                # up is red
                plt.scatter(up_x, up_y, marker='o', color='red', label="Up Scroll")
                # down is blue
                plt.scatter(down_x, down_y, marker='o', color='blue', label="Down Scroll")

                plt.xlabel('Horizontal Axis of Screen')
                plt.ylabel('Vertical Axis of Screen')

                plt.title('Scroll Tracking')

                plt.xlim(0, 1440)
                plt.ylim(-900, 0)

                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

                plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: int(abs(x))))

                plt.savefig(f'{recording_filename}/mouse/{graph_count}_scroll_{exact_time}', bbox_inches='tight')

                plt.close()

                plt.clf()

    def write_camera_error_file(self, error_message: str) -> None:
        """If camera cannot be opened then records error status into txt file."""
        filename = "cam_record.txt"
        with open(filename, "w") as file:
            file.write(f'{error_message}\n')

    def record_stats(self, stat_filename: str, stats_dict: dict, stat_names: str) -> None:
        """Records statistics of mouse clicks, scrolls, and movements."""
        # coordinates:
        # top left: x -> 0-700 | y -> -450 - 0
        # bottom left: x -> 0 - 700 | y -> -450 - -900
        # top right: x -> 700 - 1400 | y -> -450 - 0
        # bottom right: x -> 700 - 1400 | y -> -450 - -900
        new_dict = {"mouse": [], "click": []}

        # need to flip y coordinates because inverted pixel x, y
        for x, y in stats_dict["mouse"]:
            new_dict["mouse"].append((x, (-1 * y)))

        for x, y, mouse_side in stats_dict["click"]:
            new_dict["click"].append((x, (-1 * y)))

        total_stats_dict = {name: {"top_left":0, "bottom_left":0, "top_right":0, "bottom_right":0, "anomaly":0, "total": 0} for name in stat_names}
        # determine where mouse was based off of x, y coordinates (top left, right or bottom left, right)
        for stat in stats_dict:
            total_stats_dict[stat]["total"] = len(new_dict[stat])
            for x, y in new_dict[stat]:

                if (0 < x < 700) and (-450 < y < 0):
                    total_stats_dict[stat]["top_left"] = total_stats_dict[stat]["top_left"] + 1
                elif (0 < x < 700) and (-900 < y < -450):
                    total_stats_dict[stat]["bottom_left"] = total_stats_dict[stat]["bottom_left"] + 1
                elif (700 < x < 1400) and (-450 < y < 0):
                    total_stats_dict[stat]["top_right"] = total_stats_dict[stat]["top_right"] + 1
                elif (700 < x < 1400) and (-900 < y < -450):
                    total_stats_dict[stat]["bottom_right"] = total_stats_dict[stat]["bottom_right"] + 1
                else:
                    total_stats_dict[stat]["anomaly"] = total_stats_dict[stat]["anomaly"] + 1

        # flag is to control whether it is overwriting txt file or appending to it
        mode = "w"
        flag = 0
        # write stats out to txt file
        with open(stat_filename, mode) as file:
            if flag != 0:
                mode = "a"
            for key, value in total_stats_dict.items():
                total = value["total"]
                file.write(f"{key}:\n")

                for sub_key, sub_value in value.items():
                    if sub_key != "total" and sub_key != "anomaly":
                        if total == 0:
                          file.write(f"{sub_key} -> 0%\n")
                        else:
                          file.write(f"{sub_key} -> {round((sub_value / total) * 100, 2)}%\n")

                flag = flag + 1
                file.write("\n")

    def start_recording_keyboard_only(self, monitoring_time: int, filename: str, recording_filename: str, camera_flag: bool) -> None:
        """Starts only keyboard listener."""

        if camera_flag:
          cap = cv2.VideoCapture(0)

        keyboard_listener = KeyboardListener(on_press=self.press, on_release=self.rel)

        # start keyboard, mouse, and camera listeners
        keyboard_listener.start()

        time.sleep(1.5)

        if camera_flag and (not cap.isOpened()):
          self.write_camera_error_file("Error: Could not open camera.")

        image_count = 0
        original_monitoring_time = monitoring_time

        # every 20 seconds start new data collection to reduce clutter when written out to files or graphs
        while monitoring_time >= 0:

            if monitoring_time % 20 == 0 and monitoring_time != original_monitoring_time:
                # get current time and image count for filenames
                current_time = datetime.now().strftime('%Y-%m-%d@%H*%M*%S')
                image_count = image_count + 1

                if camera_flag:
                  ret, frame = cap.read()
                  if not ret:
                      self.write_camera_error_file("Error: Failed to capture frame.")
                  cv2.imwrite(f'{recording_filename}/camera/{image_count}_image_{current_time}.jpg', frame)

            time.sleep(1)
            monitoring_time = monitoring_time - 1

        # stop all listeners and record stats
        if camera_flag:
            cap.release()

        keyboard_listener.stop()
        self.combine_keyboard_strokes(filename)

    def start_recording_mouse_only(self, monitoring_time: int, filename: str, recording_filename: str, camera_flag: bool) -> None:
        """Starts only mouse listener."""

        if camera_flag:
          cap = cv2.VideoCapture(0)

        stats_dict = {"mouse": [], "click": []}
        mouse_listener = MouseListener(on_move=self.move, on_click=self.click, on_scroll=self.scroll)

        # start mouse listener
        mouse_listener.start()

        time.sleep(1.5)

        if camera_flag and (not cap.isOpened()):
          self.write_camera_error_file("Error: Could not open camera.")

        image_count = 0
        graph_count = 0
        original_monitoring_time = monitoring_time

        # every 20 seconds start new data collection to reduce clutter when written out to files or graphs
        while monitoring_time >= 0:

            if monitoring_time % 20 == 0 and monitoring_time != original_monitoring_time:
                # get current time and image count for filenames
                current_time = datetime.now().strftime('%Y-%m-%d@%H*%M*%S')
                image_count = image_count + 1

                if camera_flag:
                  ret, frame = cap.read()
                  if not ret:
                      self.write_camera_error_file("Error: Failed to capture frame.")
                  cv2.imwrite(f'{recording_filename}/camera/{image_count}_image_{current_time}.jpg', frame)

                if mouse_movements:
                    self.plot_movements(mouse_movements, "mouse", graph_count, current_time, recording_filename)
                    stats_dict["mouse"] = stats_dict["mouse"] + mouse_movements
                    mouse_movements.clear()

                if click_movements:
                    self.plot_movements(click_movements, "click", graph_count, current_time, recording_filename)
                    stats_dict["click"] = stats_dict["click"] + click_movements
                    click_movements.clear()

                if scroll_movements:
                    self.plot_movements(scroll_movements, "scroll", graph_count, current_time, recording_filename)
                    scroll_movements.clear()

                graph_count = graph_count + 1

            time.sleep(1)
            monitoring_time = monitoring_time - 1

        # stop all listeners and record stats
        if camera_flag:
            cap.release()

        mouse_listener.stop()

        self.record_stats(f'{recording_filename}/mouse/mouse_movement_statistics.txt', stats_dict, ["mouse", "click"])

    def start_recording_all(self, monitoring_time: int, filename: str, recording_filename: str, camera_flag: bool) -> None:
        """Starts all listeners at the same time."""

        if camera_flag:
          cap = cv2.VideoCapture(0)

        stats_dict = {"mouse": [], "click": []}

        keyboard_listener = KeyboardListener(on_press=self.press, on_release=self.rel)
        mouse_listener = MouseListener(on_move=self.move, on_click=self.click, on_scroll=self.scroll)

        # start keyboard, mouse, and camera listeners
        keyboard_listener.start()
        mouse_listener.start()

        time.sleep(1.5)

        if camera_flag and (not cap.isOpened()):
          self.write_camera_error_file("Error: Could not open camera.")

        image_count = 0
        graph_count = 0
        original_monitoring_time = monitoring_time

        # every 20 seconds start new data collection to reduce clutter when written out to files or graphs
        while monitoring_time >= 0:

            if monitoring_time % 20 == 0 and monitoring_time != original_monitoring_time:
                # get current time and image count for filenames
                current_time = datetime.now().strftime('%Y-%m-%d@%H*%M*%S')
                image_count = image_count + 1

                if camera_flag:
                  ret, frame = cap.read()
                  if not ret:
                      self.write_camera_error_file("Error: Failed to capture frame.")
                  cv2.imwrite(f'{recording_filename}/camera/{image_count}_image_{current_time}.jpg', frame)

                if mouse_movements:
                    self.plot_movements(mouse_movements, "mouse", graph_count, current_time, recording_filename)
                    stats_dict["mouse"] = stats_dict["mouse"] + mouse_movements
                    mouse_movements.clear()

                if click_movements:
                    self.plot_movements(click_movements, "click", graph_count, current_time, recording_filename)
                    stats_dict["click"] = stats_dict["click"] + click_movements
                    click_movements.clear()

                if scroll_movements:
                    self.plot_movements(scroll_movements, "scroll", graph_count, current_time, recording_filename)
                    scroll_movements.clear()

                graph_count = graph_count + 1

            time.sleep(1)
            monitoring_time = monitoring_time - 1

        # stop all listeners and record stats
        if camera_flag:
            cap.release()

        keyboard_listener.stop()
        mouse_listener.stop()

        self.combine_keyboard_strokes(filename)
        self.record_stats(f'{recording_filename}/mouse/mouse_movement_statistics.txt', stats_dict, ["mouse", "click"])

    def start_recording_camera_only(self, monitoring_time: int, filename: str, recording_filename: str, camera_flag: bool) -> None:
        """Starts all listeners at the same time."""

        if camera_flag:
          cap = cv2.VideoCapture(0)

        time.sleep(1.5)

        if camera_flag and (not cap.isOpened()):
          self.write_camera_error_file("Error: Could not open camera.")

        image_count = 0
        graph_count = 0
        original_monitoring_time = monitoring_time

        # every 20 seconds start new data collection to reduce clutter when written out to files or graphs
        while monitoring_time >= 0:

            if monitoring_time % 20 == 0 and monitoring_time != original_monitoring_time:
                # get current time and image count for filenames
                current_time = datetime.now().strftime('%Y-%m-%d@%H*%M*%S')
                image_count = image_count + 1

                if camera_flag:
                  ret, frame = cap.read()
                  if not ret:
                      self.write_camera_error_file("Error: Failed to capture frame.")
                  cv2.imwrite(f'{recording_filename}/camera/{image_count}_image_{current_time}.jpg', frame)

            time.sleep(1)
            monitoring_time = monitoring_time - 1

        # stop all listeners and record stats
        if camera_flag:
            cap.release()
