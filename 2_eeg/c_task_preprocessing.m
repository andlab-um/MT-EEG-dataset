% ref: https://sccn.ucsd.edu/wiki/Makoto%27s_useful_EEGLAB_code
clear;clc;
eeglab nogui;
% gpu forward compatibility issue
setenv('CUDA_CACHE_MAXSIZE', '536870912');

%% set path
output_path = fullfile('..', 'data');
% change to your BIDS path
bids_path = fullfile('..', '..',  'EGI_DATA', 'EGI_BIDS');
task_eeg_path = fullfile(output_path, 'EGI_TASK');
log_path = fullfile(output_path, 'eeg_log');
if exist(task_eeg_path, 'dir')
    rmdir(task_eeg_path, 's');
end
if exist(log_path, 'dir')
    rmdir(log_path, 's');
end
mkdir(log_path);

% channel location file, get from MNE (python) package
montage_path = fullfile('..', 'assets', 'GSN-HydroCel-129.sfp');

% set task names
foodtask = "foodchoice";
wordtask = "wordchoice";
imagetask = "imagechoice";

% log file
fileID = fopen(fullfile(output_path, 'exp_log.txt'), 'w');

%% start
delete(gcp('nocreate'));
parpool(16);
for task = [ foodtask wordtask imagetask ]
    fprintf(fileID, '\n-------------------------------- %s --------------------------------\n', task);
    for i = 1 : 31
        fprintf(fileID, 'sub-%02d, ', i);
        f_path = fullfile(bids_path, sprintf('sub-%02d', i), 'eeg', sprintf('sub-%02d_task-%s_eeg.set', i, task));
        outname = sprintf('sub-%02d_task-%s_eeg.set', i, task);

        sprintf('------------------- Processing %s -------------------', f_path);
        %% import data
        % EEG = pop_mffimport(f_path, 'type');
        EEG = pop_loadset(f_path);

        %% load channel location
        EEG = pop_chanedit(EEG, 'load', {montage_path, 'filetype', 'autodetect'}, 'changefield', {132, 'labels', 'E129'});

        %% resample
        EEG = pop_resample(EEG, 100);

        %% filter
        EEG = pop_eegfiltnew(EEG, 'locutoff', 0.1);
        EEG = pop_eegfiltnew(EEG, 'hicutoff', 30);

        % %% ! 0_save files
        % dir_path = fullfile(task_eeg_path, '0_ds_fil', sprintf('sub-%02d', i));
        % if (~exist(dir_path, 'dir'))
        %     mkdir(dir_path);
        % end
        % EEG = pop_saveset(EEG, 'filename', outname, 'filepath', dir_path, 'savemode', 'onefile');
        
        %% detect 20Hz noise
        fig = figure;
        [spectra, freq] = pop_spectopo(EEG, 1, [0 EEG.xmax*1000], 'EEG', 'percent', 50, 'freq', [6 10 22], 'freqrange',[0.1 30],'electrodes','off');
        % save spectopo figure
        saveas(fig, fullfile(log_path, sprintf('task-%s_sub-%02d_eeg', task, i)), 'png');
        close;
        [pks, locs] = findpeaks(mean(spectra), freq, 'MinPeakProminence', 2);
        % fprintf(fileID, 'sub-%02d, peaks: %d, locs: %d\n', i, pks, locs);
        if any(locs==20)
            fprintf(fileID, '20Hz noise, ');
            % continue;
        end

        %% remove useless channels
        EEG = pop_select(EEG, 'nochannel', {'E125', 'E128', 'E43', 'E48', 'E49', 'E56', 'E63', ...
                        'E68', 'E73', 'E81', 'E88', 'E94', 'E99', 'E107', 'E113', 'E120', 'E119', ...
                        'E1', 'E8', 'E14', 'E17', 'E21', 'E25', 'E32', 'E38', 'E121', 'E126', 'E127'});

        %% extract useful events
        % stimulus mark: 0400-0403
        stim_mark = ["0400", "0401", "0402", "0403"];
        % correct response mark
        if task == foodtask
            resp_mark = ["0500", "0501"];
        else
            resp_mark = ["0500", "0503", "0505", "0506"];
        end
        select_list = [];
        correct_trials = 0;
        for index = 1 : length(EEG.event)-1
            % if this mark is a stimulus mark and next mark is a (correct) response mark
            if any(find(stim_mark == EEG.event(index).type)) && any(find(resp_mark == EEG.event(index+1).type))
                % add stim mark and response mark for correct trials (add all for foodchoice)
                select_list(end + 1) = index;
                select_list(end + 1) = index + 1;
                correct_trials = correct_trials + 1;
            end
        end
        % save selected events
        EEG = pop_selectevent(EEG, 'event', select_list, 'deleteevents', 'on');
        % Check all events for consistency
        EEG = eeg_checkset(EEG, 'eventconsistency');

        %% remove artifacts
        % remove E129 temporarily
        ch_E129 = EEG.chanlocs(end);
        assert(strcmp(ch_E129.labels, 'E129') == 1, 'Some channel error.');
        EEG = pop_select(EEG, 'nochannel', {'E129'});
        % save EEG (channel information)
        originalEEG = EEG;
        % Remove bad channels
        EEG = pop_clean_rawdata(EEG, 'FlatlineCriterion', 5, 'ChannelCriterion', 0.8, 'LineNoiseCriterion', 4, 'Highpass', 'off', ...
                                'BurstCriterion', 'off', 'WindowCriterion', 'off', 'BurstRejection', 'off', 'Distance', 'Euclidian');
        fprintf(fileID, 'reserved bad channel: %d/%d, ', EEG.nbchan, originalEEG.nbchan);
        %% interpolate channels
        EEG = pop_interp(EEG, originalEEG.chanlocs, 'spherical');
        
        %% re-reference
        % add E129 back
        EEG.chanlocs(end+1) = ch_E129;
        EEG.nbchan = EEG.nbchan + 1;
        EEG.data(end+1, :) = zeros(1, EEG.pnts);
        EEG = pop_reref(EEG, []);

        % reject bad data periods by ASR
        EEG = pop_clean_rawdata(EEG, 'FlatlineCriterion', 'off', 'ChannelCriterion', 'off', 'LineNoiseCriterion', 'off', 'Highpass', ...
        'off', 'BurstCriterion', 100, 'WindowCriterion', 'off', 'BurstRejection', 'on', 'Distance', 'Euclidian');

        %% ICA
        % TODO: need to optimize
        EEG = pop_runica(EEG, 'icatype', 'runica', 'extended', 1);
        % EEG = pop_runica(EEG, 'icatype', 'runica', 'extended', 1, 'pca', 50);
        ica_components = size(EEG.icaweights, 1);
        %% remove components by ICLabel
        EEG = pop_iclabel(EEG, 'default');
        % flag different noises. [Brain, Muscle, Eye, Heart, Line Noise, Channel Noise, Other]
        EEG = pop_icflag(EEG, [NaN NaN; 0.7 1; 0.7 1; 0.7 1; 0.7 1; 0.7 1; NaN NaN]);
        EEG = pop_subcomp(EEG, [], 0, 0);
        fprintf(fileID, 'reserved components: %d/%d, ', size(EEG.icaweights, 1), ica_components);
        %% save preprocessed continuous files
        dir_path = fullfile(task_eeg_path, sprintf('sub-%02d', i));
        if (~exist(dir_path, 'dir'))
            mkdir(dir_path);
        end
        EEG = pop_saveset(EEG, 'filename', outname, 'filepath', dir_path, 'savemode', 'onefile');

        %% epoch data
        EEG = pop_epoch(EEG, cellstr(stim_mark), [-0.2 0.8], 'newname', outname(1:end-4), 'epochinfo', 'yes');
        % baseline correction
        EEG = pop_rmbase(EEG, [-200 0], []);
        fprintf(fileID, 'reserved trials: %d/%d\n', EEG.trials, correct_trials);
        % % [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0, 'setname', 'test','gui','off');
        % % eeglab redraw;
    end
end

fclose(fileID);
