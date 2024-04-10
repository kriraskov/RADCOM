%% Init
clear

% File attributes
basedir = "240409_back_to_back\240409\";
atten = [0 0 6];
line = "Q-";
n_pts = 501;

% Data structures
control = zeros(n_pts, length(atten));
amplitude = zeros(n_pts, length(atten));
phase = zeros(n_pts, length(atten));
Re = zeros(n_pts, length(atten));
Im = zeros(n_pts, length(atten));
Re_mean = zeros(1, length(atten));
Im_mean = zeros(1, length(atten));

%% Read
files = dir(strcat(basedir, "*", line, "*.csv"));

for i = 1:3
    M = readmatrix(strcat(basedir, files(i).name));
    control(:, i) = M(:, 1);
    amplitude(:, i) = M(:, 2);
    phase(:, i) = M(:, 3);
    Re(:, i) = amplitude(:, i) .* cosd(phase(:, i));
    Im(:, i) = amplitude(:, i) .* sind(phase(:, i));
    
    Re_mean(:, i) = mean(Re(:, i));
    Im_mean(:, i) = mean(Im(:, i));
end

%% Plot
close all

figure
t = tiledlayout(2, 1);

nexttile
plot(control, amplitude)
title(strcat(line, " output"))
legend(["0dB" "-6dB" "-12dB"])
grid on
xlim([0 5])
ylabel("Amplitude (Volts)")

nexttile
plot(control, phase)
grid on
xlabel("Control Voltage (Volts)")
ylabel("Phase (Degrees)")
xlim([0 5])

figure
title(strcat(line, " output"))
hold on
scatter(Re, Im)
scatter(Re_mean, Im_mean)
legend(["0dB" "-6dB" "-12dB"])
hold off
grid on
ax = gca;
ax.XAxisLocation = 'origin';
ax.YAxisLocation = 'origin';
xlabel("Re (Volts)")
ylabel("Im (Volts)")