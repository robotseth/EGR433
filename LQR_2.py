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

# MATLAB file, L = 1
A_2 = np.array([[0, 0, 1, 0],
                [0, 0, 0, 1],
                [0, -17.8529, -2.0055, -0.2942],
                [0, -54.8919,  1.1297, -0.9046]])

# Paper by Govind and Kumar
A_3 = np.array([[0, 0, 1, 0],
                [0, 0, 0, 1],
                [0,  149.27, -0.0104, 0],
                [0, -261.60,  0.0103, 0]])

B_1 = np.array([[0],
                [0],
                [10.4452],
                [5.8841]])

B_2 = np.array([[0],
                [0],
                [10.4452],
                [-5.8841]])

B_3 = np.array([[0],
                [0],
                [49.72],
                [-49.14]])

C = np.array([[1, 0, 0, 0],
              [0, 1, 0, 0]])

D = np.array([[0],
              [0]])

# Define the weighting matrices
Q = np.diag([150, 150, 150, 150])
R = np.array([[5]])

# Design the LQR controller. Comment / uncomment as needed.
# K, S, E = control.lqr(A_1, B_1, Q, R)
# K, S, E = control.lqr(A_2, B_2, Q, R)
K, S, E = control.lqr(A_3, B_3, Q, R)
############################## End LQR Stuff ###########################

# Previous values of theta, alpha, theta_dot, alpha_dot is stored for next iteration of the loop
theta_n_k1 = 0
alpha_n_k1 = 0
theta_dot_k1 = 0
alpha_dot_k1 = 0

# Run LQR control loop
while True:
    try:
        watch_for_fall() # Check if the pendulum has falled and quit if it has
        update_led() # Update the LED color depending on the state of the pendulum

        setPoint = 0.0
        #alpha = qube.read_encoders()[1] * (2.0 * np.pi / 2048) - np.pi   # vert
        #theta = qube.read_encoders()[0] * (-2.0 * np.pi / 2048) - np.pi  # horz
        theta, alpha = get_angle('rad', invert=True) # Pole the current encoder values | pendulum, arm
        # invert angle of pendulum


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

        print(motor_voltage)
        set_motor(motor_voltage*50) # Set the motor power
        # Wait for a short period before updating again
        #time.sleep(0.005)
        #print(f'Outer Encoder: {qube.read_state().encoder0} | Inner Encoder: {qube.read_encoders()[1]-1024}')
    except KeyboardInterrupt:
        # quit
        print('stopping motor...')
        qube.set_motor(0)
        sys.exit()