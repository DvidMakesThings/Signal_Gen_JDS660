import sys
import time
import serial
from core.serialHandler import SerialConnection
from core.utils.utils import channel, unit, amplitude, waveform
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
    
    signal_gen_write.set_waveform(channel.CH1, waveform.SINE)
    signal_gen_write.set_frequency(channel.CH1, 1, unit.KHZ)
    signal_gen_write.set_amplitude(channel.CH1, 2, amplitude.VOLT)
    signal_gen_write.set_offset(channel.CH1, 1, amplitude.VOLT)
    signal_gen_write.set_duty_cycle(channel.CH1, 25)
    signal_gen_write.set_phase(channel.CH1, 10)
    signal_gen_write.set_channel_enable(channel.CH1)
    
    time.sleep(0.5)
    
    signal_gen_read.get_waveform(channel.CH1)
    signal_gen_read.get_frequency(channel.CH1)
    signal_gen_read.get_amplitude(channel.CH1)
    signal_gen_read.get_offset(channel.CH1)
    signal_gen_read.get_duty_cycle(channel.CH1)
    signal_gen_read.get_phase(channel.CH1)
    signal_gen_read.get_channel_enable()

    time.sleep(5)

    signal_gen_write.set_waveform(channel.CH1, waveform.SQUARE)
    signal_gen_write.set_frequency(channel.CH1, 1, unit.KHZ)
    signal_gen_write.set_amplitude(channel.CH1, 3, amplitude.VOLT)
    signal_gen_write.set_offset(channel.CH1, 0, amplitude.VOLT)
    signal_gen_write.set_duty_cycle(channel.CH1, 50)
    signal_gen_write.set_phase(channel.CH1, 0)
    signal_gen_write.set_channel_enable()
    
    time.sleep(0.5)
    
    signal_gen_read.get_waveform(channel.CH1)
    signal_gen_read.get_frequency(channel.CH1)
    signal_gen_read.get_amplitude(channel.CH1)
    signal_gen_read.get_offset(channel.CH1)
    signal_gen_read.get_duty_cycle(channel.CH1)
    signal_gen_read.get_phase(channel.CH1)
    signal_gen_read.get_channel_enable()
if __name__ == '__main__':
    main()