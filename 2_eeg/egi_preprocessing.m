clear;clc;
eeglab;

%% set path
root_path = 'D:\\EGI_DATA';
mff_path = fullfile(root_path, 'EGI_FMT');
set_path = fullfile(root_path, 'EGI_SET');

% set task names
wordtask = "wordchoice";
imagetask = "imagechoice";
wmtask = "wordimagematch";
rest = "rest";

fileID = fopen('exp.txt','w');

%% start
for i = 10 : 10
    for task = (wordtask)
        fname = fullfile(mff_path, sprintf('sub-%03d', i), 'eeg', sprintf('sub-%03d_task-%s_eeg.mff', i, task));
        outname = fullfile(set_path, sprintf('sub-%03d', i), 'eeg', sprintf('sub-%03d_task-%s_eeg.set', i, task));
        % create target folder if not exist
        if (~exist(fullfile(set_path, sprintf('sub-%03d', i), 'eeg'), 'dir'))
            mkdir(fullfile(set_path, sprintf('sub-%03d', i), 'eeg'));
        end
        sprintf('------------------- Processing %s -------------------', fname);
        %% import data
        EEG = pop_mffimport({fname}, {'code'});
        %% load channel location
        % EEG = pop_chanedit(EEG, 'load', {location_path, 'filetype', 'autodetect'}, 'changefield', {132, 'labels', 'E129'});
        %% resample
        EEG = pop_resample(EEG, 250);
        %% filter
        EEG = pop_eegfiltnew(EEG, 'locutoff', 1);
        EEG = pop_eegfiltnew(EEG, 'hicutoff', 30);
        %% remove line noise
        % EEG = pop_eegfiltnew(EEG, 'locutoff', 48, 'hicutoff', 52, 'revfilt', 1);
        % EEG = pop_cleanline(EEG, 'bandwidth', 2, 'chanlist', [1:129], 'computepower', 1, 'linefreqs', 50, 'normSpectrum', 0, 'p', 0.01, 'pad', 2, ...
        %                     'plotfigures', 0, 'scanforlines', 1, 'sigtype', 'Channels', 'tau', 100, 'verb', 1, 'winsize', 4, 'winstep', 1);
        %% remove useless channels
        % EEG = pop_select(EEG, 'nochannel', {'E125', 'E128', 'E43', 'E48', 'E49', 'E56', 'E63', ...
        %                 'E68', 'E73', 'E81', 'E88', 'E94', 'E99', 'E107', 'E113', 'E120', 'E119', ...
        %                 'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E121', 'E126', 'E127'});
        %% reject bad channels
        % remove E129 temporarily
        ch_E129 = EEG.chanlocs(end);
        assert(strcmp(ch_E129.labels, 'E129') == 1, 'Some channel error.')
        EEG = pop_select(EEG, 'nochannel', {'E129'});
        % save EEG (channel information)
        originalEEG = EEG;
        EEG = pop_clean_rawdata(EEG, 'FlatlineCriterion', 5, 'ChannelCriterion', 0.8, 'LineNoiseCriterion', 4, 'Highpass', 'off', ...
                                'BurstCriterion', 'off', 'WindowCriterion', 'off', 'BurstRejection', 'off', 'Distance', 'Euclidian');
        fprintf(fileID, 'sub-%03d, %d, removed bad channel: %d\r\n', i, task, originalEEG.nbchan-EEG.nbchan);
        %% interpolate channels
        EEG = pop_interp(EEG, originalEEG.chanlocs, 'spherical');
        %% re-reference
        % add E129 back
        EEG.chanlocs(end+1) = ch_E129;
        EEG.nbchan = EEG.nbchan + 1;
        EEG.data(end+1, :) = zeros(1, EEG.pnts);
        EEG = pop_reref(EEG, []);
        % %% correct bad data periods by ASR
        % % TODO: change criteria or options
        % EEG = pop_clean_rawdata(EEG, 'FlatlineCriterion', 'off', 'ChannelCriterion', 'off', 'LineNoiseCriterion', 'off', 'Highpass', ...
        %                         'off', 'BurstCriterion', 20, 'WindowCriterion', 'off', 'BurstRejection', 'on', 'Distance', 'Euclidian');
        % %% re-reference
        % EEG = pop_reref(EEG, []);

        %% ICA
        % downsample for speed up
        EEG_forICA = pop_resample(EEG, 100);
        % TODO: need to optimize
        EEG_forICA = pop_runica(EEG_forICA, 'icatype', 'runica', 'extended', 1);
        % EEG_forICA = pop_runica(EEG_forICA, 'icatype', 'runica', 'extended', 1, 'interrupt', 'on', 'pca', 50);
        EEG.icaweights = EEG_forICA.icaweights;
        EEG.icasphere  = EEG_forICA.icasphere;
        EEG = eeg_checkset(EEG, 'ica');
        
        % EEG = pop_runica(EEG, 'icatype', 'runica', 'extended', 1);

        %% remove components by ICLabel
        EEG = pop_iclabel(EEG, 'default');
        % eye: >0.9, muscle: >0.9
        EEG = pop_icflag(EEG, [NaN NaN; 0.9 1; 0.9 1; NaN NaN; NaN NaN; NaN NaN; NaN NaN]);
        EEG = pop_subcomp(EEG, [], 0, 0);

        %% epoch data
        EEG = pop_epoch(EEG, {'0400' '0401' '0402' '0403'}, [-0.2 0.8], 'newname', sprintf(outname(1:end-4), '_epochs'), 'epochinfo', 'yes');
        EEG = pop_rmbase(EEG, [-200 0], []);

        %% save to .set
        EEG = pop_saveset(EEG, 'filename', outname, 'filepath', '');
        % [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0, 'setname', 'clean_epoch','gui','off');
        % eeglab redraw;
    end
end

fclose(fileID);

% EEG = pop_rmdat(EEG, {'rsfi'}, [0 6.1], 0);
% EEG = pop_saveset(EEG,'filename','D:\EGI_DATA\EGI_REST_SET\sub-001_task-rest_pre.set','filepath','');

% EEG = eeg_regepochs(EEG, 'recurrence', 2, 'limits', [0 2], 'eventtype','10');
% EEG = pop_saveset(EEG,'filename','D:\EGI_DATA\EGI_REST_SET\sub-001_task-rest_epo.set','filepath','');

% For rest data
% EEG = eeg_regepochs(EEG, 'recurrence', 2, 'limits', [-0.1 2], 'eventtype', 'new', 'extractepochs', 'on');