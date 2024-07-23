# Monitoring System on MacOS (Python and Bash)

This program records mouse camera snapshots, movement, scrolls, clicks, network information, operating system details, and hardware/software configuration details.

This assumes that you are running on a Mac machine with MacOS and Network, OS, and camera recordings can be toggled to not record.

The main code is written in Python but you can run the code using the provided Bash script "monitor.sh".

You can turn on and off the camera, network, keyboard, and mouse recorders with different flags in your command.
Examples are below.

## Details on what is recorded:
**_NOTES_**:
- All of these metrics are recorded in 20 second increments (ex. if you set the time to be 60 seconds with the camera function
on then it will take 3 pictures and save 3 seperate visualizations of movements but 1 record of Network/OS).

- Network and OS information recording says that it is getting an error, but it still records - disregard.
Additionally, takes about a minute to record this information - program is not broken it is taking some time.

- Undefined behavior on different machines and on external monitors.


**Mouse movement**: visually displays mouse movement on graph.

**Clicks**: shows where user clicks screen with right click(red) and left click(blue) indicators.

**Scrolls**: shows where user scrolled up(red) and down(blue).

**Camera**: takes a picture from user's camera every 20 seconds, program procedes if no camera is detected.

**Network information**: saves user's network information by running.

**Operating system information**: records the product name, product version, and build version.

**Hardware and Software Configuration information**: this will provide the harware and software versions and configurations that are stored on the OS.


## How to Execute:

**_BEFORE_ RUNNING .sh FILES RUN ``` chmod 777 <filename>``` TO CHANGE PERMISSIONS AND THEN RUN USING ```./<filename>```**

Run the setup_monitoring.sh file to install the python dependencies:
```
./setup_monitoring.sh
```

Run the monitor.sh file using any of these example commands:

To run monitoring system with network, camera, keyboard, and mouse recordings enabled::
```
./monitor.sh <how long you want to run it in increments of 20> -c -n -k -m
```

With keyboard, camera, and mouse recordings enabled:
```
./monitor.sh <how long you want to run it in increments of 20> -c -k -m
```

With keyboard and mouse:
```
./monitor.sh <how long you want to run it in increments of 20> -k -m
```

With just mouse:
```
./monitor.sh <how long you want to run it in increments of 20> -m
```

With just keyboard:
```
./monitor.sh <how long you want to run it in increments of 20> -k
```

With just camera:
```
./monitor.sh <how long you want to run it in increments of 20> -c
```

Example that runs for 60 seconds with network, camera, keyboard, and mouse recordings enabled:
```
./monitor.sh 60 -n -c -k -m
```
