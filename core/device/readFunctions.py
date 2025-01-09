import serial
import time
from core.utils.utils import amplitude, channel, unit, waveform, parameters
from core.serialHandler import SerialConnection
from logger import test_logger

class signalGenerator_read:
    def __init__(self, serial_connection):
        self.serial_connection = serial_connection

    def _send_command(self, command):
        return self.serial_connection.send_command(command)

    def getSerialnumber(self) -> str:
        response = self._send_command(':r00=')
        return response.strip()
    
    def getDevicetype(self) -> str:
        response = self._send_command(':r01=')
        return response.strip()

    def get_channel_enable(self) -> tuple[bool, bool]:
        response = self._send_command(':r20=')
        ch1, ch2 = map(int, response.strip().split(','))
        return bool(ch1), bool(ch2)

    def get_waveform(self, channel_num) -> int:
        if channel_num == channel.CH1:
            response = self._send_command(':r21=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r22=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        # Extract the value from the response
        try:
            value = response.split('=')[1].strip().strip('.')
            if parameters.TEST: test_logger.info(f"Response for get_waveform: {response}, Parsed value: {value}")
            return int(value)
        except (IndexError, ValueError):
            raise ValueError("Invalid response format.")

    def get_arbitrary_waveform(self, channel_num) -> int:
        if channel_num == channel.CH1:
            response = self._send_command(':r21=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r22=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        return int(response.strip()) - 100

    def get_frequency(self, channel_num) -> tuple[float, str]:
        if channel_num == channel.CH1:
            response = self._send_command(':r23=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r24=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        # Log the response for debugging
        if parameters.TEST: test_logger.info(f"Response for get_frequency: {response}")
        
        # Parse the response
        try:
            value = response.split('=')[1].strip().strip('.')
            if ',' in value:
                freq, freq_unit = map(int, value.split(','))
            else:
                freq = int(value)
                freq_unit = 0  # Default to Hz if no unit is provided
        except (IndexError, ValueError):
            raise ValueError("Invalid response format.")
        
        # Frequency multiplier
        freq_conversion_factors = (1, 1, 1, 1/1000, 1/1000000)
        freq_units = ["Hz", "KHz", "MHz", "mHz", "uHz"]
        
        # Calculate the frequency value
        frequency = freq * freq_conversion_factors[freq_unit] / 100
        
        return frequency, freq_units[freq_unit]

    def get_amplitude(self, channel_num) -> tuple[float, str]:
        if channel_num == channel.CH1:
            response = self._send_command(':r25=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r26=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        amplitude_value = int(response.strip())
        if amplitude_value >= 1000:
            return amplitude_value / 1000, amplitude.VOLT
        else:
            return amplitude_value, amplitude.MILLIVOLT

    def get_offset(self, channel_num) -> tuple[float, str]:
        if channel_num == channel.CH1:
            response = self._send_command(':r27=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r28=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        offset_value = int(response.strip()) - 1000
        if abs(offset_value) >= 1000:
            return offset_value / 100, amplitude.VOLT
        else:
            return offset_value / 1000, amplitude.MILLIVOLT

    def get_duty_cycle(self, channel_num) -> float:
        if channel_num == channel.CH1:
            response = self._send_command(':r29=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r30=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        return int(response.strip()) / 10

    def get_phase(self, channel_num) -> float:
        if channel_num == channel.CH1:
            response = self._send_command(':r31=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r32=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        phase_value = int(response.strip())
        if phase_value > 3600:
            phase_value -= 3600
        return phase_value / 10