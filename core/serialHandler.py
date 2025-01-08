import time
import serial
from core.utils.utils import parameters

class SerialConnection:
    def __init__(self, port):
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            if parameters.DEBUG: print("Serial port opened successfully.")
        except serial.SerialException as e:
            if parameters.DEBUG: print(f"Failed to open serial port: {e}")
            raise

    def send_command(self, command):
        full_command = f"{command}\r\n"
        if parameters.DEBUG: print(f"Sending command: {full_command.strip()}")  # Debug logging
        self.ser.write(full_command.encode())
        time.sleep(0.1)  # Add a small delay to allow the device to process the command
        response = self.ser.read_until(b'\r\n').decode().strip()
        if parameters.DEBUG: print(f"Received response: {response}")  # Debug logging
        return response

    def close(self):
        if self.ser.is_open:
            self.ser.close()
            if parameters.DEBUG: print("Serial port closed.")