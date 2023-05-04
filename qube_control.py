# initialize the spi
# zero the encoders
# read encoder values
# send motor values
# send led color
# disable motors and stop program if it falls

from serial_communication import Qube  # read_encoders, set_motor, set_led_color
import time
import sys
from loguru import logger
import numpy as np

# Creates a Qube object
qube = Qube

def initialize_qube():
    qube.zero_motor_encoder()
    # waits for pendulum to be lifted
    # TODO: check for angle instead of waiting a set time
    logger.info("Please lift pendulum")
    while abs(get_angle()[1]) > 30:
         time.sleep(0.1)
    logger.info("Initializing Completed - Starting control loop")

def get_angle(type='tics', invert=False):
    arm_angle = qube.moving_average_filter(qube.parse_motor_encoder(), 3)[-1]
    pen_angle = qube.moving_average_filter(1024 - qube.read_encoders()[1], 3)[-1]
    if type == 'rad':
         arm_angle = arm_angle*(np.pi/1024)*3
         pen_angle = pen_angle*(np.pi/1024)*3
    if invert:
         arm_angle = arm_angle*-1
         pen_angle = pen_angle*-1
    return arm_angle, pen_angle

def update_led(band=10):
    if abs(get_angle()[1]) < band: #make sure this works and I do not need to directly get the angle of the spi packet like before | abs(qube.read_encoders()[1] - 1024) > 800
        qube.set_led_color([0, 255, 0])
    else:
        qube.set_led_color([255, 0, 0])
    pass

def set_motor(motor_voltage):
        motor_voltage = max(-800, min(800, motor_voltage))
        qube.set_motor(int(motor_voltage))
        
def watch_for_fall():
    if abs(qube.read_encoders()[1] - 1024) > 800:
        print("")
        logger.warning("Pendulum fell - Stopping motor...")
        qube.set_motor(0)
        sys.exit()
