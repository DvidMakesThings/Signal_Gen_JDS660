import sys
import serial
from core.serialHandler import SerialConnection
from core.utils.utils import channel, unit, amplitude
from core.device.readFunctions import signalGenerator_read
from core.device.writeFunctions import signalGenerator_write

def main():
    try:
        serial_conn = SerialConnection('COM2')  # Adjust 'COM2' as needed
    except serial.SerialException:
        sys.exit(1)

    signal_gen_read = signalGenerator_read(serial_conn)
    signal_gen_write = signalGenerator_write(serial_conn)

    # Read the serial number
    serial_number = signal_gen_read.getSerialnumber()
    print("Serial Number:", serial_number)
    device_type = signal_gen_read.getDevicetype()
    print("Device:", device_type)

    if not serial_number:
        print("Failed to get serial number. Exiting.")
        sys.exit(1)
    
    signal_gen_write.set_offset(channel.CH1, 0, amplitude.VOLT)

if __name__ == '__main__':
    main()