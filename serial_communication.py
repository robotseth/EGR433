# This program is used to interface with the Qube over SPI.
# Programmed by Seth Altobelli - Last Updated 5/2/2023

import time
import sys
import spidev
from simple_pid import PID
import numpy as np
import struct

class Qube:
    def __init__(self, device_id, encoder0, encoder1, tach0, status, current_sense):
        self.device_id = device_id
        self.encoder0 = encoder0
        self.encoder1 = encoder1
        self.tach0 = tach0
        self.status = status
        self.current_sense = current_sense

    def __str__(self):
        return "Qube(device_id={}, encoder0={}, encoder1={}, tach0={}, status={}, current_sense={})".format(
            self.device_id, self.encoder0, self.encoder1, self.tach0, self.status, self.current_sense)

    def read_state():
        msg = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # Replace with appropriate command or dummy bytes
        response = spi.xfer2(msg)
        qube_data = Qube.parse_spi_data(response)
        return qube_data

    def parse_spi_data(rx_packet):
        # Extract data from packet
        device_id = (rx_packet[0] << 8) | rx_packet[1]
        encoder0 = (rx_packet[2] << 16) | (rx_packet[3] << 8) | rx_packet[4]
        encoder1 = (rx_packet[5] << 16) | (rx_packet[6] << 8) | rx_packet[7]
        tach0 = (rx_packet[8] << 16) | (rx_packet[9] << 8) | rx_packet[10]
        status = rx_packet[11]
        current_sense = (rx_packet[12] << 8) | rx_packet[13]

        # Return extracted data as Qube object
        #device_id = "{}{}".format(device_id_msb, device_id_lsb)
        return Qube(device_id, encoder0, encoder1, tach0, bin(status), current_sense)
    
    def read_encoders():
        data = Qube.read_state()
        encoder_vals = [wrap_number(data.encoder0), wrap_number(data.encoder1)]
        return encoder_vals
    
    # Pack the values into a three-byte little-endian packet

    
    def parse_motor_encoder(): #encoder_bytes
        """
        if (encoder_bytes & 0x00800000):
            encoder_bytes = encoder_bytes | 0xFF000000
        theta = encoder_bytes * (-2.0 * np.pi / 2048)
        return theta
        """
        msg = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # Replace with appropriate command or dummy bytes
        response = spi.xfer2(msg)
        byte_packet = struct.pack('>BBB', response[2], response[3], response[4])
        signed_int = struct.unpack('>i', byte_packet + b'\x00')[0]
        signed_int = int(signed_int/256)
        return signed_int


    def parse_arm_encoder(bytes):
        pass

    def write_spi_data(mask, led = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00], encoder_0 = [0x00, 0x00, 0x00], encoder_1 = [0x00, 0x00, 0x00], motor = [0x00, 0x00]):
        # [mode, padding, write mask, led bytes, encoder 0 set bytes, encoder 1 set bytes, motor set bytes]
        msg = [0x01, 0x00] + [mask] + led + encoder_0 + encoder_1 + motor  # Replace with appropriate command or dummy bytes
        spi.writebytes(msg)

    def set_motor(speed = 0):
        speed = generate_motor_command(speed)
        mask = 0b00000011
        lsb = speed & 0xFF
        msb = speed >> 8
        #print(f'MSB: {msb:b}   LSB: {lsb:b}')
        Qube.write_spi_data(mask, motor = [msb, lsb])

    def set_led_color(color_array = [255,0,0]):
        mask = 0b00011100
        r_lsb = color_array[0] & 0xFF
        r_msb = (color_array[0] >> 8) & 0xFF
        g_lsb = color_array[1] & 0xFF
        g_msb = (color_array[1] >> 8) & 0xFF
        b_lsb = color_array[2] & 0xFF
        b_msb = (color_array[2] >> 8) & 0xFF
        Qube.write_spi_data(mask, led=[r_msb,r_lsb,g_msb,g_lsb,b_msb,b_lsb])

    def zero_motor_encoder():
        mask = 0b01100000
        Qube.write_spi_data(mask)

    def moving_average_filter(data, window_size):
        window = np.ones(window_size) / float(window_size)
        return np.convolve(data, window, 'same')



def wrap_number(number, min_value=0, max_value=2048):
    """
    while number > max_value:
        number = number - max_value
    while number < min_value:
        number = number - min_value
    return number
    """
    return (number - min_value) % (max_value - min_value + 1) + min_value

def format_motor_command(motor_command):
    # Check if motor should be enabled
    if motor_command < 0:
        motor_command = -motor_command
        motor_command |= 1 << 15  # set bit 15 to 1 to enable motor
    else:
        motor_command &= ~(1 << 15)  # set bit 15 to 0 to disable motor
    
    # Format the motor command value
    if motor_command > 999:
        motor_command = 999
    elif motor_command < -999:
        motor_command = -999
        
    # Convert to 2's complement if negative
    if motor_command < 0:
        motor_command = (1 << 15) | ((-motor_command) ^ 0xFFFF)
    
    return motor_command

def generate_motor_command(speed):
    if speed > 999:
        speed = 999
    elif speed < -999:
        speed = -999

    return (1 << 15) | speed

#print(f'{format_motor_command(30)}')
#print(f'{format_motor_command(-30)}')

# Initialize SPI interface
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = 1000000  # Set maximum SPI clock speed
spi.mode = 2  # Set SPI mode to 0 (CPOL = 0, CPHA = 0)



"""

import spidev

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)  # Assuming you're using the default SPI bus and device on the Pi

# Configure SPI settings
spi.max_speed_hz = 1000000  # Set SPI clock speed to 1 MHz
spi.mode = 0b00  # Set SPI mode to 0b00 (CPOL=0, CPHA=0)


tx_data = [0x01] + [0x00]*15  # 16-byte array with first byte 0x01 and rest 0x00
spi.writebytes(tx_data)

# Read SPI data in loop and print raw packets
while True:
    # Read 10 bytes of data from SPI bus
    data = spi.readbytes(16)
    
    # Print raw packet data as hex
    print(' '.join([format(byte, '02X') for byte in data]))
"""

"""
import spidev
import time

bus = 0
device = 0
spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 10000
spi.mode = 2  # Set SPI mode to 0 (CPOL = 0, CPHA = 0)

msg = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # Replace with appropriate command or dummy bytes
response = spi.xfer2(msg)

device_id = (response[0] << 8) | response[1]

print("Received data:", response)
print(f'The device id is: {device_id}')

spi.close()

"""