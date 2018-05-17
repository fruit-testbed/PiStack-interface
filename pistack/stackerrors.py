"""
Pi Stack Error Conversions
Philip Basford
May 2018
Provides a mapping between error codes and human descriptions
"""

# Non-error status
_SUCCESS = 0x00
_ERR_CMD_NO_ID_MATCH = 0x02

_BOOT_OK = 0x0F
# Command Processing
_ERR_CMD_TOO_SHORT = 0x10
_ERR_CMD_CRC_FAIL = 0x11
_ERR_CMD_UNKNOWN = 0x12
_ERR_CMD_WRONG_LENGTH = 0x13 #Not enough args for command given
_ERR_INVALID_PI_ID = 0x14
_ERR_CMD_NOT_IMPLEMENTED = 0x15

# Comms
_ERR_COMMS_NOT_READABLE = 0x20
_ERR_COMMS_TOO_LONG = 0x21
_ERR_COMMS_BUFFER_LENGTH_MISMATCH = 0x22
_ERR_COMMS_BUFFER_NOT_LONG_ENGOUGH = 0x23 #cannot fit response in buffer

# Error handling
_ERR_BUFFER_TOO_SMALL_FOR_ERRORS = 0x30

# Storage
_ERR_CONFIG_CRC_FAILURE = 0x40
_ERR_ERRORS_CRC_FAILURE = 0x41
_ERR_IAP_ERASE_PREPARE_FAIL = 0x42
_ERR_IAP_ERASE_FAIL = 0x43
_ERR_IAP_WRITE_PREPARE_FAIL = 0x44
_ERR_IAP_WRITE_FAIL = 0x45
_ERR_IAP_COMPARE_FAIL = 0x46
_ERR_IAP_BLANK_CHECK_FAIL = 0x47

_ERRORS = {}
_ERRORS[_SUCCESS] = "OK"
_ERRORS[_ERR_CMD_NO_ID_MATCH] = "Not a commnd for this ID"
_ERRORS[_BOOT_OK] = "Boot OK"
_ERRORS[_ERR_CMD_TOO_SHORT] = "Command too short"
_ERRORS[_ERR_CMD_CRC_FAIL] = "CRC failed"
_ERRORS[_ERR_CMD_UNKNOWN] = "Command unknown"
_ERRORS[_ERR_CMD_WRONG_LENGTH] = "Wrong number of args"
_ERRORS[_ERR_INVALID_PI_ID] = "Invalid PI ID sent"
_ERRORS[_ERR_CMD_NOT_IMPLEMENTED] = "Command not yet implemented"
_ERRORS[_ERR_COMMS_NOT_READABLE] = "Comms should have been readable but weren't"
_ERRORS[_ERR_COMMS_TOO_LONG] = "Comms too long"
_ERRORS[_ERR_COMMS_BUFFER_LENGTH_MISMATCH] = "Message length longer than buffer containing it"
_ERRORS[_ERR_COMMS_BUFFER_NOT_LONG_ENGOUGH] = "Buffer not long enough for response"
_ERRORS[_ERR_BUFFER_TOO_SMALL_FOR_ERRORS] = "Error buffer is bigger than the comms buffer"
_ERRORS[_ERR_CONFIG_CRC_FAILURE] = "Error loading config from EEPROM"
_ERRORS[_ERR_ERRORS_CRC_FAILURE] = "Error loading error buffer from EEPROM"
_ERRORS[_ERR_IAP_ERASE_PREPARE_FAIL] = "Error preparing block for erasing"
_ERRORS[_ERR_IAP_ERASE_FAIL] = "Failed to perform erase"
_ERRORS[_ERR_IAP_WRITE_PREPARE_FAIL] = "Error preparing block for writing"
_ERRORS[_ERR_IAP_WRITE_FAIL] = "Failed to perform write"
_ERRORS[_ERR_IAP_COMPARE_FAIL] = "IAP comparison failed"
_ERRORS[_ERR_IAP_BLANK_CHECK_FAIL] = "Failed to check if block is blank"

def lookup_error(err):
    """
        Looks up the given error and returns the humand description of it
    """
    return _ERRORS[err]

def lookup_errors(errors):
    """
        Takes a buffer and looksup all all elements in it,
        returning a buffer with the ID code and string descriptions in
    """
    resp = []
    for err in errors:
        resp.append((err, lookup_error(err)))
    return resp

def decode(errors):
    """
        Alias for lookup_errors
    """
    return lookup_errors(errors)
