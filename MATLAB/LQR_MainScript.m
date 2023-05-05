%function outputData = LQR_MainScript(SL, simNumber)

% Debug
% SL.Q1 = 3;
% SL.Q2 = 1;
% SL.Q3 = 30;
% SL.Q4 = 100;
% SL.R = 1;
% simNumber = 1;
    %% Load simulation parameters
    run("LQR_SetParams.m");
    Q = diag([SL.Q1, SL.Q2, SL.Q3, SL.Q4]);
    R = SL.R;
    [K, ~, ~] = lqr(A,B,Q,R);

    %% Run simulation...
    outputData = sim("inverted_pendulum.slx");
    outputData.timeStart = datestr(now,"HH:MM:SS");

    %% Save more output data
    outputData.SL = SL;
    outputData.simNumber = simNumber;
    outputData.alphaRT = 0;
    outputData.alphaST = 0;
    outputData.alphaOS = 0;

%end