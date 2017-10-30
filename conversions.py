VREF = 3.3
ADC_MAX = 65535

VIN_R1 = 100000
VIN_R2 = 12000

V5_R1 = 3300
V5_R2 = 3900

PI_R1 = 2000
PI_R2 = 3000

PI_C_SENSE = 0.05
PI_C_R_OUT = 3300

def convert_vin(reading):
    return _convert_adc(reading, VIN_R1, VIN_R2)

def convert_cin(reading):
    pass

def convert_5v(reading):
    return _convert_adc(reading, V5_R1, V5_R2)

def convert_pi_v(reading):
    return _convert_adc(reading, PI_R1, PI_R2)

def convert_pi_c(reading):
    return (100 * _adc_to_v(reading))/(PI_C_SENSE * PI_C_R_OUT)

def _convert_adc(adc, res1, res2):
    """
        R1 = the upper of the pair
        R2 = the lower of the pair
    """
    return _adc_to_v(adc) * (res1 + res2) / res2

def _adc_to_v(adc):
    """
        Convert an ADC reading the voltage being put into it
    """
    return adc * VREF / ADC_MAX
