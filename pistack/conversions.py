"""
    Conversions used for the pi stack to get actual values rather than ADC counts
    Philip Basford
    October 2017
"""

VREF = 3.3  #The reference voltage used in the chip
ADC_MAX = 65535 #The maximum ADC value possible

#Potential divider details for main voltage in
VIN_R1 = 100000
VIN_R2 = 12000

#Details for main current measurement
CIN_SENSE = 0.039
CIN_GAIN = 20

#potentional divider details for 5V powersupply
V5_R1 = 3300
V5_R2 = 3900

#potential divider details for pi PSU
PI_R1 = 2000
PI_R2 = 3000

#details for pi current monitoring circuit
PI_C_SENSE = 0.05
PI_C_R_OUT = 3300

#scale factor for ZXCT1009
ZXCT1009_SF = 100

def convert_vin(reading):
    """
        Convert ADC reading to main input voltage
    """
    return _convert_adc(reading, VIN_R1, VIN_R2)

def convert_cin(reading):
    """
        Convert ADC reading to main current reading
    """
    return round(_adc_to_v(reading) / CIN_GAIN / CIN_SENSE,2 )

def convert_5v(reading):
    """
        Convert ADC reading to 5v measurement
    """
    return _convert_adc(reading, V5_R1, V5_R2)

def convert_pi_v(reading):
    """
        Convert ADC reading to Pi output measurement
    """
    return _convert_adc(reading, PI_R1, PI_R2)

def convert_pi_c(reading):
    """
        Convert the pi output current ADC reading to value
    """
    return round((ZXCT1009_SF * _adc_to_v(reading))/(PI_C_SENSE * PI_C_R_OUT),2)

def convert_power(reading):
    """
        Convert the power reading from the main vin side
    """
    return round(
        reading * pow(VREF, 2) / pow(ADC_MAX, 2) *
        (VIN_R1 + VIN_R2) / VIN_R2 / CIN_SENSE / CIN_GAIN, 2)

def convert_5v_power(reading):
    """
        Convert the power reading from the 5v/pi side
    """
    return round(
        reading * pow(VREF, 2) / pow(ADC_MAX, 2) *
        (V5_R2 + V5_R1) / V5_R2 * ZXCT1009_SF / (PI_C_SENSE * PI_C_R_OUT), 2)

def _convert_adc(adc, res1, res2):
    """
        R1 = the upper of the pair
        R2 = the lower of the pair
    """
    return round(_adc_to_v(adc) * (res1 + res2) / res2,2)

def _adc_to_v(adc):
    """
        Convert an ADC reading the voltage being put into it
    """
    return adc * VREF / ADC_MAX
