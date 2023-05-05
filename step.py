from log import Log
from qube_control import *
import time

datalog = Log(name='step')

initialize_qube(wait_for_lift=False) # zeros the encoders and then waits for the arm to be lifted vertically

start_time = time.time()
while True:
    try:
        arm_angle, pen_angle = get_angle() # Pole the current encoder values
        motor_voltage = 100 # step power
        if time.time() - start_time > .5: # after a half second has passed, input the step
            set_motor(motor_voltage) # Set the motor power
        datalog.log(data=[pen_angle, arm_angle, motor_voltage, (time.time() - start_time)])
        if time.time() - start_time > 2: # after a 2 seconds have passed, quit
            qube.set_motor(0)
            datalog.save()
            sys.exit()
    except KeyboardInterrupt: # Check if the program has been quit
        print("stopping motor...")
        qube.set_motor(0)
        datalog.save()
        sys.exit()
