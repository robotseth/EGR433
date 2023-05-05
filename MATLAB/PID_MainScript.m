%function outputData = LQR_MainScript(SL, simNumber)

    %% Load simulation parameters
    run("PID_SetParams.m");
    O_P = SL.O_P;
    O_I = SL.O_I;
    O_D = SL.O_D;
    I_P = SL.I_P;
    I_I = SL.I_I;
    I_D = SL.I_D;

    %% Run simulation...
    outputData = sim("s_qube2_bal_PID.slx");
    outputData.timeStart = datestr(now,"HH:MM:SS");

    %% Save more output data
    outputData.SL = SL;
    outputData.simNumber = simNumber;
    outputData.alphaRT = 0;
    outputData.alphaST = 0;
    outputData.alphaOS = 0;

%end