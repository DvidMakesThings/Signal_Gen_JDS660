class parameters:
    DEBUG = True
    TEST = True

class device:
    DEVICETYPE=0
    SERIALNUMBER=1

class channel:
    # Channel numbers
    CH1 = 1
    CH2 = 2

class amplitude:
    # Amplitude units
    VOLT = 1000
    MILLIVOLT = 1

class unit:
    # Frequency units
    HZ = 1
    KHZ = 1000
    MHZ = 1000000

class waveform:
    # Waveform types
    SINE = 0
    SQUARE = 1
    PULSE = 2
    TRIANGLE = 3
    PARTIAL_SINE = 4
    CMOS = 5
    DC = 6
    HALF_WAVE = 7
    FULL_WAVE = 8
    POS_LADER = 9
    NEG_LADER = 10
    NOISE = 11
    EXP_RISE = 12
    EXP_DECAY = 13
    MULTI_TONE = 14
    SINC = 15
    LORENZ = 16
