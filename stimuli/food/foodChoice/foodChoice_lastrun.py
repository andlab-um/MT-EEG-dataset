#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2020.2.10),
    on 三月 30, 2021, at 01:12
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# set to True before start egi exp
netstation = False
recording = False


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2020.2.10'
expName = 'foodChoice'  # from the Builder filename that created this script
expInfo = {'姓名': '', '性别': '', '年龄': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['姓名'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\const\\OneDrive\\Desktop\\research\\psychopyProj\\1_mouse-egi\\food\\foodChoice\\foodChoice_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[2194, 1234], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='pix')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "welc"
welcClock = core.Clock()
rect_start = visual.Rect(
    win=win, name='rect_start',
    width=(150, 80)[0], height=(150, 80)[1],
    ori=0, pos=(0, -490),
    lineWidth=1, lineColor='black', lineColorSpace='rgb',
    fillColor='gray', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
start_btn = visual.TextStim(win=win, name='start_btn',
    text='开始',
    font='Songti SC',
    pos=(0, -490), height=50, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='Arabic',
    depth=-1.0);
welc_mouse = event.Mouse(win=win)
x, y = [None, None]
welc_mouse.mouseClock = core.Clock()
guide_image = visual.ImageStim(
    win=win,
    name='guide_image', 
    image='guide.png', mask=None,
    ori=0, pos=(0, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
if netstation:
    import egi.simple as egi
    ns = egi.Netstation()
    print("import pynetstation")
    # set ip address
    ns.connect("10.10.10.42", 55513)
    ns.BeginSession()
    print("connected to netstation")
    if recording:
        ns.StartRecording()
        print("start recording")

def send_to_NS(key_):
    if netstation:
        ns.sync()
        ns.send_event(key=key_)


# Initialize components for Routine "pause"
pauseClock = core.Clock()
pause_tip = visual.TextStim(win=win, name='pause_tip',
    text='请等待主试按下空格键后开始实验\n在此期间您可休息片刻',
    font='Songti SC',
    pos=(0, 0), height=50, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_start = keyboard.Keyboard()
isPause = False

# Initialize components for Routine "ready"
readyClock = core.Clock()
rect_ready = visual.Rect(
    win=win, name='rect_ready',
    width=(150, 80)[0], height=(150, 80)[1],
    ori=0, pos=(0, -490),
    lineWidth=1, lineColor='black', lineColorSpace='rgb',
    fillColor='gray', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
ready_btn = visual.TextStim(win=win, name='ready_btn',
    text='开始',
    font='Songti SC',
    pos=(0, -490), height=50, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='Arabic',
    depth=-1.0);
ready_mouse = event.Mouse(win=win)
x, y = [None, None]
ready_mouse.mouseClock = core.Clock()

# Initialize components for Routine "image"
imageClock = core.Clock()
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()
image_left = visual.ImageStim(
    win=win,
    name='image_left', 
    image='sin', mask=None,
    ori=0, pos=(-760, 390), size=(400, 300),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
image_right = visual.ImageStim(
    win=win,
    name='image_right', 
    image='sin', mask=None,
    ori=0, pos=(760, 390), size=(400, 300),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)

# Initialize components for Routine "display"
displayClock = core.Clock()
image_left_2 = visual.ImageStim(
    win=win,
    name='image_left_2', 
    image='sin', mask=None,
    ori=0, pos=(-760, 390), size=(400, 300),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
image_right_2 = visual.ImageStim(
    win=win,
    name='image_right_2', 
    image='sin', mask=None,
    ori=0, pos=(760, 390), size=(400, 300),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
rect = visual.Rect(
    win=win, name='rect',
    width=(400, 300)[0], height=(400, 300)[1],
    ori=0, pos=[0,0],
    lineWidth=10, lineColor='blue', lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1, depth=-3.0, interpolate=True)

# Initialize components for Routine "fixation"
fixationClock = core.Clock()
fixation_text = visual.TextStim(win=win, name='fixation_text',
    text='+',
    font='Songti SC',
    pos=(0, 0), height=100, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='Arabic',
    depth=0.0);

# Initialize components for Routine "thanks"
thanksClock = core.Clock()
text = visual.TextStim(win=win, name='text',
    text='感谢参与！',
    font='Songti SC',
    pos=(0, 0), height=50, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "welc"-------
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the welc_mouse
welc_mouse.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
welcComponents = [rect_start, start_btn, welc_mouse, guide_image]
for thisComponent in welcComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
welcClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "welc"-------
while continueRoutine:
    # get current time
    t = welcClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=welcClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *rect_start* updates
    if rect_start.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        rect_start.frameNStart = frameN  # exact frame index
        rect_start.tStart = t  # local t and not account for scr refresh
        rect_start.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(rect_start, 'tStartRefresh')  # time at next scr refresh
        rect_start.setAutoDraw(True)
    
    # *start_btn* updates
    if start_btn.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_btn.frameNStart = frameN  # exact frame index
        start_btn.tStart = t  # local t and not account for scr refresh
        start_btn.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_btn, 'tStartRefresh')  # time at next scr refresh
        start_btn.setAutoDraw(True)
    # *welc_mouse* updates
    if welc_mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        welc_mouse.frameNStart = frameN  # exact frame index
        welc_mouse.tStart = t  # local t and not account for scr refresh
        welc_mouse.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(welc_mouse, 'tStartRefresh')  # time at next scr refresh
        welc_mouse.status = STARTED
        welc_mouse.mouseClock.reset()
        prevButtonState = welc_mouse.getPressed()  # if button is down already this ISN'T a new click
    if welc_mouse.status == STARTED:  # only update if started and not finished!
        buttons = welc_mouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                for obj in [rect_start]:
                    if obj.contains(welc_mouse):
                        gotValidClick = True
                        welc_mouse.clicked_name.append(obj.name)
                if gotValidClick:  # abort routine on response
                    continueRoutine = False
    
    # *guide_image* updates
    if guide_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        guide_image.frameNStart = frameN  # exact frame index
        guide_image.tStart = t  # local t and not account for scr refresh
        guide_image.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(guide_image, 'tStartRefresh')  # time at next scr refresh
        guide_image.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in welcComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "welc"-------
for thisComponent in welcComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# store data for thisExp (ExperimentHandler)
thisExp.nextEntry()
thisExp.addData('guide_image.started', guide_image.tStartRefresh)
thisExp.addData('guide_image.stopped', guide_image.tStopRefresh)
# the Routine "welc" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
images = data.TrialHandler(nReps=2, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('trialVar.csv'),
    seed=None, name='images')
thisExp.addLoop(images)  # add the loop to the experiment
thisImage = images.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisImage.rgb)
if thisImage != None:
    for paramName in thisImage:
        exec('{} = thisImage[paramName]'.format(paramName))

for thisImage in images:
    currentLoop = images
    # abbreviate parameter names if possible (e.g. rgb = thisImage.rgb)
    if thisImage != None:
        for paramName in thisImage:
            exec('{} = thisImage[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "pause"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_start.keys = []
    key_start.rt = []
    _key_start_allKeys = []
    if images.thisN == 0 or images.thisN % 107 != 0:
        continueRoutine = False
    else:
        isPause = True
        if netstation and recording:
            ns.StopRecording()
            print("pause recording")
    
    # keep track of which components have finished
    pauseComponents = [pause_tip, key_start]
    for thisComponent in pauseComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    pauseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "pause"-------
    while continueRoutine:
        # get current time
        t = pauseClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=pauseClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *pause_tip* updates
        if pause_tip.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            pause_tip.frameNStart = frameN  # exact frame index
            pause_tip.tStart = t  # local t and not account for scr refresh
            pause_tip.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pause_tip, 'tStartRefresh')  # time at next scr refresh
            pause_tip.setAutoDraw(True)
        
        # *key_start* updates
        waitOnFlip = False
        if key_start.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_start.frameNStart = frameN  # exact frame index
            key_start.tStart = t  # local t and not account for scr refresh
            key_start.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_start, 'tStartRefresh')  # time at next scr refresh
            key_start.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_start.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_start.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_start.status == STARTED and not waitOnFlip:
            theseKeys = key_start.getKeys(keyList=['space'], waitRelease=False)
            _key_start_allKeys.extend(theseKeys)
            if len(_key_start_allKeys):
                key_start.keys = _key_start_allKeys[-1].name  # just the last key pressed
                key_start.rt = _key_start_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in pauseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "pause"-------
    for thisComponent in pauseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    images.addData('pause_tip.started', pause_tip.tStartRefresh)
    images.addData('pause_tip.stopped', pause_tip.tStopRefresh)
    if isPause:
        isPause = False
        if netstation and recording:
            ns.StartRecording()
            print("start recording")
    
    # the Routine "pause" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "ready"-------
    continueRoutine = True
    # update component parameters for each repeat
    # setup some python lists for storing info about the ready_mouse
    ready_mouse.clicked_name = []
    gotValidClick = False  # until a click is received
    win.mouseVisible = True
    send_to_NS(str(images.thisN).zfill(4))
    # keep track of which components have finished
    readyComponents = [rect_ready, ready_btn, ready_mouse]
    for thisComponent in readyComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    readyClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "ready"-------
    while continueRoutine:
        # get current time
        t = readyClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=readyClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *rect_ready* updates
        if rect_ready.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            rect_ready.frameNStart = frameN  # exact frame index
            rect_ready.tStart = t  # local t and not account for scr refresh
            rect_ready.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(rect_ready, 'tStartRefresh')  # time at next scr refresh
            rect_ready.setAutoDraw(True)
        
        # *ready_btn* updates
        if ready_btn.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ready_btn.frameNStart = frameN  # exact frame index
            ready_btn.tStart = t  # local t and not account for scr refresh
            ready_btn.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ready_btn, 'tStartRefresh')  # time at next scr refresh
            ready_btn.setAutoDraw(True)
        # *ready_mouse* updates
        if ready_mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            ready_mouse.frameNStart = frameN  # exact frame index
            ready_mouse.tStart = t  # local t and not account for scr refresh
            ready_mouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(ready_mouse, 'tStartRefresh')  # time at next scr refresh
            ready_mouse.status = STARTED
            ready_mouse.mouseClock.reset()
            prevButtonState = ready_mouse.getPressed()  # if button is down already this ISN'T a new click
        if ready_mouse.status == STARTED:  # only update if started and not finished!
            buttons = ready_mouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    for obj in [rect_ready]:
                        if obj.contains(ready_mouse):
                            gotValidClick = True
                            ready_mouse.clicked_name.append(obj.name)
                    if gotValidClick:  # abort routine on response
                        continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in readyComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "ready"-------
    for thisComponent in readyComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for images (TrialHandler)
    images.addData('ready_mouse.started', ready_mouse.tStart)
    images.addData('ready_mouse.stopped', ready_mouse.tStop)
    # the Routine "ready" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "image"-------
    continueRoutine = True
    # update component parameters for each repeat
    x_list = []
    y_list = []
    t_list = []
    mouse.setPos([0, -490])
    
    # set mark
    response_mark = 500
    send_to_NS("0400")
    # setup some python lists for storing info about the mouse
    mouse.clicked_name = []
    gotValidClick = False  # until a click is received
    image_left.setImage(left_image)
    image_right.setImage(right_image)
    # keep track of which components have finished
    imageComponents = [mouse, image_left, image_right]
    for thisComponent in imageComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    imageClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "image"-------
    while continueRoutine:
        # get current time
        t = imageClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=imageClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # get mouse track
        x_pos, y_pos = mouse.getPos()
        x_list.append(x_pos)
        y_list.append(y_pos)
        t_list.append(imageClock.getTime())
        
        # *mouse* updates
        if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse.frameNStart = frameN  # exact frame index
            mouse.tStart = t  # local t and not account for scr refresh
            mouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
            mouse.status = STARTED
            mouse.mouseClock.reset()
            prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
        if mouse.status == STARTED:  # only update if started and not finished!
            buttons = mouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    for obj in [image_left, image_right]:
                        if obj.contains(mouse):
                            gotValidClick = True
                            mouse.clicked_name.append(obj.name)
                    if gotValidClick:  # abort routine on response
                        continueRoutine = False
        
        # *image_left* updates
        if image_left.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            image_left.frameNStart = frameN  # exact frame index
            image_left.tStart = t  # local t and not account for scr refresh
            image_left.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(image_left, 'tStartRefresh')  # time at next scr refresh
            image_left.setAutoDraw(True)
        
        # *image_right* updates
        if image_right.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            image_right.frameNStart = frameN  # exact frame index
            image_right.tStart = t  # local t and not account for scr refresh
            image_right.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(image_right, 'tStartRefresh')  # time at next scr refresh
            image_right.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in imageComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "image"-------
    for thisComponent in imageComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('xTrajectory', x_list)
    thisExp.addData('yTrajectory', y_list)
    thisExp.addData('tTrajectory', t_list)
    
    # store data for images (TrialHandler)
    x, y = mouse.getPos()
    buttons = mouse.getPressed()
    if sum(buttons):
        # check if the mouse was inside our 'clickable' objects
        gotValidClick = False
        for obj in [image_left, image_right]:
            if obj.contains(mouse):
                gotValidClick = True
                mouse.clicked_name.append(obj.name)
    images.addData('mouse.x', x)
    images.addData('mouse.y', y)
    images.addData('mouse.leftButton', buttons[0])
    images.addData('mouse.midButton', buttons[1])
    images.addData('mouse.rightButton', buttons[2])
    if len(mouse.clicked_name):
        images.addData('mouse.clicked_name', mouse.clicked_name[0])
    images.addData('mouse.started', mouse.tStart)
    images.addData('mouse.stopped', mouse.tStop)
    images.addData('image_right.started', image_right.tStartRefresh)
    images.addData('image_right.stopped', image_right.tStopRefresh)
    # the Routine "image" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "display"-------
    continueRoutine = True
    routineTimer.add(1.000000)
    # update component parameters for each repeat
    image_left_2.setImage(left_image)
    image_right_2.setImage(right_image)
    if "image_left" in mouse.clicked_name:
        rect_pos = (-760, 390)
    else:
        rect_pos = (760, 390)
        response_mark += 1
    send_to_NS(str(response_mark).zfill(4))
    rect.setPos(rect_pos)
    # keep track of which components have finished
    displayComponents = [image_left_2, image_right_2, rect]
    for thisComponent in displayComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    displayClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "display"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = displayClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=displayClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *image_left_2* updates
        if image_left_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            image_left_2.frameNStart = frameN  # exact frame index
            image_left_2.tStart = t  # local t and not account for scr refresh
            image_left_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(image_left_2, 'tStartRefresh')  # time at next scr refresh
            image_left_2.setAutoDraw(True)
        if image_left_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > image_left_2.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                image_left_2.tStop = t  # not accounting for scr refresh
                image_left_2.frameNStop = frameN  # exact frame index
                win.timeOnFlip(image_left_2, 'tStopRefresh')  # time at next scr refresh
                image_left_2.setAutoDraw(False)
        
        # *image_right_2* updates
        if image_right_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            image_right_2.frameNStart = frameN  # exact frame index
            image_right_2.tStart = t  # local t and not account for scr refresh
            image_right_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(image_right_2, 'tStartRefresh')  # time at next scr refresh
            image_right_2.setAutoDraw(True)
        if image_right_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > image_right_2.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                image_right_2.tStop = t  # not accounting for scr refresh
                image_right_2.frameNStop = frameN  # exact frame index
                win.timeOnFlip(image_right_2, 'tStopRefresh')  # time at next scr refresh
                image_right_2.setAutoDraw(False)
        
        # *rect* updates
        if rect.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            rect.frameNStart = frameN  # exact frame index
            rect.tStart = t  # local t and not account for scr refresh
            rect.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(rect, 'tStartRefresh')  # time at next scr refresh
            rect.setAutoDraw(True)
        if rect.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > rect.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                rect.tStop = t  # not accounting for scr refresh
                rect.frameNStop = frameN  # exact frame index
                win.timeOnFlip(rect, 'tStopRefresh')  # time at next scr refresh
                rect.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in displayComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "display"-------
    for thisComponent in displayComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    images.addData('image_right_2.started', image_right_2.tStartRefresh)
    images.addData('image_right_2.stopped', image_right_2.tStopRefresh)
    win.mouseVisible = False
    
    
    # ------Prepare to start Routine "fixation"-------
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    fixationComponents = [fixation_text]
    for thisComponent in fixationComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    fixationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "fixation"-------
    while continueRoutine:
        # get current time
        t = fixationClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=fixationClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation_text* updates
        if fixation_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fixation_text.frameNStart = frameN  # exact frame index
            fixation_text.tStart = t  # local t and not account for scr refresh
            fixation_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_text, 'tStartRefresh')  # time at next scr refresh
            fixation_text.setAutoDraw(True)
        if fixation_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fixation_text.tStartRefresh + np.around(np.random.uniform(0.8, 1.5), 3)-frameTolerance:
                # keep track of stop time/frame for later
                fixation_text.tStop = t  # not accounting for scr refresh
                fixation_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fixation_text, 'tStopRefresh')  # time at next scr refresh
                fixation_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "fixation"-------
    for thisComponent in fixationComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "fixation" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 2 repeats of 'images'


# ------Prepare to start Routine "thanks"-------
continueRoutine = True
routineTimer.add(2.000000)
# update component parameters for each repeat
if netstation:
    if recording:
        ns.StopRecording()
    ns.EndSession()
    ns.disconnect()

# keep track of which components have finished
thanksComponents = [text]
for thisComponent in thanksComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
thanksClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "thanks"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = thanksClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=thanksClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text* updates
    if text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        text.frameNStart = frameN  # exact frame index
        text.tStart = t  # local t and not account for scr refresh
        text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
        text.setAutoDraw(True)
    if text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text.tStartRefresh + 2-frameTolerance:
            # keep track of stop time/frame for later
            text.tStop = t  # not accounting for scr refresh
            text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(text, 'tStopRefresh')  # time at next scr refresh
            text.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in thanksComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "thanks"-------
for thisComponent in thanksComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('text.started', text.tStartRefresh)
thisExp.addData('text.stopped', text.tStopRefresh)

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
