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
R=8.4;% terminal resistance, nominal 8.4
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



% Initial pendulum intial angle in degrees
% 180 corresponds to upright position
% can also be selected in the simulink model
alpha_0=170;

%% State space equation for state-feedback controller for Inverted Pendulum
% Run this block to initialise state-space controller parameters

% Inverted Pendulum Parameters
% Rotary arm parameters
L_r=rod_length/100;%convert cm to m
r_r=rod_rad/100;%convert cm to m
m_r=rod_mass;
J_r=(1/4)*m_r*r_r^2+(1/3)*m_r*L_r^2;% rotary arm moment of inertia
% Pendulum parameters
L_p=p_length/100;
m_p=p_mass;
r_p=p_rad/100;
J_p=(1/4)*m_p*r_p^2+(1/3)*m_p*L_p^2;% pendulum moment of inertia

% System linearized at [0 0 0 0]' or [0 pi 0 0]'
% For [0 0 0 0]' set l=1 For comparing state-space and nonlinear model
% normally down
% For [0 pi 0 0]' set l=-1 (for controller design)
% normally up
l=-1;

M=[m_p*L_r^2+J_r -l*0.5*m_p*L_p*L_r;
   l*0.5*m_p*L_p*L_r J_p+0.25*m_p*L_p^2];
G=[D_r+kt*km/R 0;0 D_p];
K=[0 0;0 l*0.5*m_p*L_p*9.8];
F=[kt/R;0];

%Linearized System Matrices
A=[zeros(2) eye(2);-inv(M)*K -inv(M)*G];
B=[0;0;inv(M)*F];
C=[1 0 0 0;
   0 1 0 0];
D=[0;0];

Ts = 0.01;
Tf=2;
Vmax = 5;
ic_alpha0 = pi*170/180;
theta_max = pi/3;