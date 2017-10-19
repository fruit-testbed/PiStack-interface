CMD_RESPONSE_OK = 0x00
CMD_RESPONSE_ERROR = 0x01


# Admin commands
CMD_GET_SW_VERSION = 0x02
CMD_GET_HW_VERSION = 0x03
CMD_LEDS_ON = 0x04
CMD_LEDS_OFF = 0x05
CMD_DEBUG_LED = 0x06
CMD_SET_ID_PREFIX = 0x07
CMD_GET_ID_PREFIX = 0x08
CMD_GET_ID = 0x09

#Status commands
CMD_GET_VIN = 0x0A
CMD_GET_CIN = 0x0B
CMD_GET_5V = 0x0C
CMD_GET_PI_V = 0x0D
CMD_GET_PI_C = 0x0E
CMD_GET_PI_HBT = 0x0F
CMD_GET_PI_POWERED = 0x10

# Control commands
CMD_PI_ON = 0x11
CMD_PI_OFF = 0x12
CMD_PI_FORCE_OFF = 0x13


# Command Summary
NO_CMDS = 20

#Maximum ID available on a single string of devices
MAX_ID = 15
# Command indexes
CMD_INDEX = 0 # Byte that contains the command
ADDRESS_INDEX = 1 # Byte the contains the address the CMD is sent to
LENGTH_INDEX = 2 # Byte that contains the length of the command
DATA_START_INDEX = 3 #First byte that contains data

CMD_MIN_LENGTH = 3 # Minimum length = cmd, address, length,  THIS EXCLUDES CRC

CMD_MASTER_ADDRESS = 0xFF

# Command Lengths
CMD_MIN_LENGTHS = [
    0,  #Response so not valid as an input
    0,  #Response so not valid as an input
    CMD_MIN_LENGTH,  #get sw version: cmd, addr, lngth
    CMD_MIN_LENGTH,  #get hw version: cmd, addr, lngth
    CMD_MIN_LENGTH,  #debug leds on: cmd, addr, lngth
    CMD_MIN_LENGTH,  #debug leds off: cmd, addr, lngth
    CMD_MIN_LENGTH + 3, #rgb led: cmr, addr, legnth, r, g, b
    CMD_MIN_LENGTH + 1,  #Set prefix: cmd, addr, lngth, prefix
    CMD_MIN_LENGTH,  #Get prefix: cmd, addr, lngth
    CMD_MIN_LENGTH,  #Get Id: cmd, addr, lngth
    CMD_MIN_LENGTH,  #Get Vin: cmd, addr, lngth
    CMD_MIN_LENGTH,  #Get CIN: cmd, addr, lngth
    CMD_MIN_LENGTH,  #Get 5v: cmd, addr, lngth
    CMD_MIN_LENGTH + 1,  #Get pi 5v: cmd, addr, lngth, id
    CMD_MIN_LENGTH + 1,  #Get pi current: cmd, addr, lngth, id
    CMD_MIN_LENGTH + 1,  #Get pi  heartbeat: cmd, addr, lngth, id
    CMD_MIN_LENGTH,  #Get pi status: cmd, addr, lngth, id
    CMD_MIN_LENGTH,  #Pi on : cmd, addr, lngth, id
    CMD_MIN_LENGTH,  #Pi off : cmd, addr, lngth, id
    CMD_MIN_LENGTH  #Pi force off : cmd, addr, lngth, id
]

RESPONSE_LENGTHS = [
    0,  #Response so not valid as an input
    0,  #Response so not valid as an input
    4,  #get sw version: cmd, addr, lngth, version,
    4,  #get hw version: cmd, addr, lngth, version,
    3,  #debug leds on: cmd, addr, lngth, 
    3,  #debug leds off: cmd, addr, lngth,
    3,  #rgb led off: cmd, addr, lngth, 
    3,  #Set prefix: cmd, addr, lngth, 
    4,  #Get prefix: cmd, addr, lngth, prefix,
    4,  #Get Id: cmd, addr, lngth, id,
    5,  #Get Vin: cmd, addr, lngth, vinH, vinL,
    5,  #Get CIN: cmd, addr, lngth, CinH, CinL,
    5,  #Get 5v: cmd, addr, lngth, 5vH, 5vL,
    5,  #Get pi 5v: cmd, addr, lngth, 5vH, 5vL,
    5,  #Get pi current: cmd, addr, lngth, CH, CL,
    4,  #Get pi  heartbeat: cmd, addr, lngth, status,
    4,  #Get pi status: cmd, addr, lngth, status,
    3,  #Pi  on : cmd, addr, lngth,
    3,  #Pi  off : cmd, addr, lngth,
    3  #Pi  force off : cmd, addr, lngth,
]

