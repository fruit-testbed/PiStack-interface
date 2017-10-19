
from time import sleep
from string import printable

from serial import Serial

import commands
from errors import InvalidCommandError, CrcFailureError, InvalidIdError
from crc import calculate_crc_block as calc_crc

DEFAULT_BAUD = 9600
DEFAULT_TIMEOUT = 0.5

DEFAULT_ID = 0

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
        sleep(0.5)
        resp = self.serial.readall()
        print_output = "" #what to print out for debug purposes
        device_output = []
        for c in resp:
            if c in printable:
                print_output += c
            else:
                print_output += ("%02X " % ord(c))
                device_output.append(ord(c))
        print print_output
        return device_output

    def leds_off(self, dev_id=DEFAULT_ID):
        return self._send_cmd(commands.CMD_DEBUG_LEDS_OFF, dev_id)

