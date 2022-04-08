clear;clc;
eeglab nogui;

%% set path
root_path = fullfile('..', '..', 'EGI_DATA');
src_path = fullfile(root_path, 'EGI_SRC');
set_path = fullfile(root_path, 'EGI_SET');

if exist(set_path, 'dir')
    rmdir(set_path, 's');
end

mkdir(set_path);

% set task names
resting = "resting";
foodtask = "foodchoice";
wordtask = "wordchoice";
imagetask = "imagechoice";

% delete(gcp('nocreate'));
% parpool(4);

sub_paths = dir(fullfile(src_path, 'sub*'));
% subject loop
for i = 1:length(sub_paths)
    sub = sub_paths(i).name;
    % task loop
    for task = [resting foodtask wordtask imagetask]
        % disp(['-------------------------------' char(sub) ' -> ' char(task) '-------------------------------']);
        % get paths
        mff_path = fullfile(src_path, sub, 'eeg', [sub '_task-' char(task) '_eeg.mff']);
        new_path = fullfile(set_path, sub, 'eeg', [sub '_task-' char(task) '_eeg.set']);

        if ~exist(fullfile(set_path, sub, 'eeg'), 'dir')
            mkdir(fullfile(set_path, sub, 'eeg'));
        end

        % read mff
        EEG = pop_mffimport(mff_path, 'code');
        EEG = eeg_checkset(EEG);
        % save as .set
        EEG = pop_saveset(EEG, 'filename', new_path, 'savemode', 'twofiles');
        EEG = eeg_checkset(EEG);
        disp(mff_path);
    end

end
