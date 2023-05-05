%% Inverted Pendulum model parameters
% Run this block to initialise simscape pendulum model parameters

% Inverted Pendulum Parameters
% lengths are in cm and mass in kg
base_size=7; % length of pendulum base cube
% Rotary arm parameters
rod_rad=1;% rotary arm radius
rod_length=8.5;% rotary arm length
rod_mass=0.095;% rotary arm mass
% Pendulum parameters
p_rad=1;% pendulum radius
p_length=12.9;% pendulum length
p_mass=0.024;% pendulum mass
rt1=base_size/2;
rt2=rod_length-0.4;
rt4=p_length/2;
D_r=0.0015/2;
D_p=0.0005/2;

%% DC Motor Parameters
kt=0.042;% torque constant
km=0.042;% motor back-emf constant
%R=8.4;% terminal resistance, nominal 8.4
Rm = 9.7; % nominal value = 8.4;
L=0.85e-3;% terminal inductance

%% Rotary Arm
% Mass (kg)
mr = 0.095;
% Total length (m)
r = 0.085;
% Moment of inertia about pivot (kg-m^2)
Jr = mr*r^2/3;
% Equivalent Viscous Damping Coefficient (N-m-s/rad)
br = 1e-3; % damping tuned heuristically to match QUBE-Servo 2 response
% 
%% Pendulum Link
% Mass (kg)
mp = 0.024;
% Total length (m)
Lp = 0.129;
% Pendulum center of mass (m)
l = Lp/2;
% Moment of inertia about pivot (kg-m^2)
Jp = mp*Lp^2/3;
% Equivalent Viscous Damping Coefficient (N-m-s/rad)
bp = 5e-5; % damping tuned heuristically to match QUBE-Sero 2 response
% Gravity Constant
g = 9.81;

alpha_bal_threshold = 10*pi/180; %range was 10
Ts = 0.005;
Tf=2;
Vmax = 5;
ic_alpha0 = pi*170/180;
theta_max = pi/3;