from qube_control import *
from simple_pid import PID
import sys

# Initialize PID
output_limits = (-800, 800)
inner_pid = PID(28, 0, .6, setpoint=0, output_limits=output_limits)  # 2, 0, .05
outer_pid = PID(-.6, 0, -.45, setpoint=0, output_limits=(-300,300))  # .28284/4, 0, .17222/4

initialize_qube() # zeros the encoders and then waits for the arm to be lifted vertically

PID_data = open("PID_data_2.txt", "a")

start_time = time.time()
# Run PID control loop
while True:
    try:
        arm_angle, pen_angle = get_angle() # Pole the current encoder values
        inner_val = inner_pid(pen_angle) # Compute new output from the PID according to the systems current value
        outer_val = outer_pid(arm_angle) # Compute new output from the PID according to the systems current value
        motor_voltage = (outer_val + inner_val) # Sum the control signals to set the motor power
        set_motor(motor_voltage) # Set the motor power
        print(motor_voltage)
        update_led() # Update the LED color depending on the state of the pendulum
        watch_for_fall() # Check if the pendulum has falled and quit if it has
        PID_data.write(f'{arm_angle},{pen_angle},{motor_voltage},{(time.time() - start_time)}\n')
    except KeyboardInterrupt: # Check if the program has been quit
        print("stopping motor...")
        qube.set_motor(0)
        sys.exit()
