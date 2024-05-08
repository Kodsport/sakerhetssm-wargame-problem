from typing import Optional
from enum import Enum
import serial.tools.list_ports
import serial
import time
import struct

class Port(Enum):
    """
        Enum representing which port to use on the logic analyzer
    """
    A = 16
    B = 8
    C = 0

class LogicAnalyzer():
    """
        The main class for interacting with the logic analyzer
    """
    def __init__(self, port: Optional[str] = None):
        """
            Connect to a serial port and initialize the device.
                port: (optional) path to serial device (/dev/...). If not provided, search for a device with matching Vendor ID and Product ID
        """
        if port is None:
            devices = serial.tools.list_ports.comports() # List all com ports
            for device in devices:
                # Find the correct interface for the logic analyzer
                if device.vid == 0x0e7a and device.pid == 0x4c41:
                    self.port = serial.Serial(device.device, 115200)
                    break
            else:
                raise Exception("No compatible devices found")
        else:
            self.port = serial.Serial(port, 115200)

        # Initialize stuff
        self.gpio_io_mask = 0x000000
        self.gpio_value_mask = 0x000000
        self.inited = False

    def __enter__(self):
        """
            Enable the GPIO mode of the logic analyzer
        """
        self.port.__enter__()
        self.port.write(b"\xf0")
        self.inited = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            Disable the GPIO mode of the logic analyzer
        """
        self.inited = False
        self.port.write(b"\xf1")
        self.port.__exit__(exc_type, exc_val, exc_tb)

    def read_gpio(self, port: Port, pin: int) -> bool:
        """
            Read the state of a GPIO pin

            port: The port to read from
            pin: The pin from said port to read from (one-indexed)

            returns: True if GPIO is high (3.3v), False if GPIO is low (0v).
                     (for exact levels, see section 5.5.3.4. IO Electrical Characteristics in RP2040 reference manual)
                     If the GPIO is set to output mode, returns the current value being output
        """
        if not self.inited:
            raise RuntimeError("LogicAnalyzer must be used in a with block. See example usage for details")
        if pin < 1 or pin > 8:
            raise ValueError("Pin must be in range 1-8")
        self.port.write(b"\xf4")
        data = self.port.read(4)
        gpio_values = struct.unpack(">I", data)[0]
        return gpio_values & (1 << (port.value + 8 - pin)) != 0

    def set_gpio_mode(self, port: Port, pin: int, output: bool) -> None:
        """
            Set a GPIO pin to input or output
                port: The port to set I/O mode on
                pin:  The pin in said port to modify (one-indexed)
                output: True if pin should be output, False if pin should be input
        """
        if not self.inited:
            raise RuntimeError("LogicAnalyzer must be used in a with block. See example usage for details")
        if pin < 1 or pin > 8:
            raise ValueError("Pin must be in range 1-8")
        mask = 1 << (port.value + 8 - pin)
        if output: self.gpio_io_mask |= mask
        else: self.gpio_io_mask &= ~mask
        self.port.write(b"\xf2" + struct.pack("<I", self.gpio_io_mask))

    def set_gpio_level(self, port: Port, pin: int, high: bool) -> None:
        """
        Drive a GPIO in output mode to either high (3.3v), or low (0v)

            port: The port to output to
            pin:  The pin in said port to output to
            high: True if pin should be high (3.3v), False if pin should be low (0v)
        """
        if not self.inited:
            raise RuntimeError("LogicAnalyzer must be used in a with block. See example usage for details")
        if pin < 1 or pin > 8:
            raise ValueError("Pin must be in range 1-8")
        mask = 1 << (port.value + 8 - pin)
        if high: self.gpio_value_mask |= mask
        else: self.gpio_value_mask &= ~mask
        #print(self.gpio_value_mask)
        self.port.write(b"\xf3" + struct.pack("<I", self.gpio_value_mask))

# Example usage
if __name__ == "__main__":
    with LogicAnalyzer() as la:
        la.set_gpio_mode(Port.A, 1, True) # Set pin A1 to output

        while True:
            la.set_gpio_level(Port.A, 1, False) # Make pin A1 low (0v)
            print(la.read_gpio(Port.A, 1)) # Read the current level of A1 (should return False)
            time.sleep(1)

            la.set_gpio_level(Port.A, 1, True) # Make pin A1 high (3.3v)
            print(la.read_gpio(Port.A, 1)) # Read the current level of A1 (should return True)
            time.sleep(1)
