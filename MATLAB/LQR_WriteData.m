clear
load Megarun_1_OutputData.mat
numSims = length(bigOutputData);
Alpha = zeros(301, 675);
AugmentedMatrix = zeros(307, 675);
writematrix(["Num";"Q1";"Q2";"Q3";"Q4";"R";"Alphas"],"Megarun_1_Data.xlsx");
risetimes = zeros(1,675);
for Simu = 1:numSims
    % save alpha i guess
    Alpha(:,Simu) = bigOutputData(Simu).Alpha(:,2);
    QandR = [bigOutputData(Simu).SL.Q1;
             bigOutputData(Simu).SL.Q2;
             bigOutputData(Simu).SL.Q3;
             bigOutputData(Simu).SL.Q4;
             bigOutputData(Simu).SL.R];
    AugmentedMatrix(:,Simu) = [Simu;QandR;Alpha(:,Simu)];
    pos = find(Alpha(:,Simu)>0);
    risetimes(Simu) = pos(1)/100;
end

writematrix(AugmentedMatrix, "Megarun_1_Data.xlsx", "Range","B1")
