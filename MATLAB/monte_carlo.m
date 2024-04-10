%% Init
% Parameters
clear

s = RandStream.create("twister");

n_sim = 10;
step = 3;

% Data structures
dir = [0 20];
err = [2 4 6];
data = cell(length(err), length(dir));

%% Sim
for i = 1:length(err)
    for j = 1:length(dir)
        S = zeros(360 / step + 1, n_sim + 2);

        arr = PhasedArray(4, 140e9, 0.5, "ThetaStepSize", step);
        arr = arr.setDir(dir(j));
        S(:, 2) = 10 * log10(arr.getGain()');

        for k = 1:n_sim
            arr = PhasedArray(4, 140e9, 0.5, "PhaseError", ...
                              err(i), "RandStream", s, ...
                              "ThetaStepSize", step);
            arr = arr.setDir(dir(j));
            S(:, k + 2) = 10 * log10(arr.getGain()');
            S(:, 1) = arr.Theta;
        end

        data{i, j} = S;
        writematrix(S, strcat('mc_sim_err_', num2str(err(i)), '_', ...
            'dir_', num2str(dir(j)), '.csv'))
    end
end

%% Plt
close all
figure

t = tiledlayout(length(err), length(dir), "TileSpacing", "compact");
colororder(flip(sky))

for i = 1:length(err)
    for j = 1:length(dir)
        nexttile
        plot(data{i, j}(:, 1), data{i, j}(:, 2:end))
        xlim([-180 180])
        ylim([-40 20])
    end
end