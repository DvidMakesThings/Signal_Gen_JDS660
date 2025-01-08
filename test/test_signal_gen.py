import unittest
from unittest.mock import patch, MagicMock
import serial
from JDS import JDS660SignalGenerator
from utils import unit, waveform, channel, amplitude

class TestJDS660SignalGenerator(unittest.TestCase):

    @patch('serial.Serial')
    def setUp(self, mock_serial):
        self.mock_serial_instance = mock_serial.return_value
        self.signal_gen = JDS660SignalGenerator('COM2')

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

    def test_invalid_frequency_unit(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_frequency(channel.CH1, 1, 10)

    def test_invalid_amplitude_unit(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_amplitude(channel.CH1, 1, -1)  # Invalid unit

    def test_invalid_offset_unit(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_offset(channel.CH1, 1, -1)  # Invalid unit

    def test_invalid_phase(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_phase(channel.CH1, 400)

    def test_serial_exception(self):
        with patch('serial.Serial', side_effect=serial.SerialException):
            with self.assertRaises(serial.SerialException):
                JDS660SignalGenerator('COM2')

    def test_command_timeout(self):
        self.mock_serial_instance.read_until.return_value = b''
        response = self.signal_gen._send_command(':r01=')
        self.assertEqual(response, '')

    def test_invalid_frequency_value(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_frequency(channel.CH1, 70000000, unit.HZ)  # Exceeds max frequency

    def test_invalid_offset_value(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_offset(channel.CH1, 10, amplitude.VOLT)  # Exceeds max offset

    def test_invalid_arbitrary_waveform(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_arbitrary_waveform(channel.CH1, 61)  # Exceeds max arbitrary waveform number

    def test_invalid_duty_cycle(self):
        with self.assertRaises(ValueError):
            self.signal_gen.set_duty_cycle(channel.CH1, 110)  # Exceeds max duty cycle

if __name__ == '__main__':
    unittest.main()