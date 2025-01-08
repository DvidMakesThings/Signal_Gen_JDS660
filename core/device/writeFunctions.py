import serial
import time
from core.utils.utils import amplitude, channel, unit, waveform, parameters
from core.serialHandler import SerialConnection
from logger import test_logger

DEBUG = True

class signalGenerator_write:
    def __init__(self, serial_connection):
        self.serial_connection = serial_connection

    def _send_command(self, command):
        return self.serial_connection.send_command(command)

    def set_channel_enable(self, *channels):
        ch1 = 1 if channel.CH1 in channels else 0
        ch2 = 1 if channel.CH2 in channels else 0
        if any(ch not in (channel.CH1, channel.CH2) for ch in channels):
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        if parameters.TEST: test_logger.info(f"Setting channel enable: CH1={ch1}, CH2={ch2}")
        return self._send_command(f':w20={ch1},{ch2}.')

    def set_waveform(self, channel_num, waveform):
        if waveform not in range(17):  # Ensure waveform is valid
            raise ValueError("Invalid waveform. Use a value between 0 and 16.")
        if parameters.TEST: test_logger.info(f"Setting waveform: Channel={channel_num}, Waveform={waveform}")
        if channel_num == channel.CH1:
            command = f':w21={waveform}.'
        elif channel_num == channel.CH2:
            command = f':w22={waveform}.'
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        if parameters.TEST: test_logger.info(f"Sending command: {command}")
        response = self._send_command(command)
        if parameters.TEST: test_logger.info(f"Response for set_waveform: {response}")
        return response

    def set_arbitrary_waveform(self, channel_num, waveform_num):
        if not (1 <= waveform_num <= 60):
            raise ValueError("Invalid arbitrary waveform number. Use a value between 1 and 60.")
        if parameters.TEST: test_logger.info(f"Setting arbitrary waveform: Channel={channel_num}, Waveform Number={waveform_num}")
        if channel_num == channel.CH1:
            return self._send_command(f':w21={100 + waveform_num}.')
        elif channel_num == channel.CH2:
            return self._send_command(f':w22={100 + waveform_num}.')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")

    def set_frequency(self, channel_num, frequency, freq_unit):
        valid_units = [unit.HZ, unit.KHZ, unit.MHZ, unit.MILLI_HZ, unit.MICRO_HZ]
        if freq_unit not in valid_units:
            raise ValueError("Invalid unit. Use unit.HZ, unit.KHZ, unit.MHZ, unit.MILLI_HZ, or unit.MICRO_HZ.")
        
        # Frequency limits
        if freq_unit in [unit.HZ, unit.KHZ, unit.MHZ] and frequency > 60000000:
            raise ValueError("Maximum frequency using unit {} is 60 MHz.".format(freq_unit))
        elif freq_unit == unit.MILLI_HZ and frequency > 80000:
            raise ValueError("Maximum frequency using unit 3 is 80 KHz.")
        elif freq_unit == unit.MICRO_HZ and frequency > 80:
            raise ValueError("Maximum frequency using unit 4 is 80 Hz.")

        # Frequency multiplier
        freq_conversion_factors = (1, 1, 1, 1/1000, 1/1000000)

        # Round to nearest 0.01 value and calculate the frequency value
        freq = int(round(frequency * 100 / freq_conversion_factors[freq_unit]))
        value = f"{freq},{freq_unit}"

        if parameters.TEST: test_logger.info(f"Setting frequency: Channel={channel_num}, Frequency={frequency}, Unit={freq_unit}")
        if channel_num == channel.CH1:
            return self._send_command(f':w23={value}.')
        elif channel_num == channel.CH2:
            return self._send_command(f':w24={value}.')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")

    def set_amplitude(self, channel_num, amplitude_value, amplitude_unit):
        if amplitude_unit not in [amplitude.VOLT, amplitude.MILLIVOLT]:
            raise ValueError("Invalid amplitude unit. Use amplitude.VOLT or amplitude.MILLIVOLT.")
        amplitude_value_converted = amplitude_value * amplitude_unit
        if parameters.TEST: test_logger.info(f"Setting amplitude: Channel={channel_num}, Amplitude Value={amplitude_value}, Amplitude Unit={amplitude_unit}")
        if channel_num == channel.CH1:
            return self._send_command(f':w25={amplitude_value_converted}.')
        elif channel_num == channel.CH2:
            return self._send_command(f':w26={amplitude_value_converted}.')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")

    def set_offset(self, channel_num, offset_value, offset_unit):
        if offset_unit not in [amplitude.VOLT, amplitude.MILLIVOLT]:
            raise ValueError("Invalid offset unit. Use amplitude.VOLT or amplitude.MILLIVOLT.")
        
        # Convert the offset value to volts if necessary
        if offset_unit == amplitude.MILLIVOLT:
            offset_value = offset_value / 1000.0

        # Ensure the range is between -9.99V and 9.99V
        if not (-9.99 <= offset_value <= 9.99):
            raise ValueError("Offset value out of range. Must be between -9.99V and 9.99V.")

        # Map the offset value to the appropriate format
        offset_value_converted = int(round(offset_value * 100)) + 1000

        if parameters.TEST: test_logger.info(f"Setting offset: Channel={channel_num}, Offset Value={offset_value}, Offset Unit={offset_unit}")
        if channel_num == channel.CH1:
            return self._send_command(f':w27={offset_value_converted}.')
        elif channel_num == channel.CH2:
            return self._send_command(f':w28={offset_value_converted}.')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")

    def set_duty_cycle(self, channel_num, duty_cycle):
        if not (0 <= duty_cycle <= 100):
            raise ValueError("Duty cycle out of range. Must be between 0 and 100.")
        duty_cycle_mod = duty_cycle * 10
        if parameters.TEST: test_logger.info(f"Setting duty cycle: Channel={channel_num}, Duty Cycle={duty_cycle}")
        if channel_num == channel.CH1:
            return self._send_command(f':w29={duty_cycle_mod}.')
        elif channel_num == channel.CH2:
            return self._send_command(f':w30={duty_cycle_mod}.')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
    def set_phase(self, channel_num, phase):
        # Ensure the range is between -360 and 360 degrees
        if not (-360 <= phase <= 360):
            raise ValueError("Phase value out of range. Must be between -360 and 360 degrees.")

        # Adjust phase if it is negative
        if phase < 0:
            phase += 360

        # Round to the nearest 0.1 value and convert to the appropriate format
        phase_converted = int(round(phase * 10))

        if parameters.TEST: test_logger.info(f"Setting phase: Channel={channel_num}, Phase={phase}")
        if channel_num == channel.CH1:
            return self._send_command(f':w31={phase_converted}.')
        elif channel_num == channel.CH2:
            return self._send_command(f':w32={phase_converted}.')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")