# Signal_Gen_JDS660

This program allows you to control the JDS6600 signal generator from your PC. It provides an easy-to-use interface for configuring and managing signal output parameters such as frequency, amplitude, and waveform type.

## Features

- Set waveform type (e.g., SINE, SQUARE, TRIANGLE)
- Set frequency with various units (Hz, kHz, MHz, etc.)
- Set amplitude with various units (V, mV)
- Set offset with various units (V, mV)
- Set phase
- Enable/disable channels
- Set arbitrary waveforms
- Set duty cycle

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Signal_Gen_JDS660.git
    cd Signal_Gen_JDS660
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Connect your JDS6600 signal generator to your PC via a serial port. Run the main script to start controlling the signal generator:

3. Run the program:
    ```sh
    python main.py
    ```

## Example

Here is an example of how to use the `JDS660SignalGenerator` class to set up a signal:
```python
from JDS import JDS660SignalGenerator
from utils import channel, waveform, unit, amplitude

# Initialize the signal generator
signal_gen = JDS660SignalGenerator('COM2')

# Set waveform to SINE on channel 1
signal_gen.set_waveform(channel.CH1, waveform.SINE)

# Set frequency to 1 kHz on channel 1
signal_gen.set_frequency(channel.CH1, 1, unit.KHZ)

# Set amplitude to 1 V on channel 1
signal_gen.set_amplitude(channel.CH1, 1, amplitude.VOLT)

# Set offset to 0 V on channel 1
signal_gen.set_offset(channel.CH1, 0, amplitude.VOLT)

# Enable channel 1
signal_gen.set_channel_enable(channel.CH1)
```

## Running Tests

To run the tests and check the coverage, use the following commands:

1. Run the tests:
    ```sh
    coverage run -m unittest discover -s test
    ```

2. Generate the coverage report:
    ```sh
    coverage report -m
    ```

## Future Development

- Implement sweep function
- Implement custom waveform generation
- Implement readout functionality

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or feedback:

- Email: s.dvid@hotmail.com
- GitHub: [DvidMakesThings](https://github.com/DvidMakesThings)