clear

dB = @(x) 10^(x / 10);
show_filter = true;
show_plot = false;           % Don't.
write_file = false;

%% Filter Parameters
N = 2048e3 - 1;
Fs = 10e9;
Fc = 100e6;
B = 1e6;
Fpass1 = Fc - B / 2;
Fpass2 = Fc + B / 2;

%% Create Filter
Fnorm = [Fpass1 Fpass2] ./ (Fs / 2);
b = fir1(N, Fnorm);

disp(strcat("Filter: N = ", num2str(N)))

if show_filter
    fvtool(b)
end

if write_file
    file = sprintf("fir_bpf_100MHz_%dkHz_hamming_%dtaps.csv", ...
        B / 1e3, length(b));
    writematrix(b, file)
end

%% Test signal
if show_plot
    close all
    f = Fc / (Fs / 2);
    X = linspace(0, 5 / f, 10*N);
    Y = sin(2 * pi * f * X);
    Yfilt = filter(b, 1, Y);
    plot(X, Yfilt)
end