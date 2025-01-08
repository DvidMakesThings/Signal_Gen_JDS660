import unittest
from unittest.mock import patch, MagicMock
import serial
from core.device.writeFunctions import signalGenerator_write
from core.utils.utils import unit, waveform, channel, amplitude
from core.serialHandler import SerialConnection

class TestJDS660SignalGenerator(unittest.TestCase):

    @patch('core.serialHandler.SerialConnection')
    def setUp(self, mock_serial_connection):
        self.mock_serial_instance = mock_serial_connection.return_value
        self.signal_gen = signalGenerator_write(self.mock_serial_instance)

    def test_waveforms(self):
        for wf in range(17):
            with self.subTest(waveform=wf):
                self.signal_gen.set_waveform(channel.CH1, wf)
                self.signal_gen.set_channel_enable(channel.CH1)
                self.signal_gen.set_channel_enable()
        self.signal_gen.set_waveform(channel.CH1, waveform.SQUARE)
        self.signal_gen.set_channel_enable(channel.CH1)
        self.signal_gen.set_channel_enable()

    def test_frequencies(self):
        for freq_unit in range(5):
            with self.subTest(freq_unit=freq_unit):
                self.signal_gen.set_frequency(channel.CH1, 1, freq_unit)
                self.signal_gen.set_channel_enable(channel.CH1)
                self.signal_gen.set_channel_enable()
        self.signal_gen.set_frequency(channel.CH1, 1, unit.KHZ)
        self.signal_gen.set_channel_enable(channel.CH1)
        self.signal_gen.set_channel_enable()

    def test_amplitudes(self):
        for amp_unit in [amplitude.VOLT, amplitude.MILLIVOLT]:
            with self.subTest(amp_unit=amp_unit):
                self.signal_gen.set_amplitude(channel.CH1, 1, amp_unit)
                self.signal_gen.set_channel_enable(channel.CH1)
                self.signal_gen.set_channel_enable()
        self.signal_gen.set_amplitude(channel.CH1, 1, amplitude.VOLT)
        self.signal_gen.set_channel_enable(channel.CH1)
        self.signal_gen.set_channel_enable()

    def test_offsets(self):
        for offset_unit in [amplitude.VOLT, amplitude.MILLIVOLT]:
            with self.subTest(offset_unit=offset_unit):
                self.signal_gen.set_offset(channel.CH1, 1, offset_unit)
                self.signal_gen.set_channel_enable(channel.CH1)
                self.signal_gen.set_channel_enable()
        self.signal_gen.set_offset(channel.CH1, 0, amplitude.VOLT)
        self.signal_gen.set_channel_enable(channel.CH1)
        self.signal_gen.set_channel_enable()

    def test_phases(self):
        for phase in [-360, -180, 0, 180, 360]:
            with self.subTest(phase=phase):
                self.signal_gen.set_phase(channel.CH1, phase)
                self.signal_gen.set_channel_enable(channel.CH1)
                self.signal_gen.set_channel_enable()
        self.signal_gen.set_phase(channel.CH1, 0)
        self.signal_gen.set_channel_enable(channel.CH1)
        self.signal_gen.set_channel_enable()

    def test_invalid_channel(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_waveform(3, waveform.SQUARE)
        with self.assertRaises(ValueError):
            self.signal_gen.set_frequency(3, 1, unit.KHZ)
        with self.assertRaises(ValueError):
            self.signal_gen.set_amplitude(3, 1, amplitude.VOLT)
        with self.assertRaises(ValueError):
            self.signal_gen.set_offset(3, 1, amplitude.VOLT)
        with self.assertRaises(ValueError):
            self.signal_gen.set_phase(3, 0)

    def test_invalid_waveform(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_waveform(channel.CH1, 100)

    def test_invalid_amplitude_unit(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_amplitude(channel.CH1, 1, -1)  # Invalid unit

    def test_invalid_offset_unit(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_offset(channel.CH1, 1, -1)  # Invalid unit

    def test_invalid_phase(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_phase(channel.CH1, 400)

    @patch('core.serialHandler.SerialConnection.__init__', side_effect=serial.SerialException)
    def test_serial_exception(self, mock_serial_init):
        with self.assertRaises(serial.SerialException):
            SerialConnection('COM2')

    def test_command_timeout(self):
        self.mock_serial_instance.send_command.return_value = ''
        response = self.signal_gen._send_command(':r01=')
        self.assertEqual(response, '')

    def test_invalid_frequency_value(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_frequency(channel.CH1, 70000000, unit.HZ)  # Exceeds max frequency

    def test_invalid_offset_value(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_offset(channel.CH1, 100, amplitude.VOLT)  # Exceeds max offset

    def test_invalid_arbitrary_waveform(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_arbitrary_waveform(channel.CH1, 61)  # Exceeds max arbitrary waveform number

    def test_invalid_duty_cycle(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_duty_cycle(channel.CH1, 110)  # Exceeds max duty cycle

    def test_set_channel_enable(self):
        self.signal_gen.set_channel_enable(channel.CH1)
        self.signal_gen.set_channel_enable(channel.CH2)
        self.signal_gen.set_channel_enable(channel.CH1, channel.CH2)

    def test_set_arbitrary_waveform(self):
        self.signal_gen.set_arbitrary_waveform(channel.CH1, 1)
        self.signal_gen.set_arbitrary_waveform(channel.CH2, 1)

    def test_set_frequency(self):
        self.signal_gen.set_frequency(channel.CH1, 1000, unit.HZ)
        self.signal_gen.set_frequency(channel.CH2, 1000, unit.HZ)

    def test_set_amplitude(self):
        self.signal_gen.set_amplitude(channel.CH1, 1, amplitude.VOLT)
        self.signal_gen.set_amplitude(channel.CH2, 1, amplitude.VOLT)

    def test_set_offset(self):
        self.signal_gen.set_offset(channel.CH1, 0, amplitude.VOLT)
        self.signal_gen.set_offset(channel.CH2, 0, amplitude.VOLT)

    def test_set_phase(self):
        self.signal_gen.set_phase(channel.CH1, 0)
        self.signal_gen.set_phase(channel.CH2, 0)

    def test_set_waveform_invalid(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_waveform(channel.CH1, 17)  # Invalid waveform

    def test_set_arbitrary_waveform_invalid(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_arbitrary_waveform(channel.CH1, 61)  # Invalid arbitrary waveform

    def test_set_channel_enable_invalid(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_channel_enable(3)  # Invalid channel

    def test_set_waveform_valid(self):
        self.signal_gen.set_waveform(channel.CH1, waveform.SQUARE)
        self.signal_gen.set_waveform(channel.CH2, waveform.SINE)

    def test_set_arbitrary_waveform_valid(self):
        self.signal_gen.set_arbitrary_waveform(channel.CH1, 1)
        self.signal_gen.set_arbitrary_waveform(channel.CH2, 1)

    def test_invalid_frequency_unit_3(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_frequency(channel.CH1, 90000, unit.MILLI_HZ)  # Exceeds max frequency for unit 3

    def test_invalid_frequency_unit_4(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_frequency(channel.CH1, 90, unit.MICRO_HZ)  # Exceeds max frequency for unit 4

    def test_invalid_duty_cycle_channel(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_duty_cycle(3, 50)  # Invalid channel

    def test_set_duty_cycle_ch1(self):
        self.signal_gen.set_duty_cycle(channel.CH1, 50)  # Valid duty cycle for CH1

    def test_set_duty_cycle_ch2(self):
        self.signal_gen.set_duty_cycle(channel.CH2, 50)  # Valid duty cycle for CH2
    
    def test_invalid_arbitrary_waveform_channel(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_arbitrary_waveform(3, 1)  # Invalid channel

    def test_invalid_frequency_unit(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_frequency(channel.CH1, 1000, "x")  # Invalid unit
    
    
class TestSerialConnection(unittest.TestCase):

    @patch('serial.Serial')
    def test_serial_connection_init_success(self, mock_serial):
        mock_serial_instance = mock_serial.return_value
        conn = SerialConnection('COM2')
        self.assertTrue(mock_serial_instance.is_open)
        self.assertIsNotNone(conn.ser)

    @patch('serial.Serial', side_effect=serial.SerialException)
    def test_serial_connection_init_failure(self, mock_serial):
        with self.assertRaises(serial.SerialException):
            SerialConnection('COM2')

    @patch('serial.Serial')
    def test_send_command(self, mock_serial):
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.read_until.return_value = b':r01=1234.\r\n'
        conn = SerialConnection('COM2')
        response = conn.send_command(':r01=')
        self.assertEqual(response, ':r01=1234.')

    @patch('serial.Serial')
    def test_send_command_timeout(self, mock_serial):
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.read_until.return_value = b''
        conn = SerialConnection('COM2')
        response = conn.send_command(':r01=')
        self.assertEqual(response, '')

    @patch('serial.Serial')
    def test_close(self, mock_serial):
        mock_serial_instance = mock_serial.return_value
        conn = SerialConnection('COM2')
        conn.close()
        mock_serial_instance.close.assert_called_once()


if __name__ == '__main__': # pragma: no cover
    unittest.main()