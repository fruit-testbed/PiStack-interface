"""
    Interface to the serial interface used on the Pi Stack
    Philip Basford
    October 2017
"""
from time import sleep

from serial import Serial

from commands import *

from errors import (
    InvalidCommandError, CrcFailureError, NoResponseError, InvalidPiError,
    InvalidResponseAddressError, InvalidPrefixError, ResponseLengthWrongError
    )
from crc import calculate_crc_block as calc_crc

DEFAULT_BAUD = 9600
DEFAULT_TIMEOUT = 0.1

DEFAULT_ID = 0

RESPONSE_WAIT_TIME = 0.3

class Comms(object):
    """
        Handle all comms over the serial link
    """
    def __init__(self, port_name, baud=DEFAULT_BAUD, timeout=DEFAULT_TIMEOUT):
        self.port_name = port_name
        self.baudrate = baud
        self.timeout = timeout
        self.serial = Serial(self.port_name, timeout=self.timeout, baudrate=self.baudrate)

    def _send_cmd(self, cmd, dev_id, args=None):
        """
            Handles the actual process of sending a command and recieving a response.
            All methods that commnicate with the stack make use of this
        """
        if cmd > NO_CMDS:   #Command is not known about
            raise InvalidCommandError()
        data = [cmd, dev_id, CMD_MIN_LENGTHS[cmd]] #Convert the inputsinto an array to send
        if args is not None:    #if there are arugments to the call add them onto the existing array
            data.extend(args)
        crc = calc_crc(data)    #work out the crc
        data.append(crc)        #and append it
        print(data)
        self.serial.reset_input_buffer()
        self.serial.write(data)
        sleep(RESPONSE_WAIT_TIME)
        resp = self.serial.readall()
        if len(resp) == 0:
            raise NoResponseError()
        device_output = []
        for chrtr in resp:
            device_output.append(chrtr)
        print(device_output)
        crc = calc_crc(device_output[:-1])
        if len(device_output) < CMD_RESP_MIN_LENGTH:
            raise ResponseLengthWrongError()
        if device_output[-1] != crc:
            print(device_output)
            raise CrcFailureError()
        if device_output[LENGTH_INDEX] < RESPONSE_LENGTHS[cmd]:
            print("%d %d" %(device_output[LENGTH_INDEX], RESPONSE_LENGTHS[cmd]))
            raise ResponseLengthWrongError()
        if device_output[ADDRESS_INDEX] != CMD_MASTER_ADDRESS:
            raise InvalidResponseAddressError()
        success = (device_output[CMD_INDEX] == CMD_RESPONSE_OK)
        return (success, device_output[DATA_START_INDEX:-1])

    def leds_off(self, dev_id=DEFAULT_ID):
        return self._send_cmd(CMD_LEDS_OFF, dev_id)[0]

    def leds_on(self, dev_id=DEFAULT_ID):
        return self._send_cmd(CMD_LEDS_ON, dev_id)[0]

    def rgb_led(self, dev_id, red, green, blue):
        return self._send_cmd(CMD_DEBUG_LED, dev_id, [red, green, blue])[0]

    def get_sw_version(self, dev_id=DEFAULT_ID):
        (success, data) = self._send_cmd(CMD_GET_SW_VERSION, dev_id)
        return (success, data[0])

    def get_hw_version(self, dev_id=DEFAULT_ID):
        (success, data) = self._send_cmd(CMD_GET_HW_VERSION, dev_id)
        return (success, data[0])

    def set_id_prefix(self, dev_id, prefix):
        """
            The ID conists to 2 parts, the lower 4 bits are set using the dip switches.
            The higher 4 bits are set using this command.
            WARNING: This is not yet persistent in the PiStack board
        """
        if prefix & 0x0F:
            raise InvalidPrefixError()
        return self._send_cmd(CMD_SET_ID_PREFIX, dev_id, [prefix])[0]

    def get_id_prefix(self, dev_id=DEFAULT_ID):
        (success, data) = self._send_cmd(CMD_GET_ID_PREFIX, dev_id)
        return (success, data[0])

    def get_id(self, dev_id=DEFAULT_ID):
        (success, data) = self._send_cmd(CMD_GET_ID, dev_id)
        return (success, data[0])

    def get_vin(self, dev_id=DEFAULT_ID):
        (success, data) = self._send_cmd(CMD_GET_VIN, dev_id)
        if success:
            return (success, (data[0] << 8 | data[1]))
        return (success, None)

    def get_cin(self, dev_id=DEFAULT_ID):
        (success, data) = self._send_cmd(CMD_GET_CIN, dev_id)
        if success:
            return (success, (data[0] << 8 | data[1]))
        return (success, None)


    def get_5v(self, dev_id=DEFAULT_ID):
        (success, data) = self._send_cmd(CMD_GET_5V, dev_id)
        if success:
            return (success, (data[0] << 8 | data[1]))
        return (success, None)

    def get_pi_v(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        (success, data) = self._send_cmd(CMD_GET_PI_V, dev_id, [pi_id])
        if success:
            return (success, (data[0] << 8 | data[1]))
        return (success, None)

    def get_pi_c(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        (success, data) = self._send_cmd(CMD_GET_PI_C, dev_id, [pi_id])
        if success:
            return (success, (data[0] << 8 | data[1]))
        return (success, None)

    def get_pi_hbt(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        (success, data) = self._send_cmd(CMD_GET_PI_HBT, dev_id, [pi_id])
        if success:
            return (success, data[0] == 1)
        return (success, None)

    def get_pi_powered(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        (success, data) = self._send_cmd(CMD_GET_PI_POWERED, dev_id, [pi_id])
        if success:
            return (success, data[0] == 1)
        return (success, None)

    def pi_on(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        return self._send_cmd(CMD_PI_ON, dev_id, [pi_id])[0]

    def pi_off(self, dev_id, pi_id, force=False):
        validate_pi_id(pi_id)
        if force:
            return self._send_cmd(CMD_PI_FORCE_OFF, dev_id, [pi_id])[0]
        else:
            return self._send_cmd(CMD_PI_OFF, dev_id, [pi_id])[0]

    def get_pi_hbt_time(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        (success, data) = self._send_cmd(CMD_GET_HBT_TIME, dev_id, [pi_id])
        if success:
            return (success, data[0])
        else:
            return (success, None)

    def set_pi_hbt_time(self, dev_id, pi_id, time):
        validate_pi_id(pi_id)
        return self._send_cmd(CMD_SET_HBT_TIME, dev_id, [pi_id, time])[0]

    def get_pi_hbt_delay(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        (success, data) = self._send_cmd(CMD_GET_HBT_DELAY, dev_id, [pi_id])
        if success:
            return (success, data[0])
        else:
            return (success, None)

    def set_pi_hbt_delay(self, dev_id, pi_id, time):
        validate_pi_id(pi_id)
        return self._send_cmd(CMD_SET_HBT_DELAY, dev_id, [pi_id, time])[0]

    def get_pi_off_delay(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        (success, data) = self._send_cmd(CMD_GET_OFF_DELAY, dev_id, [pi_id])
        if success:
            return (success, data[0])
        else:
            return (success, None)

    def set_pi_off_delay(self, dev_id, pi_id, time):
        validate_pi_id(pi_id)
        return self._send_cmd(CMD_SET_OFF_DELAY, dev_id, [pi_id, time])[0]

    def get_pi_sig_delay(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        (success, data) = self._send_cmd(CMD_GET_SIG_OFF_DELAY, dev_id, [pi_id])
        if success:
            return (success, data[0])
        else:
            return (success, None)

    def set_pi_sig_delay(self, dev_id, pi_id, time):
        validate_pi_id(pi_id)
        return self._send_cmd(CMD_SET_SIG_OFF_DELAY, dev_id, [pi_id, time])[0]

    def get_error_buffer(self, dev_id=DEFAULT_ID):
        (success, data) = self._send_cmd(CMD_GET_ERROR_BUFFER, dev_id)
        if success:
            return (success, data)
        else:
            return (success, None)

    def clear_error_buffer(self, dev_id=DEFAULT_ID):
        return self._send_cmd(CMD_CLEAR_ERROR_BUFFER, dev_id)[0]

    def get_error_count(self, dev_id=DEFAULT_ID):
        (success, data) = self._send_cmd(CMD_GET_ERROR_COUNT, dev_id)
        if success:
            count = (data[0] << 8) | data[1]
            return (success, count)
        else:
            return (success, None)

    def reset_error_count(self, dev_id=DEFAULT_ID):
        return self._send_cmd(CMD_CLEAR_ERROR_COUNT, dev_id)[0]

    def get_error_pointer(self, dev_id=DEFAULT_ID):
        (success, data) = self._send_cmd(CMD_GET_ERROR_POINTER, dev_id)
        if success:
            return (success, data[0])
        else:
            return (success, None)

    def send_sig(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        return self._send_cmd(CMD_SEND_SIG, dev_id, [pi_id])[0]

    def set_pi_on_startup(self, dev_id, pi_id, status=True):
        validate_pi_id(pi_id)
        return self._send_cmd(CMD_SET_PI_ON_STARTUP, dev_id, [pi_id, int(status)])[0]

    def get_pi_on_startup(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        (success, value) = self._send_cmd(CMD_GET_PI_ON_STARTUP, dev_id, [pi_id])
        print(value)
        if success:
            return (success, bool(value[0]))
        else:
            return (success, None)

    def set_pi_sig_width(self, dev_id, pi_id, width):
        validate_pi_id(pi_id)
        return self._send_cmd(CMD_SET_SIG_WIDTH, dev_id, [pi_id, width])[0]

    def get_pi_sig_width(self, dev_id, pi_id):
        validate_pi_id(pi_id)
        (success, value) = self._send_cmd(CMD_GET_SIG_WIDTH, dev_id, [pi_id])
        if success:
            return (success, value[0])
        else:
            return (success, None)


def validate_pi_id(pi_id):
    if pi_id < 0 or pi_id > 1:
        raise InvalidPiError()
    return True
