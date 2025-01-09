import sys
import time
import serial
from core.device.writeFunctions import signalGenerator_write
from core.device.readFunctions import signalGenerator_read
from core.utils.utils import parameters, unit, waveform, channel, amplitude
from logger import test_logger
from core.serialHandler import SerialConnection

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
    
    if parameters.TEST: test_logger.info(f"Completed frequency tests for Channel={channel_num}\n\n")

def test_amplitudes(signal_gen_write, signal_gen_read, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting amplitude tests for Channel={channel_num}")
    
    if parameters.TEST: test_logger.info(f"Completed amplitude tests for Channel={channel_num}\n\n")

def test_offsets(signal_gen_write, signal_gen_read, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting offset tests for Channel={channel_num}")
    
    if parameters.TEST: test_logger.info(f"Completed offset tests for Channel={channel_num}\n\n")

def test_phases(signal_gen_write, signal_gen_read, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting phase tests for Channel={channel_num}")
    
    if parameters.TEST: test_logger.info(f"Completed phase tests for Channel={channel_num}\n\n")

def main():
    # Initialize serial connection
    try:
        serial_conn = SerialConnection('COM2')  # Adjust 'COM2' as needed
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