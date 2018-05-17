# Pi Stack Python interface

Originally written for Python 2.7, now changed to be Python3.

## Requirements
* python3-serial ```sudo apt install python3-serial```
  alternatively, install using pip: ```python3 -m pip install pyserial```
## Usage
```
import pistack.comms, pistack.conversions
C = pistack.comms.Comms("/dev/ttyS15", 9600)
C.get_hw_version(4)
```

You can find the appropriate /dev interface with a dmesg command after you have plugged in your USB-to-RS232 converter. It may be /dev/ttyUSB0 or similar.

All commands take the board ID in as the first argument.  If it is not specified it defaults to Pi Stack ID 0.

The functions return a tuple of ```(success, data)``` the data sent over the serial bus is currently printed out, but I will remove this in a later version.

### ADC conversions
The data is sent as ints over the RS485 connection so there is the conversions module to convert this to actual values.  

```
 pistack.conversions.convert_vin(C.get_vin(4)[1])
```
Shows the input voltage measured by Pi Stack 4.  

Notes:
* The conversion functions are based on the resistor networks so there is some deviation between boards due to the tolerance of the components.
* When using the V3 hardware use ```pistack.conversions.convert_5v``` for the pi voltage measurements as well.  ```pistack.conversions.convert_pi_v``` is for the version 2 hardware which has slighty different resistor networks.

### Pi Power Control
```pi_on(0, 0)``` turns the pi on instantly.

```pi_off(0, 0)``` waits the time set by ```set_pi_sig_delay``` before turning the power off.  This is to allow the Pi time to respond to the shutdown command before the power is removed.  To override this an additional argument can be used eg. ```C.pi_off(0, 0, true)

