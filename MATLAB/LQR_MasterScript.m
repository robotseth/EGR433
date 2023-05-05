clear
clc

simLawExcel = "Megarun 1.xlsx";
sheetNum = 1;
RAW = readcell(simLawExcel,'Sheet',sheetNum);
% Convert missing to NaN
for i=1:size(RAW,1)
    for j=1:size(RAW,2)
        if(ismissing(RAW{i,j}))
            RAW{i,j} = NaN;
        end
    end
end

%% Parse input Excel sheet
fprintf("Reading Excel sheet.\n");
varLabelColumn = 1;
startingColumn = 2;
startingRow = 1;
numColumns = size(RAW,2) - startingColumn + 1;

BigSL = struct();
combinations = 1;
changedVariables = strings(0);
for row = startingRow:size(RAW,1)
    % For each variable
    varLabel = RAW{row,varLabelColumn};
    if(isnan(varLabel))
        continue;
    end
    numValues = 0;
    for column = startingColumn:size(RAW,2)
        % For each variable value
        varValue = RAW{row,column};
        if(isnan(varValue))
            continue;
        end
        if(class(varValue) == "char")
            %Try evaluating string
            varValue = Utility.parTryEval(varValue);
        end
        
        childVarLabel = sprintf("%s%d",varLabel,column);
        BigSL.(varLabel).(childVarLabel) = varValue;
        numValues = numValues + 1;
    end
    if(numValues > 1)
        combinations = combinations * numValues;
        changedVariables(length(changedVariables)+1) = varLabel;
    end
end
%% Prepare large SL with all iterations
fprintf("Preparing SL for %d combinations.\n",combinations);
SLIterations(1:combinations) = struct();
repeat = 1;

varLabels = fieldnames(BigSL);
for i=1:size(varLabels,1)
    varLabel = varLabels{i};
    valueLabels = fieldnames(BigSL.(varLabel));
    numValues = size(valueLabels,1);
    numCycles = combinations / (repeat * numValues);
    storeIndex = 1;
    for j=1:numCycles
        for k=1:numValues
            valueLabel = valueLabels{k};
            for l=1:repeat
                SLIterations(storeIndex).(varLabel) = BigSL.(varLabel).(valueLabel);
                storeIndex = storeIndex + 1;
            end
        end
    end
    repeat = repeat * numValues;
end

fprintf("Done. Ready to iterate over variables:\n");
for i=1:length(changedVariables)
    fprintf(" - %s\n",changedVariables(i));
end



%% Iterate through simulations
fprintf("Starting simulations for %g combination(s).\n",combinations);
numSims = combinations;
for simu = 1:numSims
    %% Run Simulation
    SL = SLIterations(simu);
    simNumber = simu;
    run("LQR_MainScript.m");
    bigOutputData(simu) = outputData;
    fprintf("Finished sim %d.\n",simNumber);
    
end

fprintf("Finished simulations.\n");

%% Save data
save("Megarun_1_OutputData.mat",'bigOutputData');
% outputStructCode = sprintf('%s/%s_%s.mat',simBatchFolder,'%s',simBatchCode);
% outputExcelName = sprintf('%s/SimData_%s.xlsx',simBatchFolder,simBatchCode);
% outputVariables = ["simNumber";"rngSeed";"timeStart";"timeEnd";"surviving";"collisionDeaths";"groundDeaths";"flightTime";"heightScore";"explorationPercent";"thermalUseScore";"finalHeightMax";"finalHeightMin";"finalHeightAvg"];
% 
% Utility.generateOutputStruct(outputStructCode,matFilesFolder,changedVariables,outputVariables);
% Utility.generateOutputExcelSheet(outputExcelName,matFilesFolder,RAW,changedVariables,outputVariables);
fprintf("Done!\n");