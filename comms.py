
from time import sleep
from string import printable

from serial import Serial

import commands
from errors import InvalidCommandError, CrcFailureError, InvalidIdError
from crc import calculate_crc_block as calc_crc

DEFAULT_BAUD = 9600
DEFAULT_TIMEOUT = 0.5

DEFAULT_ID = 0

RESPONSE_WAIT_TIME = 1

class Comms(object):
    def __init__(self, port_name, baud=DEFAULT_BAUD, timeout=DEFAULT_TIMEOUT):
        self.port_name = port_name
        self.baudrate = baud
        self.timeout = timeout
        self.serial = Serial(self.port_name, timeout=self.timeout, baudrate=self.baudrate)

    def _send_cmd(self, cmd, dev_id, args=None):
        if cmd > commands.NO_CMDS:
            raise InvalidCommandError()
        if dev_id > commands.MAX_ID:
            raise InvalidIdError()
        data = [cmd, dev_id, commands.CMD_MIN_LENGTHS[cmd]]
        if args is not None:
            data.extend(args)
        crc = calc_crc(data)
        data.append(crc)
        print data
        self.serial.write(data)
        sleep(RESPONSE_WAIT_TIME)
        resp = self.serial.readall()
        device_output = []
        for c in resp:
            device_output.append(ord(c))
        print device_output
        crc = calc_crc(device_output[:-1])
        if device_output[-1] != crc:
            raise CrcFailureError()
        return device_output[2:-2]

    def leds_off(self, dev_id=DEFAULT_ID):
        self._send_cmd(commands.CMD_DEBUG_LEDS_OFF, dev_id)

    def leds_on(self, dev_id=DEFAULT_ID):
        self._send_cmd(commands.CMD_DEBUG_LEDS_ON, dev_id)

    def get_sw_version(self, dev_id=DEFAULT_ID):
        return self._send_cmd(commands.CMD_GET_SW_VERSION, dev_id)[0]

