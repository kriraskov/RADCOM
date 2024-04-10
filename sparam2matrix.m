% Read all the .s2p file recorded for the voltage sweep and save it as
% a single matrix in .csv format.
%% Init
clear

ps_names = {'cartman' 'kenny' 'kyle' 'stan'};
dac_names = {'DACA' 'DACB' 'DACC' 'DACD'};
s21_data = cell(1, length(ps_names));
freq = linspace(10.5e9, 12.5e9, 0.5e9); % Frequencies in Hz
codes = 0:13:2^16-1;

%% Read
for i = 1:length(ps_names)
    % Empty vector to store S21 for every code
    s21_data{i} = zeros(length(freq), length(codes));

    for j = 1:length(codes)
        % Create the file name
        file = sprintf('s2p/volt/CMD297P34_%s_%s_ch1_1mV_10.5-12.5GHz_5pts/CMD297P34_%s_dac_ch1_%dmV_10.5-12.5GHz_5pts.s2p', ...
            ps_names{i}, ps_names{i}, codes(j));

        try
            % Read .s2p file
            s2p_data = sparameters(file);
            s21_data{i}(:, j) = squeeze(s2p_data.Parameters(2, 1, :));
        catch ME
            % Some files are faulty, skip these
            fprintf('Error processing file %s: %s\n', file, ME.message)
        end
    end
end

%% Save
for i = 1:length(ps_names)
    % Remove the faulty columns
    I = find(s21_data{i}(1, :));
    s21_data{i} = s21_data{i}(:, I);

    % Save the new matrix as a csv file
    filename = sprintf('CMD297P34_%s_dac_ch1_1mV_10.5-12.5GHz_5pts.csv', ...
        ps_names{i});
    writematrix([codes(I)' s21_data{i}'], filename)
end