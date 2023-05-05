doLoad = false;
doCalc = true;
doSave = false;
outSheet = "PID_Megarun_2_Data.xlsx";

if doLoad
    disp("Now Loading")
    load PID_Megarun_2_OutputData.mat
    disp("Done Loading")
end
if doCalc
    disp("Now Calculating")
    numSims = length(bigOutputData);
    N = 1728;
    T = 501;
    Alpha = zeros(501, N);
    headerSize = 8;
    AugmentedMatrix = zeros(501 + headerSize, N);
    risetimes = zeros(1,N);
    invalid = false(1,N);
    for Simu = 1:numSims
        % save alpha i guess
        Alpha(:,Simu) = bigOutputData(Simu).Alpha(:,2);
        PIDs =  [bigOutputData(Simu).SL.O_P;
                 bigOutputData(Simu).SL.O_I;
                 bigOutputData(Simu).SL.O_D;
                 bigOutputData(Simu).SL.I_P;
                 bigOutputData(Simu).SL.I_I;
                 bigOutputData(Simu).SL.I_D];
        if (max(abs(Alpha((end-500):end,Simu))) > 4)
            invalid(Simu) = true;
        end
        AugmentedMatrix(:,Simu) = [Simu;PIDs;invalid(Simu);Alpha(:,Simu)];
        pos = find(Alpha(:,Simu)>0);
        risetimes(Simu) = pos(1)/50;
        if mod(Simu,100)==0
            fprintf("%4.0f\n",Simu);
        end
    end
    disp("Done Calculating")
end
if doSave
    disp("Now Saving")
    Header = ["Num";"OP";"OI";"OD";"IP";"II";"ID";"Invalid";"Alphas"];
    writematrix(Header,outSheet,"Sheet","Data");
    writematrix(AugmentedMatrix, outSheet, "Sheet","Data","Range","B1")
    
    writematrix(Header',outSheet,"Sheet","Analysis", "Range","A8","AutoFitWidth",false);
    writematrix(AugmentedMatrix(1:headerSize,:)', outSheet, "Sheet","Analysis","Range","A9","AutoFitWidth",false)
    
    writematrix(AugmentedMatrix(:,(~invalid)), outSheet, "Sheet","onlyValids","Range","B1","AutoFitWidth",false)
    writematrix(Header,outSheet,"Sheet","onlyValids");
    disp("Done saving")
end
numPassed = sum(~invalid)
plot(Alpha(:,~invalid))