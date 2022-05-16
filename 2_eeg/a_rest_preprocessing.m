clear;clc;
eeglab nogui;

%% set path
% change bids_path to your BIDS path
bids_path = fullfile('F:\', 'EGI_DATA', 'EGI_BIDS');
output_path = fullfile('..', 'data');
eeg_preproc_path = fullfile(output_path, 'EGI_PROC');

% channel location file, get from MNE (python) package
montage_path = fullfile('..', 'assets', 'GSN-HydroCel-129.sfp');

for i = 1:31
    fname = fullfile(bids_path, sprintf('sub-%02d', i), 'eeg', sprintf('sub-%02d_task-resting_eeg.set', i));
    outname = sprintf('sub-%02d_task-resting_eeg.set', i);
    % sprintf('------------------- Processing %s -------------------', fname);
    % import data
    % EEG = pop_mffimport({fname}, {'code'});
    EEG = pop_loadset(fname);
    % load channel location
    EEG = pop_chanedit(EEG, 'load', {montage_path, 'filetype', 'autodetect'}, 'changefield', {132, 'labels', 'E129'});
    % resample
    EEG = pop_resample(EEG, 250);
    % filter
    EEG = pop_eegfiltnew(EEG, 'locutoff', 2);
    EEG = pop_eegfiltnew(EEG, 'hicutoff', 20);
    % no need remove line noise since line frequency is 50Hz
    % remove useless channels
    EEG = pop_select(EEG, 'nochannel', {'E125', 'E128', 'E43', 'E48', 'E49', 'E56', 'E63', ...
                        'E68', 'E73', 'E81', 'E88', 'E94', 'E99', 'E107', 'E113', 'E120', 'E119', ...
                            'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E121', 'E126', 'E127'});
    % remove E129 temporarily
    ch_E129 = EEG.chanlocs(end);
    assert(strcmp(ch_E129.labels, 'E129') == 1, 'Some channel error.');
    EEG = pop_select(EEG, 'nochannel', {'E129'});
    % reject bad channels
    originalEEG = EEG;
    EEG = pop_clean_rawdata(EEG, 'FlatlineCriterion', 5, 'ChannelCriterion', 0.8, 'LineNoiseCriterion', 4, 'Highpass', 'off', ...
        'BurstCriterion', 'off', 'WindowCriterion', 'off', 'BurstRejection', 'off', 'Distance', 'Euclidian');
    % interpolate channels
    EEG = pop_interp(EEG, originalEEG.chanlocs, 'spherical');
    % add E129 back
    EEG.chanlocs(end + 1) = ch_E129;
    EEG.nbchan = EEG.nbchan + 1;
    EEG.data(end + 1, :) = zeros(1, EEG.pnts);
    % re-reference
    EEG = pop_reref(EEG, []);
    % correct bad data periods by ASR
    EEG = pop_clean_rawdata(EEG, 'FlatlineCriterion', 'off', 'ChannelCriterion', 'off', 'LineNoiseCriterion', 'off', 'Highpass', ...
    'off', 'BurstCriterion', 20, 'WindowCriterion', 'off', 'BurstRejection', 'off', 'Distance', 'Euclidian');
    % re-reference
    EEG = pop_reref(EEG, []);
    % save 0-6s data after rsfi
    EEG = pop_rmdat(EEG, {'rsfi'}, [-0.1 6], 0);
    EEG = eeg_regepochs(EEG, 'recurrence', 2, 'limits', [-0.1 2], 'eventtype', 'new', 'extractepochs', 'on');
    % save to .set
    dir_path = fullfile(eeg_preproc_path, sprintf('sub-%02d', i));

    if ~exist(dir_path, 'dir')
        mkdir(dir_path);
    end

    EEG = pop_saveset(EEG, 'filename', outname, 'filepath', dir_path, 'savemode', 'onefile');
end
