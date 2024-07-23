#!/usr/bin/env bash

FILENAME_CURRENT_DATE="recording_$(date '+%Y-%m-%d_%H-%M-%S')"
OS_NET_INFO="${FILENAME_CURRENT_DATE}/os_network_info"
MONITOR_TIME=$1

# Initialize flags
n_flag=0
c_flag=0
k_flag=0
m_flag=0

if [ -z "$1" ]; then
    echo "usage: ./monitor.sh <monitoring time desired in multiple of 20> <record network flag> <camera_flag either 0 or 1> <record keyboard flag> <record mouse flag>"
    echo "-n : records user network and operating system information into text files."
    echo "-c : turns user camera on and records pictures."
    echo "-k : turns keyboard recorder on."
    echo "-m : turns mouse recorder on."
    exit 1
fi

shift

while getopts ":nckm" opt; do
  case ${opt} in
    n )
      n_flag=1
      ;;
    c )
      c_flag=1
      ;;
    k )
      k_flag=1
      ;;
    m )
      m_flag=1
      ;;
    \? )
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

mkdir ${FILENAME_CURRENT_DATE}

if [ $k_flag -eq 1 ]; then
  mkdir ${FILENAME_CURRENT_DATE}/keyboard
fi

if [ $m_flag -eq 1 ]; then
  mkdir ${FILENAME_CURRENT_DATE}/mouse
fi

if [ $c_flag -eq 1 ]; then
  mkdir ${FILENAME_CURRENT_DATE}/camera
fi

python3 main.py -s $MONITOR_TIME -f ${FILENAME_CURRENT_DATE} -c $c_flag -m $m_flag -k $k_flag

if [ $n_flag -eq 1 ]; then
  mkdir -p "$OS_NET_INFO"
  system_profiler > "$OS_NET_INFO/hardware_software_config.txt"
  sw_vers > "$OS_NET_INFO/os_versions.txt"
  ifconfig > "$OS_NET_INFO/network_config.txt"
fi