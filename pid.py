from serial_communication import Qube #read_encoders, set_motor, set_led_color
from simple_pid import PID
import time
import sys

# TODO:
# live graph of encoders | Not possible when remoting into the raspberry pi
# nested pid loops | the horizontal encoder is very diffifult to use because it wraps over instead of going negative. Probably a binary overflow error of some kind :(


# Creates a Qube object
qube = Qube

# Initialize PID
output_limits = (-800,800)
inner_pid = PID(3.2, 0, .08, setpoint=-10, output_limits=output_limits) # PID loop to keep the arm vertical | PID(2.75, 0, 0.05, setpoint=-10, output_limits=output_limits)
outer_pid = PID(.1, 0, 0, setpoint=0, output_limits=output_limits) # PID loop to keep the horizontal arm centered

# Read SPI packets and parse data
while True:
    try:
        if (qube.read_encoders()[1]-1024) < -15 or (qube.read_encoders()[1]-1024) > 15:
            qube.set_led_color([255,0,0])
        else:
            qube.set_led_color([0,255,0])

        # Compute new output from the PID according to the systems current value
        inner_val = inner_pid(1024 - qube.read_encoders()[1])
        outer_val = outer_pid(qube.parse_motor_encoder(qube.read_encoders()[0]))
        motor_voltage = inner_val*0 + outer_val # inner PID loop zeroed to tune the outer PID
        #print(motor_voltage)
        qube.set_motor(int(motor_voltage))
        # Wait for a short period before updating again
        time.sleep(0.005)
        print(f'Outer Encoder: {qube.read_state().encoder0} | Inner Encoder: {qube.read_encoders()[1]-1024}')
    except KeyboardInterrupt:
        # quit
        print('stopping motor...')
        qube.set_motor(0)
        sys.exit()
