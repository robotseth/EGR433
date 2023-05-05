from qube_control import *
from log import Log
import time
import sys
import numpy as np
import control

# Initialize
initialize_qube()
output_limits = (-800,800)
motor_voltage = 0

########################### Begin LQR Stuff ###########################
# Define the system matrices

# MATLAB file, L = -1
A_1 = np.array([[0, 0, 1, 0],
                [0, 0, 0, 1],
                [0, -17.8529, -2.0055,  0.2942],
                [0,  54.8919, -1.1297, -0.9046]])

# MATLAB file, L = -2
A_2 = np.array([[0, 0, 1, 0],
                [0, 0, 0, 1],
                [0, -17.8529, -2.0055, -0.2942],
                [0, -54.8919,  1.1297, -0.9046]])

B_1 = np.array([[0],
                [0],
                [10.4452],
                [5.8841]])

B_2 = np.array([[0],
                [0],
                [10.4452],
                [-5.8841]])

C = np.array([[1, 0, 0, 0],
              [0, 1, 0, 0]])

D = np.array([[0],
              [0]])

# Define the weighting matrices
Q = np.diag([30, 100, 0, 0])
R = np.array([[.004]])

# Design the LQR controller. Comment / uncomment as needed.
K, S, E = control.lqr(A_1, B_1, Q, R) # assume up is 0
#K, S, E = control.lqr(A_2, B_2, Q, R) # assume down is 0

############################## End LQR Stuff ###########################

# Previous values of theta, alpha, theta_dot, alpha_dot is stored for next iteration of the loop
theta_n_k1 = 0
alpha_n_k1 = 0
theta_dot_k1 = 0
alpha_dot_k1 = 0


#LQR_data = open("LQR_data_3.txt", "a")
start_time = time.time()

# Run LQR control loop
while True:
    try:
        watch_for_fall() # Check if the pendulum has falled and quit if it has
        update_led() # Update the LED color depending on the state of the pendulum

        setPoint = 0.0
        #alpha = qube.read_encoders()[1] * (2.0 * np.pi / 2048) - np.pi   # vert
        #theta = qube.read_encoders()[0] * (-2.0 * np.pi / 2048) - np.pi  # horz
        theta, alpha = get_angle('rad', invert=False) # Pole the current encoder values | arm, pendulum
        theta = 0

        #print(f'Arm: {theta} | Pendulum: {alpha}')

        if abs(alpha) >= (10 * np.pi / 180):
            theta_n = setPoint - theta
            alpha_n = setPoint - alpha

            theta_dot = (50.0 * theta_n) - (50.0 * theta_n_k1) + (0.9512 * theta_dot_k1)
            theta_n_k1 = theta_n
            theta_dot_k1 = theta_dot

            alpha_dot = (50.0 * alpha_n) - (50.0 * alpha_n_k1) + (0.9512 * alpha_dot_k1)
            alpha_n_k1 = alpha_n
            alpha_dot_k1 = alpha_dot

            ############### The only section in the loop that has anything to do with LQR
            state = np.array([theta, alpha, theta_dot, alpha_dot])
            motor_voltage = -K @ state
            #print(-K @ state)

        print(motor_voltage)
        set_motor(motor_voltage) # Set the motor power
        # Wait for a short period before updating again
        #print(f'Outer Encoder: {qube.read_state().encoder0} | Inner Encoder: {qube.read_encoders()[1]-1024}')
        #LQR_data.write(f'{alpha},{theta},{motor_voltage},{(time.time() - start_time)}\n')
    except KeyboardInterrupt:
        # quit
        print('stopping motor...')
        qube.set_motor(0)
        sys.exit()
