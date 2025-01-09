import sys
import time
import serial
import platform
from core.device.writeFunctions import signalGenerator_write
from core.device.readFunctions import signalGenerator_read
from core.utils.utils import parameters, unit, waveform, channel, amplitude
from logger import test_logger
from core.serialHandler import SerialConnection

def get_serial_port():
    os_name = platform.system()
    if os_name == "Windows":
        return 'COM2'  # Adjust as needed
    elif os_name == "Linux":
        return '/dev/ttyUSB0'  # Adjust as needed
    else:
        raise ValueError(f"Unsupported operating system: {os_name}")


def test_waveforms(signal_gen_write, signal_gen_read, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting waveform tests for Channel={channel_num}")
    for wf in range(17):  # There are 17 waveform types
        if parameters.TEST: test_logger.info(f"Setting waveform: {wf} for Channel={channel_num}")
        
        signal_gen_write.set_waveform(channel_num, wf)
        signal_gen_write.set_channel_enable(channel_num)
        time.sleep(0.5)
        
        signal_gen_write.set_channel_enable()
        time.sleep(0.5)
    
    # Set waveform back to SQUARE after testing all waveforms
    signal_gen_write.set_waveform(channel_num, waveform.SQUARE)
    signal_gen_write.set_channel_enable()
    time.sleep(0.5)
    if parameters.TEST: test_logger.info(f"Set waveform back to SQUARE for Channel={channel_num}")
    if parameters.TEST: test_logger.info(f"Completed waveform tests for Channel={channel_num}\n\n")

def test_frequencies(signal_gen_write, signal_gen_read, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting frequency tests for Channel={channel_num}")
    frequencies = [(1, unit.HZ), (1, unit.KHZ), (1, unit.MHZ)]
    for freq, freq_unit in frequencies:
        signal_gen_write.set_frequency(channel_num, freq, freq_unit)
        signal_gen_write.set_channel_enable(channel_num)
        time.sleep(0.5)
        signal_gen_write.set_channel_enable()
        time.sleep(0.5)
    # Reset frequency to default (1 kHz)
    signal_gen_write.set_frequency(channel_num, 1, unit.KHZ)
    signal_gen_write.set_channel_enable()
    if parameters.TEST: test_logger.info(f"Completed frequency tests for Channel={channel_num}\n\n")

def test_amplitudes(signal_gen_write, signal_gen_read, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting amplitude tests for Channel={channel_num}")
    amplitudes = [(1, amplitude.VOLT), (1, amplitude.MILLIVOLT)]
    for amp, amp_unit in amplitudes:
        signal_gen_write.set_amplitude(channel_num, amp, amp_unit)
        signal_gen_write.set_channel_enable(channel_num)
        time.sleep(0.5)
        signal_gen_write.set_channel_enable()
        time.sleep(0.5)
    # Reset amplitude to default (1 V)
    signal_gen_write.set_amplitude(channel_num, 3.3, amplitude.VOLT)
    signal_gen_write.set_channel_enable()
    if parameters.TEST: test_logger.info(f"Completed amplitude tests for Channel={channel_num}\n\n")

def test_offsets(signal_gen_write, signal_gen_read, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting offset tests for Channel={channel_num}")
    offsets = [(1, amplitude.VOLT), (1, amplitude.MILLIVOLT)]
    for offset, offset_unit in offsets:
        signal_gen_write.set_offset(channel_num, offset, offset_unit)
        signal_gen_write.set_channel_enable(channel_num)
        time.sleep(0.5)
        signal_gen_write.set_channel_enable()
        time.sleep(0.5)
    # Reset offset to default (0 V)
    signal_gen_write.set_offset(channel_num, 0, amplitude.VOLT)
    signal_gen_write.set_channel_enable()
    if parameters.TEST: test_logger.info(f"Completed offset tests for Channel={channel_num}\n\n")

def test_phases(signal_gen_write, signal_gen_read, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting phase tests for Channel={channel_num}")
    phases = [-360, -180, 0, 180, 360]
    for phase in phases:
        signal_gen_write.set_phase(channel_num, phase)
        signal_gen_write.set_channel_enable(channel_num)
        time.sleep(0.5)
        signal_gen_write.set_channel_enable()
        time.sleep(0.5)
    # Reset phase to default (0 degrees)
    signal_gen_write.set_phase(channel_num, 0)
    signal_gen_write.set_channel_enable()
    if parameters.TEST: test_logger.info(f"Completed phase tests for Channel={channel_num}\n\n")

def main():
    # Initialize serial connection
    try:
        serial_port = get_serial_port()
        serial_conn = SerialConnection(serial_port)
        signal_gen_read = signalGenerator_read(serial_conn)
        signal_gen_write = signalGenerator_write(serial_conn)
        print("Serial port opened successfully.")
    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")
        sys.exit(1)

    # Read the serial number
    serial_number = signal_gen_read.getSerialnumber()
    print("Serial Number:", serial_number)

    if not serial_number:
        print("Failed to get serial number. Exiting.")
        sys.exit(1)

    # Test CH1
    print("Testing CH1...")
    if parameters.TEST: test_logger.info("\n\n##### Starting tests for Channel 1 #####\n")
    test_waveforms(signal_gen_write, signal_gen_read, channel.CH1)
    test_frequencies(signal_gen_write, signal_gen_read, channel.CH1)
    test_amplitudes(signal_gen_write, signal_gen_read, channel.CH1)
    test_offsets(signal_gen_write, signal_gen_read, channel.CH1)
    test_phases(signal_gen_write, signal_gen_read, channel.CH1)
    if parameters.TEST: test_logger.info("Completed tests for Channel 1\n\n")

    # Test CH2
    print("Testing CH2...")
    if parameters.TEST: test_logger.info("\n\n##### Starting tests for Channel 2 #####\n")
    test_waveforms(signal_gen_write, signal_gen_read, channel.CH2)
    test_frequencies(signal_gen_write, signal_gen_read, channel.CH2)
    test_amplitudes(signal_gen_write, signal_gen_read, channel.CH2)
    test_offsets(signal_gen_write, signal_gen_read, channel.CH2)
    test_phases(signal_gen_write, signal_gen_read, channel.CH2)
    if parameters.TEST: test_logger.info("Completed tests for Channel 2\n\n")

    if parameters.TEST: test_logger.info("\n\n##### Test finished successfully #####\n\n")

if __name__ == "__main__":
    main()