% clear all;clc;
% eeglab;

mff_path = 'D:\\EGI_DATA\\EGI_REST'
set_path = 'D:\\EGI_DATA\\EGI_REST_SET'
location_path = 'C:\\Users\\const\\MATLAB\\eeglab2021.0\\sample_locs\\GSN129.sfp'

for i = 1 : 31
    fname = fullfile(mff_path, sprintf('sub-%03d_task-rest_eeg.mff', i));
    outname = fullfile(set_path, sprintf('sub-%03d_task-rest_eeg.set', i));
    % sprintf('------------------- Processing %s -------------------', fname);
    % import data
    EEG = pop_mffimport({fname}, {'code'});
    % load channel location
    EEG = pop_chanedit(EEG, 'load', {location_path, 'filetype', 'autodetect'}, 'changefield', {132, 'labels', 'E129'});
    % resample
    EEG = pop_resample(EEG, 250);
    % filter
    EEG = pop_eegfiltnew(EEG, 'locutoff', 2);
    EEG = pop_eegfiltnew(EEG, 'hicutoff', 20);
    % remove line noise
    EEG = pop_eegfiltnew(EEG, 'locutoff', 48, 'hicutoff', 52, 'revfilt', 1);
    EEG = pop_cleanline(EEG, 'bandwidth', 2, 'chanlist', [1:129], 'computepower', 1, 'linefreqs', 50, 'normSpectrum', 0, 'p', 0.01, 'pad', 2, ...
                        'plotfigures', 0, 'scanforlines', 1, 'sigtype', 'Channels', 'tau', 100, 'verb', 1, 'winsize', 4, 'winstep', 1);
    % remove useless channels
    % EEG = pop_select(EEG, 'nochannel', {'E125', 'E128', 'E43', 'E48', 'E49', 'E56', 'E63', ...
    %                 'E68', 'E73', 'E81', 'E88', 'E94', 'E99', 'E107', 'E113', 'E120', 'E119'});
    EEG = pop_select(EEG, 'nochannel', {'E125', 'E128', 'E43', 'E48', 'E49', 'E56', 'E63', ...
                    'E68', 'E73', 'E81', 'E88', 'E94', 'E99', 'E107', 'E113', 'E120', 'E119', ...
                    'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E121', 'E126', 'E127'});
    % reject bad channels
    originalEEG = EEG;
    EEG = pop_clean_rawdata(EEG, 'FlatlineCriterion', 'off', 'ChannelCriterion', 0.8, 'LineNoiseCriterion', 4, 'Highpass', 'off', ...
                            'BurstCriterion', 'off', 'WindowCriterion', 'off', 'BurstRejection', 'off', 'Distance', 'Euclidian');
    % interpolate channels
    EEG = pop_interp(EEG, originalEEG.chanlocs, 'spherical');
    % re-reference
    EEG = pop_reref(EEG, []);
    % correct bad data periods by ASR
    EEG = pop_clean_rawdata(EEG, 'FlatlineCriterion', 'off', 'ChannelCriterion', 'off', 'LineNoiseCriterion', 'off', 'Highpass', ...
                            'off', 'BurstCriterion', 20, 'WindowCriterion', 'off', 'BurstRejection', 'off', 'Distance', 'Euclidian');
    % re-reference
    EEG = pop_reref(EEG, []);
    % save 0-6s data after rsfi
    EEG = pop_rmdat(EEG, {'rsfi'}, [-0.1 6], 0);
    EEG = eeg_regepochs(EEG, 'recurrence', 2, 'limits', [-0.1 2], 'eventtype','new', 'extractepochs', 'on');
    % EEG = pop_epoch(EEG, {'new'}, [-0.1 2], 'epochinfo', 'yes');
    % EEG = pop_rmbase(EEG, [-100 0], []);
    % EEG = pop_rmdat(EEG, {'new'}, [0 2], 0);
    % save to .set
    EEG = pop_saveset(EEG, 'filename', outname, 'filepath', ''); 
end

% for i = 1 : 31
% 	fname = fullfile(set_path, sprintf('sub-%03d_task-rest_eeg.set', i));
% 	sprintf('------------------- Processing %s -------------------', fname);
% 	EEG = pop_loadset('filename', fname, 'filepath', '');
% end


% EEG = pop_rmdat(EEG, {'rsfi'}, [0 6.1], 0);
% EEG = pop_saveset(EEG,'filename','D:\EGI_DATA\EGI_REST_SET\sub-001_task-rest_pre.set','filepath','');

% EEG = eeg_regepochs(EEG, 'recurrence', 2, 'limits', [0 2], 'eventtype','10');%%重新分成两秒一段
% EEG = pop_saveset(EEG,'filename','D:\EGI_DATA\EGI_REST_SET\sub-001_task-rest_epo.set','filepath','');