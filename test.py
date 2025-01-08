import sys
import time
import serial
from JDS import JDS660SignalGenerator
from utils import parameters, unit, waveform, channel, amplitude
from logger import test_logger

def test_waveforms(signal_gen, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting waveform tests for Channel={channel_num}")
    for wf in range(17):  # There are 17 waveform types
        signal_gen.set_waveform(channel_num, wf)
        signal_gen.set_channel_enable(channel_num)
        time.sleep(0.5)
        signal_gen.set_channel_enable()
        time.sleep(0.5)
    # Set waveform back to SQUARE after testing all waveforms
    signal_gen.set_waveform(channel_num, waveform.SQUARE)
    signal_gen.set_channel_enable(channel_num)
    time.sleep(0.5)
    signal_gen.set_channel_enable()
    time.sleep(0.5)
    if parameters.TEST: test_logger.info(f"Set waveform back to SQUARE for Channel={channel_num}")
    if parameters.TEST: test_logger.info(f"Completed waveform tests for Channel={channel_num}\n\n")

def test_frequencies(signal_gen, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting frequency tests for Channel={channel_num}")
    for freq_unit in range(5):  # There are 5 frequency units
        signal_gen.set_frequency(channel_num, 1, freq_unit)
        signal_gen.set_channel_enable(channel_num)
        time.sleep(0.5)
        signal_gen.set_channel_enable()
        time.sleep(0.5)
    # Set frequency back to 1KHz after testing all frequencies
    signal_gen.set_frequency(channel_num, 1, unit.KHZ)
    signal_gen.set_channel_enable(channel_num)
    time.sleep(0.5)
    signal_gen.set_channel_enable()
    time.sleep(0.5)
    if parameters.TEST: test_logger.info(f"Set frequency back to 1KHz for Channel={channel_num}")
    if parameters.TEST: test_logger.info(f"Completed frequency tests for Channel={channel_num}\n\n")

def test_amplitudes(signal_gen, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting amplitude tests for Channel={channel_num}")
    for amp_unit in [amplitude.VOLT, amplitude.MILLIVOLT]:
        signal_gen.set_amplitude(channel_num, 1, amp_unit)
        signal_gen.set_channel_enable(channel_num)
        time.sleep(0.5)
        signal_gen.set_channel_enable()
        time.sleep(0.5)
    # Set amplitude back to 1V after testing all amplitudes
    signal_gen.set_amplitude(channel_num, 1, amplitude.VOLT)
    signal_gen.set_channel_enable(channel_num)
    time.sleep(0.5)
    signal_gen.set_channel_enable()
    time.sleep(0.5)
    if parameters.TEST: test_logger.info(f"Set amplitude back to 1V for Channel={channel_num}")
    if parameters.TEST: test_logger.info(f"Completed amplitude tests for Channel={channel_num}\n\n")

def test_offsets(signal_gen, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting offset tests for Channel={channel_num}")
    for offset_unit in [amplitude.VOLT, amplitude.MILLIVOLT]:
        signal_gen.set_offset(channel_num, 1, offset_unit)
        signal_gen.set_channel_enable(channel_num)
        time.sleep(0.5)
        signal_gen.set_channel_enable()
        time.sleep(0.5)
    # Set offset back to 0V after testing all offsets
    signal_gen.set_offset(channel_num, 0, amplitude.VOLT)
    signal_gen.set_channel_enable(channel_num)
    time.sleep(0.5)
    signal_gen.set_channel_enable()
    time.sleep(0.5)
    if parameters.TEST: test_logger.info(f"Set offset back to 0V for Channel={channel_num}")
    if parameters.TEST: test_logger.info(f"Completed offset tests for Channel={channel_num}\n\n")

def test_phases(signal_gen, channel_num):
    if parameters.TEST: test_logger.info(f"\n\nStarting phase tests for Channel={channel_num}")
    for phase in [-360, -180, 0, 180, 360]:
        signal_gen.set_phase(channel_num, phase)
        signal_gen.set_channel_enable(channel_num)
        time.sleep(0.5)
        signal_gen.set_channel_enable()
        time.sleep(0.5)
    # Set phase back to 0 degrees after testing all phases
    signal_gen.set_phase(channel_num, 0)
    signal_gen.set_channel_enable(channel_num)
    time.sleep(0.5)
    signal_gen.set_channel_enable()
    time.sleep(0.5)
    if parameters.TEST: test_logger.info(f"Set phase back to 0 degrees for Channel={channel_num}")
    if parameters.TEST: test_logger.info(f"Completed phase tests for Channel={channel_num}\n\n")

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

    # Test CH1
    print("Testing CH1...")
    if parameters.TEST: test_logger.info("\n\n##### Starting tests for Channel 1 #####\n")
    test_waveforms(signal_gen, channel.CH1)
    test_frequencies(signal_gen, channel.CH1)
    test_amplitudes(signal_gen, channel.CH1)
    test_offsets(signal_gen, channel.CH1)
    test_phases(signal_gen, channel.CH1)
    if parameters.TEST: test_logger.info("Completed tests for Channel 1\n\n")

    # Test CH2
    print("Testing CH2...")
    if parameters.TEST: test_logger.info("\n\n##### Starting tests for Channel 2 #####\n")
    test_waveforms(signal_gen, channel.CH2)
    test_frequencies(signal_gen, channel.CH2)
    test_amplitudes(signal_gen, channel.CH2)
    test_offsets(signal_gen, channel.CH2)
    test_phases(signal_gen, channel.CH2)
    if parameters.TEST: test_logger.info("Completed tests for Channel 2\n\n")

    if parameters.TEST: test_logger.info("\n\n##### Test finished succesfully #####\n\n")

if __name__ == "__main__":
    main()