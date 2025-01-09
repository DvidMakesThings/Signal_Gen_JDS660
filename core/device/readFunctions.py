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
    
    def _parse_response(self, response: str) -> float:
        try:
            value = response.split('=')[1].strip().strip('.').replace(',', '.')
            return float(value)
        except (IndexError, ValueError):
            raise ValueError("Invalid response format.")

    def getSerialnumber(self) -> str:
        response = self._send_command(':r00=')
        return response.strip()
    
    def getDevicetype(self) -> str:
        response = self._send_command(':r01=')
        return response.strip()

    def get_channel_enable(self) -> str:
        response = self._send_command(':r20=')
        
        # Log the response for debugging
        if parameters.DEBUG: print(f"Response for get_channel_enable: {response}")
        if parameters.TEST: test_logger.info(f"Response for get_channel_enable: {response}")
        
        # Parse the response
        try:
            values = response.split('=')[1].strip().strip('.').split(',')
            ch1_enable = int(values[0])
            ch2_enable = int(values[1])
        except (IndexError, ValueError):
            raise ValueError("Invalid response format.")
        
        ch1_status = "CH1 - ON" if ch1_enable else "CH1 - OFF"
        ch2_status = "CH2 - ON" if ch2_enable else "CH2 - OFF"
        
        if parameters.DEBUG: print(f"{ch1_status},\n{ch2_status}")
        if parameters.TEST: test_logger.info(f"{ch1_status}, {ch2_status}")
        
        return response

    def get_waveform(self, channel_num) -> str:
        if channel_num == channel.CH1:
            response = self._send_command(':r21=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r22=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        # Log the response for debugging
        if parameters.DEBUG: print(f"Response for get_waveform: {response}")
        if parameters.TEST: test_logger.info(f"Response for get_waveform: {response}")
        
        # Parse the response
        waveform_value = self._parse_response(response)
        
        # Mapping of waveform types to their names
        waveform_types = {
            0: "SINE",
            1: "SQUARE",
            2: "PULSE",
            3: "TRIANGLE",
            4: "PARTIAL_SINE",
            5: "CMOS",
            6: "DC",
            7: "HALF_WAVE",
            8: "FULL_WAVE",
            9: "POS_LADER",
            10: "NEG_LADER",
            11: "NOISE",
            12: "EXP_RISE",
            13: "EXP_DECAY",
            14: "MULTI_TONE",
            15: "SINC",
            16: "LORENZ"
        }
        
        waveform_name = waveform_types.get(waveform_value, "UNKNOWN")
        
        if parameters.DEBUG: print(f"Waveform value: {waveform_name}")
        if parameters.TEST: test_logger.info(f"Waveform value: {waveform_name}")
        
        return response

    def get_arbitrary_waveform(self, channel_num) -> str:
        if channel_num == channel.CH1:
            response = self._send_command(':r33=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r34=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        # Log the response for debugging
        if parameters.DEBUG: print(f"Response for get_arbitrary_waveform: {response}")
        if parameters.TEST: test_logger.info(f"Response for get_arbitrary_waveform: {response}")
        
        # Parse the response
        arbitrary_waveform_value = self._parse_response(response)
        
        if parameters.DEBUG: print(f"Arbitrary waveform value: {arbitrary_waveform_value}")
        if parameters.TEST: test_logger.info(f"Arbitrary waveform value: {arbitrary_waveform_value}")
        
        return response

    def get_frequency(self, channel_num) -> str:
        if channel_num == channel.CH1:
            response = self._send_command(':r23=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r24=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        # Log the response for debugging
        if parameters.DEBUG: print(f"Response for get_frequency: {response}")
        if parameters.TEST: test_logger.info(f"Response for get_frequency: {response}")
        
        # Parse the response
        frequency_value = self._parse_response(response)
        
        if frequency_value >= 1000000:
            frequency_value /= 1000000
            unit = "MHz"
        elif frequency_value >= 1000:
            frequency_value /= 1000
            unit = "kHz"
        else:
            unit = "Hz"
        
        if parameters.DEBUG: print(f"Frequency value: {frequency_value} {unit}")
        if parameters.TEST: test_logger.info(f"Frequency value: {frequency_value} {unit}")
        
        return response

    def get_amplitude(self, channel_num) -> str:
        if channel_num == channel.CH1:
            response = self._send_command(':r25=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r26=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        # Log the response for debugging
        if parameters.DEBUG: print(f"Response for get_amplitude: {response}")
        if parameters.TEST: test_logger.info(f"Response for get_amplitude: {response}")
        
        # Parse the response
        amplitude_value = self._parse_response(response)
        
        if amplitude_value >= 1000:
            amplitude_value = amplitude_value / 1000
            unit = amplitude.VOLT
        else:
            unit = amplitude.MILLIVOLT
        
        if unit == amplitude.VOLT:
            if parameters.DEBUG: print(f"Amplitude value: {amplitude_value} V")
            if parameters.TEST: test_logger.info(f"Amplitude value: {amplitude_value} V")
        else:
            if parameters.DEBUG: print(f"Amplitude value: {amplitude_value} mV")
            if parameters.TEST: test_logger.info(f"Amplitude value: {amplitude_value} mV")
        
        return response

    def get_offset(self, channel_num) -> str:
        if channel_num == channel.CH1:
            response = self._send_command(':r27=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r28=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        # Log the response for debugging
        if parameters.DEBUG: print(f"Response for get_offset: {response}")
        if parameters.TEST: test_logger.info(f"Response for get_offset: {response}")
        
        # Parse the response
        offset_value = self._parse_response(response)
        
        offset_value = (offset_value - 1000) / 100.0
        
        if abs(offset_value) >= 1:
            unit = amplitude.VOLT
        else:
            unit = amplitude.MILLIVOLT
        
        if unit == amplitude.VOLT:
            if parameters.DEBUG: print(f"Offset value: {offset_value} V")
            if parameters.TEST: test_logger.info(f"Offset value: {offset_value} V")
        else:
            if parameters.DEBUG: print(f"Offset value: {offset_value * 1000} mV")
            if parameters.TEST: test_logger.info(f"Offset value: {offset_value * 1000} mV")
        
        return response

    def get_duty_cycle(self, channel_num) -> str:
        if channel_num == channel.CH1:
            response = self._send_command(':r29=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r30=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        # Log the response for debugging
        if parameters.DEBUG: print(f"Response for get_duty_cycle: {response}")
        if parameters.TEST: test_logger.info(f"Response for get_duty_cycle: {response}")
        
        # Parse the response
        duty_cycle = self._parse_response(response) / 10.0
        
        if parameters.DEBUG: print(f"Duty cycle value: {duty_cycle}%")
        if parameters.TEST: test_logger.info(f"Duty cycle value: {duty_cycle}%")
        
        return response

    def get_phase(self, channel_num) -> str:
        if channel_num == channel.CH1:
            response = self._send_command(':r31=')
        elif channel_num == channel.CH2:
            response = self._send_command(':r32=')
        else:
            raise ValueError("Invalid channel. Use channel.CH1 or channel.CH2.")
        
        # Log the response for debugging
        if parameters.DEBUG: print(f"Response for get_phase: {response}")
        if parameters.TEST: test_logger.info(f"Response for get_phase: {response}")
        
        # Parse the response
        phase_value = self._parse_response(response)
        
        if phase_value > 3600:
            phase_value -= 3600
        
        phase_value = phase_value / 10.0
        
        if parameters.DEBUG: print(f"Phase value: {phase_value} deg")
        if parameters.TEST: test_logger.info(f"Phase value: {phase_value} deg")
        
        return response