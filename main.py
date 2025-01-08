import sys
import time
import serial
from JDS import JDS660SignalGenerator
from utils import parameters, unit, waveform, channel, amplitude
from logger import test_logger

def main():
    # Initialize serial connection
    try:
        signal_gen = JDS660SignalGenerator('COM2')  # Adjust 'COM2' as needed
        print("Serial port opened successfully.")
    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")
        sys.exit(1)

    # Read the serial number
    serial_number = signal_gen.get_serial_number()
    print("Serial Number:", serial_number)

    if not serial_number:
        print("Failed to get serial number. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()