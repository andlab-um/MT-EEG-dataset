%% Read the data and perform preprocessing
clear all; close all; clc

ConDir = 'D:\\EGI_DATA\\EGI_REST_SET'
SavePath = 'D:\\EGI_DATA\\EGI_REST_MS'
group_name = 'resting-state'
location_path = 'C:\\Users\\const\\MATLAB\\eeglab2021.0\\sample_locs\\GSN129.sfp' 

ConIndex = [];

DirCon = dir(fullfile(ConDir,'*.set'));  %%%% find all the set file in your folder
FileNamesCon = {DirCon.name};

% Read the data and preprocess
eeglab
for f = 1:numel(FileNamesCon)
    EEG = pop_loadset(FileNamesCon{f}, ConDir); 
    setname = strrep(FileNamesCon{f},'.set',''); 
    [ALLEEG, EEG, CURRENTSET] = pop_newset(ALLEEG, EEG, 0,'setname',setname,'gui','off'); 
    % EEG = pop_chanedit(EEG, 'load', {location_path, 'filetype', 'autodetect'}, 'changefield', {132, 'labels', 'E129'});
    % EEG = pop_reref( EEG, []); % Make things average reference
    % EEG = pop_eegfiltnew(EEG, 2, 20, [], 0, [], 0);
    EEG.group = group_name;
    ALLEEG = eeg_store(ALLEEG, EEG, CURRENTSET);
    ConIndex = [ConIndex CURRENTSET]; 
end

eeglab redraw

%% Cluster the stuff
ClustPars = struct('MinClasses', 3, 'MaxClasses', 6, 'GFPPeaks', 1, 'IgnorePolarity', 1, ...
                    'MaxMaps', Inf, 'Restarts', 5, 'UseAAHC', 2, 'Normalize', 1);

% Loop across all subjects to identify the individual clusters
for i = 1:numel(ConIndex) 
    tmpEEG = eeg_retrieve(ALLEEG,ConIndex(i)); % the EEG we want to work with
    fprintf(1,'Clustering dataset %s (%i/%i)\n',tmpEEG.setname,i,numel(ConIndex)); % Some info for the impatient user
    tmpEEG = pop_FindMSTemplates(tmpEEG, ClustPars, 0, 0); % This is the actual clustering within subjects
    ALLEEG = eeg_store(ALLEEG, tmpEEG, ConIndex(i)); % Done, we just need to store this
end

eeglab redraw

%% Now we combine the microstate maps across subjects and edit the mean
EEG = pop_CombMSTemplates(ALLEEG, ConIndex, 0, 0, strcat('GrandMean', group_name));
[ALLEEG, EEG, CURRENTSET] = pop_newset(ALLEEG, EEG, numel(ALLEEG)+1, 'gui', 'off'); % Make a new set
[ALLEEG,EEG] = pop_ShowIndMSMaps(EEG, 4, 1, ALLEEG); % Here, we go interactive to allow the user to put the classes in the canonical order
[ALLEEG,EEG, CURRENTSET] = eeg_store(ALLEEG, EEG, CURRENTSET); % and store it
GrandMeanConIndex = CURRENTSET; % And keep track of it

eeglab redraw

%% And we sort things out over means and subjects
ALLEEG = pop_SortMSTemplates(ALLEEG, ConIndex, 0, GrandMeanConIndex); 

eeglab redraw

%% eventually save things
for f = 1:numel(ALLEEG)
    EEG = eeg_retrieve(ALLEEG, f);
    fname = [EEG.setname,'.set'];
    pop_saveset( EEG, 'filename',fname,'filepath',SavePath);
end

%% fitting the maps
fitting_gfp = inputdlg('Fitting based on GFP peaks? True = 1 False = 0');
fitting_gfp = str2num(fitting_gfp{1});
FitPars = struct('nClasses',4,'lambda',1,'b',30,'PeakFit',fitting_gfp, 'BControl',true);

% Using the individual templates
pop_QuantMSTemplates(ALLEEG, ConIndex, 0, FitPars, [], fullfile(SavePath,'ResultsFromIndividualTemplates.csv'));

% And using the grand mean template
pop_QuantMSTemplates(ALLEEG, ConIndex, 1, FitPars, GrandMeanConIndex, fullfile(SavePath,'ResultsFromGrandGrandMeanTemplate.csv'));


