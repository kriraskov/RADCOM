import time
import serial


def modbus_crc16(data: bytes, poly: int = 0xA001):
    """Modbus CRC16.

    Generate a 16-bit CRC (Modbus) code for a given byte string.

    Args:
        data (bytes): Byte string to encode.
        poly (int): CRC polynomial.

    Returns:
        int: The two generated CRC bytes, with the least significant bit
        first (little endian).
    """
    crc = 0xFFFF  # Initial value
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= poly
            else:
                crc >>= 1
    return crc


class DAC:
    """DAC class.

    The DAC is a mystery box. No datasheet available.
    """
    def __init__(self, port: str, baud: int = 9600):
        """DAC constructor.

        Args:
            port (str): Serial port of the DAC.
            baud (int): Baud rate for the serial communication.
        """
        self._port = serial.Serial(port, baud)

    def write(self, data: bytes):
        """Write data to the DAC.

        Sends a write command (`b'\x01\x06'`) followed by a byte string
        to be sent to the DAC. The message is encoded with CRC16
        (Modbus).

        Args:
            data (bytes): Data to write to DAC.
        """
        msg = b'\x01\x06' + data
        crc = modbus_crc16(msg).to_bytes(2, 'little')
        self._port.write(list(msg + crc))

    def close(self):
        """Close the serial port.

        Wrapper method for `pyserial.Serial.close()`.
        """
        self._port.close()

    def set_volt(self, channel: int, volt: int):
        """Set the output voltage of the DAC.

        Updates the output voltage of the specified channel.
        Args:
            channel (int): Output channel (1-6).
            volt (int): Output voltage in millivolts.
        """
        chl = (channel + 0x09) & 0xFF           # 0x0A for channel 1, etc.
        val = volt.to_bytes(2, 'big')
        self.write(bytes([0x00, chl]) + val)


if __name__ == "__main__":
    dac = DAC('COM5')
    while True:
        #dac.set_volt(1, 0)
        dac.set_volt(2, 0)
        time.sleep(0.1)
        #dac.set_volt(1, 1000)
        dac.set_volt(2, 1000)
        time.sleep(0.1)
    dac.close()
