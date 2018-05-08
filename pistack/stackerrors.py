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


def lookup_error(err):
    return _ERRORS[err]

def lookup_errors(errors):
    resp = []
    for err in errors:
        resp.append((err, lookup_error(err)))
    return resp

def decode(errors):
    return lookup_errors(errors)
