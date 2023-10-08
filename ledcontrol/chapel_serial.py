import serial
import time
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger()

global_serial_port = None


def list_ports():
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
    return ports


def serial_send_command(command):
    global global_serial_port
    logger.info(f"Trying to send command: {command}")

    if global_serial_port is None:
        logger.error("Not connected to serial port")
        return
    try:
        global_serial_port.write(command)
        logger.info(f"Command sent: {command}")
    except serial.SerialException:
        logger.error("Port closed, Please reconnect")


def connect_serial(port):
    logger.info(f"Connect to {port}")
    # open serial port
    serial_port = serial.Serial()
    serial_port.port = port
    serial_port.baudrate = 9600
    serial_port.parity = serial.PARITY_NONE
    # serial_port.timeout = 2
    serial_port.dtr = True
    try:
        serial_port.open()
    except PermissionError:
        logger.error("Port already open, Access is denied.")
        return False
    except serial.SerialException:
        logger.error("Device not found, Please check if the device is connected to this com port")
        return False

    # check which port was really used
    logger.info(f"Connected to {serial_port.name}")
    global global_serial_port
    global_serial_port = serial_port
    return global_serial_port


def close_com_port(serial_port):
    global global_serial_port
    serial_port.close()
