%% Init
clear

files = ["240408_N6700B_amplitude+phase_readings_Qminus_filterBW_30kHz_sweep_0-2000mV_10mV_avgTime_750ms_LO_11dBm3_11GHz666_1Mpts.csv", ...
    "240408_N6700B_amplitude+phase_readings_-6dB_Qminus_filterBW_30kHz_sweep_0-2000mV_10mV_avgTime_750ms_LO_11dBm3_11GHz666_1Mpts.csv", ...
    "240408_N6700B_amplitude+phase_readings_-12dB_Qminus_filterBW_30kHz_sweep_0-2000mV_10mV_avgTime_750ms_LO_11dBm3_11GHz666_1Mpts.csv"];

for i = 1:3
    M = readmatrix(files(i));
    control(:, i) = M(:, 1);
    amplitude(:, i) = M(:, 2);
    phase(:, i) = M(:, 3);
    Re(:, i) = amplitude(:, i) .* cosd(phase(:, i));
    Im(:, i) = amplitude(:, i) .* sind(phase(:, i));
    
    Re_mean(:, i) = mean(Re(:, i));
    Im_mean(:, i) = mean(Im(:, i));
    
    
    [~, i45(i)] = min(abs(phase(:, i) - 45));
    [~, i135(i)] = min(abs(phase(:, i) - 135));
    a45(i) = amplitude(i45(i), i);
    a135(i) = amplitude(i135(i), i);
    disp(["q =" num2str(a135(i) / a45(i))]);
end

%% Plot
close all

figure
t = tiledlayout(2, 1);

nexttile
plot(control, amplitude)
title("Q- output")
legend(["0dB" "-6dB" "-12dB"])
grid on
ylabel("Amplitude (Volts)")

nexttile
plot(control, phase)
grid on
xlabel("Control Voltage (Volts)")
ylabel("Phase (Degrees)")

figure
title("Q- output")
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