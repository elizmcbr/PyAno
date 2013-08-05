#   15-110 Final Project
#
#   PyAno: The Python-based piano
#
#
#   WRITTEN BY (NAME & ANDREW ID): Elizabeth Davis (emd1)
#
#   
#   
#   15-110 section: A
#

from Tkinter import *
import os
import pygame
from pygame.locals import *

# Responds to a key being pressed, either displaying the menu,
# toggling key display, switching octaves, or playing notes.
# Parameters:
#    event: event that just occurred (key pressed)
# Returns nothing
def keyPressed(event):
    canvas = event.widget.canvas
    keySymListWhite = canvas.data["keySymListWhite"]
    keySymListBlack = canvas.data["keySymListBlack"]
    allPitches = canvas.data["allPitches"]
    keys = canvas.data["keys"]
    if (event.keysym == "Up"):
        toggleOctave(canvas, +1)
    elif (event.keysym == "Down"):
        toggleOctave(canvas, -1)
    elif (event.keysym == "h"):
        canvas.data["showKeySymMode"] = not canvas.data["showKeySymMode"]
    elif (event.keysym == "m"):
        canvas.data["helpClicked"] = False
    elif (event.keysym == "x"):
        sys.exit()
    elif (((event.keysym in keySymListWhite) or
          (event.keysym in keySymListBlack)) and
          (canvas.data["helpClicked"] == False)):
        for key in keys:
            theKey = keys[key]
            if (theKey["keySym"] == event.keysym):
                theKey["playing"] = True
                playPitch(canvas, key)
    redrawAll(canvas)

# Responds to a key being released, pertaining to notes being
# played. Ends their sounding.
# Parameters:
#    event: event that just occurred (key released)
# Returns nothing
def keyReleased(event):
    canvas = event.widget.canvas
    keySymListWhite = canvas.data["keySymListWhite"]
    keySymListBlack = canvas.data["keySymListBlack"]
    allPitches = canvas.data["allPitches"]
    keys = canvas.data["keys"]
    if (((event.keysym in keySymListWhite) or
        (event.keysym in keySymListBlack)) and
        (canvas.data["helpClicked"] == False)):
        for key in keys:
            theKey = keys[key]
            if (theKey["keySym"] == event.keysym):
                theKey["playing"] = False
                playPitch(canvas, key)
    redrawAll(canvas)

# Responds to the mouse being clicked, pertaining to recording,
# playing back, or displaying the help screen.
# Parameters:
#    event: event that just occurred (mouse clicked)
# Returns nothing
def mousePressed(event):
    canvas = event.widget.canvas
    xCoord = event.x
    yCoord = event.y
    canvas.data["lastClickCoords"] = (xCoord, yCoord)
    buttonClicked(canvas, xCoord, yCoord)
    redrawAll(canvas)

# Responds to the mouse button being released, which is important 
# for functions of the keyboard such as playback, stop, and record.
# Parameters:
#    event: event that just occurred (mouse button released)
# Returns nothing
def mouseReleased(event):
    canvas = event.widget.canvas
    xCoord = canvas.data["lastClickCoords"][0]
    yCoord = canvas.data["lastClickCoords"][1]
    buttonReleased(canvas, xCoord, yCoord)
    redrawAll(canvas)

# Redraws the canvas after an event occurs.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def redrawAll(canvas):
    canvas.delete(ALL)
    keys = canvas.data["keys"]
    colorKey(canvas)
    drawBackground(canvas)
    drawButtons(canvas)
    drawWhites(canvas)
    drawBlacks(canvas)
    displayOctave(canvas)
    if (canvas.data["helpClicked"] == True):
        drawHelpScreen(canvas)

# Initially draws the background, piano, and buttons.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def loadPiano(canvas):
    drawBackground(canvas)
    drawButtons(canvas)
    loadWhiteKeys(canvas)
    loadBlackKeys(canvas)
    colorKey(canvas)

# Draws the white keys and (if in showKeyMode) their
# corresponding keyboard buttons. Also draws them in
# color corresponding to their state as being played or not.
# Parameters:
#     canvas: canvas where the data dictionary is stored
# Returns Nothing
def drawWhites(canvas):
    keys = canvas.data["keys"]
    showKeySymMode = canvas.data["showKeySymMode"]
    for key in keys:
        theKey = keys[key]
        if theKey["type"] == "white":
            left = theKey["left"]
            top = theKey["top"]
            right = theKey["right"]
            bottom = theKey["bottom"]
            length = bottom - top
            textX = (left + right) / 2
            textY = bottom - (length / 8)
            color = theKey["fill"]
            canvas.create_rectangle(left, top, right, bottom,
                                    fill = color)
            if (showKeySymMode == True):
                keySym = theKey["keySym"]
                if keySym == "bracketleft":
                    keySym = "["
                elif keySym == "bracketright":
                    keySym = "]"
                elif keySym == "backslash":
                    keySym = "\\"
                canvas.create_text(textX, textY, text=keySym)

# Draws the black keys and (if in showKeyMode) their
# corresponding keyboard buttons. Also draws them in
# color corresponding to their state as being played or not.
# Parameters:
#     canvas: canvas where the data dictionary is stored
# Returns Nothing            
def drawBlacks(canvas):
    keys = canvas.data["keys"]
    showKeySymMode = canvas.data["showKeySymMode"]
    for key in keys:
        theKey = keys[key]
        if theKey["type"] == "black":
            left = theKey["left"]
            top = theKey["top"]
            right = theKey["right"]
            bottom = theKey["bottom"]
            length = bottom - top
            textX = (left + right) / 2
            textY = bottom - (length / 8)
            color = theKey["fill"]
            canvas.create_rectangle(left, top, right, bottom,
                                    fill = color)
            if (showKeySymMode == True):
                keySym = theKey["keySym"]
                if keySym == "minus":
                    keySym = "-"
                canvas.create_text(textX, textY, text=keySym, fill="white")                

# Initially draws the white keys and sets their attributes
# involving coordinates, keysym, octave range, etc.
# "pitch" is the key's pitch relative to the surrounding keys.
# "globalPitch" is the key's pitch relative to all possible pitches.
# Parameters:
#     canvas: canvas where the data dictionary is stored
# Returns Nothing              
def loadWhiteKeys(canvas):
    keys = canvas.data["keys"]
    margin = canvas.data["margin"]
    whiteKeys = canvas.data["whiteKeys"]
    whiteKeyStart = canvas.data["whiteKeyStart"]
    whiteKeyWidth = canvas.data["whiteKeyWidth"]
    blackKeyWidth = canvas.data["blackKeyWidth"]
    whiteKeyHeight = canvas.data["whiteKeyHeight"]
    blackKeyHeight = canvas.data["blackKeyHeight"]
    whiteDefaultFill = canvas.data["whiteDefaultFill"]
    outlineFill = canvas.data["outlineFill"]
    keySymListWhite = canvas.data["keySymListWhite"]
    octave = canvas.data["baseOctave"]
    octaveCount = 0
    for i in range(whiteKeys):
        key = {}
        #defines pitch as somewhere between A and G
        pitch = str(chr(ord('g') - ((4 - i) % 7)))
        left = whiteKeyStart + i*whiteKeyWidth
        top = whiteKeyStart
        right = whiteKeyStart + (i + 1) * whiteKeyWidth
        bottom = whiteKeyStart + whiteKeyHeight
        #fill in dictionary of pitches and space
        keyNumber = str(i)
        if keyNumber not in keys:
            key["pitch"] = pitch + str(octaveCount)
            key["globalPitch"] = pitch + str(octaveCount + octave)
            key["left"] = left
            key["top"] = top
            key["right"] = right
            key["bottom"] = bottom
            key["type"] = "white"
            key["playing"] = False
            key["fill"] = whiteDefaultFill
            key["keySym"] = keySymListWhite[i]
            key["soundActivated"] = False
            key["playStart"] = 0
            key["playStop"] = 0
            keys[str(i)] = key
        canvas.create_rectangle(left, top, right, bottom,
                                outline=outlineFill,
                                fill=whiteDefaultFill)
        #determines if we've cycled through an octave
        if ((i + 1) % 7) == 0:
            octaveCount += 1

# Initially draws the black keys and sets their attributes
# involving coordinates, keysym, octave range, etc.
# "pitch" is the key's pitch relative to the surrounding keys.
# "globalPitch" is the key's pitch relative to all possible pitches.
# Parameters:
#     canvas: canvas where the data dictionary is stored
# Returns nothing         
def loadBlackKeys(canvas):
    keys = canvas.data["keys"]
    whiteKeys = canvas.data["whiteKeys"]
    blackKeys = canvas.data["blackKeys"]
    octaveWidth = canvas.data["octaveWidth"]
    octaves = canvas.data["octaves"]
    blackKeyWidth = canvas.data["blackKeyWidth"]
    blackKeyHeight = canvas.data["blackKeyHeight"]
    whiteKeyStart = canvas.data["whiteKeyStart"]
    blackKeyStartX = canvas.data["blackKeyStartX"]
    blackKeyStartY = canvas.data["blackKeyStartY"]
    singleKeyGap = canvas.data["singleKeyGap"]
    doubleKeyGap = canvas.data["doubleKeyGap"]
    blackDefaultFill = canvas.data["blackDefaultFill"]
    outlineFill = canvas.data["outlineFill"]
    keySymListBlack = canvas.data["keySymListBlack"]
    octave = canvas.data["baseOctave"]
    octaveCount = 0
    for i in range(blackKeys):
        key = {}
        top = blackKeyStartY
        bottom = blackKeyStartY + blackKeyHeight
        if (i % (blackKeys / octaves) == 0):
                left = (octaveCount * octaveWidth + blackKeyStartX)
                key["pitch"] = "cs" + str(octaveCount)
                key["globalPitch"] = "cs" + str(octaveCount + octave)
        elif (i % (blackKeys / octaves) == 1):
                left = (octaveCount * octaveWidth + blackKeyStartX +
                        singleKeyGap + blackKeyWidth)
                key["pitch"] = "ds" + str(octaveCount)
                key["globalPitch"] = "ds" + str(octaveCount + octave)
        elif (i % (blackKeys / octaves) == 2):
                left = (octaveCount * octaveWidth + blackKeyStartX +
                        singleKeyGap + blackKeyWidth * 2 + doubleKeyGap)
                key["pitch"] = "fs" + str(octaveCount)
                key["globalPitch"] = "fs" + str(octaveCount + octave)
        elif (i % (blackKeys / octaves) == 3):
                left = (octaveCount * octaveWidth + blackKeyStartX +
                        singleKeyGap * 2 + blackKeyWidth * 3 + doubleKeyGap)
                key["pitch"] = "gs" + str(octaveCount)
                key["globalPitch"] = "gs" + str(octaveCount + octave)
        elif (i % (blackKeys/octaves) == 4):
                left = (octaveCount * octaveWidth + blackKeyStartX +
                        singleKeyGap * 3 + blackKeyWidth * 4 + doubleKeyGap)
                key["pitch"] = "as" + str(octaveCount)
                key["globalPitch"] = "as" + str(octaveCount + octave)
        right = left + blackKeyWidth
        keyNumber = whiteKeys + i
        key["left"] = left
        key["top"] = top
        key["right"] = right
        key["bottom"] = bottom
        key["type"] = "black"
        key["playing"] = False
        key["fill"] = blackDefaultFill
        key["keySym"] = keySymListBlack[i]
        key["soundActivated"] = False
        key["playStart"] = 0
        key["playStop"] = 0
        keys[str(keyNumber)] = key
        canvas.create_rectangle(left, top, right, bottom,
                                outline = outlineFill,
                                fill = blackDefaultFill)
        if ((i + 1) % 5) == 0:
            octaveCount += 1
    

# Changes the octave range, making each key sound either one octave
# higher or one octave lower, depending on the parity of dOctave.
# Parameters:
#    canvas: canvas where the data dictionary is stored
#    dOctave: the direction of octave change. A positive value
#             means higher, while a negative value means lower
# Returns nothing
def toggleOctave(canvas, dOctave):
    if (((dOctave == +1) and (canvas.data["baseOctave"] + 1 < 7)) or
        ((dOctave == -1) and (canvas.data["baseOctave"] - 1 > 0))):
        canvas.data["baseOctave"] += dOctave
        octave = canvas.data["baseOctave"]
        keys = canvas.data["keys"]
        for key in keys:
            theKey = keys[key]
            actualPitch = theKey["globalPitch"]
            actualPitchOctave = actualPitch[-1]
            newOctave = str(int(actualPitchOctave) + dOctave)
            newPitch = actualPitch[:-1] + newOctave
            theKey["globalPitch"] = newPitch
    

# Displays the pitches and absolute octaves of each key.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def displayOctave(canvas):
    keys = canvas.data["keys"]
    margin = canvas.data["margin"]
    for key in keys:
        theKey = keys[key]
        globalPitch = theKey["globalPitch"]
        left = theKey["left"]
        right = theKey["right"]
        centerX = (left + right) / 2
        if (len(theKey["pitch"]) == 2):
            bottom = theKey["bottom"]
            centerY = bottom + (margin / 2)
            pitchDisplay = globalPitch.upper()
            canvas.create_text(centerX, centerY, text=pitchDisplay)
        elif (len(theKey["pitch"]) == 3):
            top = theKey["top"]
            centerY = top - (margin / 2)
            pitchDisplay = (globalPitch[0] + "#" + globalPitch[2]).upper()
            canvas.create_text(centerX, centerY, text=pitchDisplay)
    
# Sets the color for each key depending on whether or not it is
# being played at the time.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def colorKey(canvas):
    keys = canvas.data["keys"]
    playFill = canvas.data["playFill"]
    whiteDefaultFill = canvas.data["whiteDefaultFill"]
    blackDefaultFill = canvas.data["blackDefaultFill"]
    for key in keys:
        theKey = canvas.data["keys"][key]
        if (theKey["playing"] == True):
            theKey["fill"] = playFill
        else:
            if theKey["type"] == "black":
                theKey["fill"] = blackDefaultFill
            elif theKey["type"] == "white":
              theKey["fill"] = whiteDefaultFill

# Iterates through all the keys, plays the ones that are being
# activated, and stops those that are no longer being activated.
# If in record mode, captures the time at which the key is first
# activated and when key is deactivated. It then populates a list,
# "tune," which represents the music being recorded. Each element
# is a list containing the pitch being played, its starting time
# relative to when record mode was initialized, and the duration of
# the key being sounded.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def playPitch(canvas, key):
    keys = canvas.data["keys"]
    theKey = keys[key]
    actualPitch = theKey["globalPitch"]
    sound = canvas.data["allPitches"][actualPitch]
    tuneStart = canvas.data["tuneStart"]
    fadeOutTime = canvas.data["fadeOutTime"]
    if theKey["playing"] == True:
        if theKey["soundActivated"] == False:
            sound.play()
            theKey["soundActivated"] = True
            if canvas.data["recActive"] == True:
                theKey["playStart"] = pygame.time.get_ticks()
                
    else:
        sound.fadeout(fadeOutTime)
        theKey["soundActivated"] = False
        if canvas.data["recActive"] == True:
            theKey["playStop"] = pygame.time.get_ticks()
            playStop = theKey["playStop"]
            playStart = theKey["playStart"]
            keyDuration = playStop - playStart
            tuneStart = canvas.data["tuneStart"]
            relativeStart = playStart - tuneStart
            canvas.data["tune"].append([sound,
                                        relativeStart,
                                        keyDuration])

# Takes the "tune" list and sorts it according to when each note was
# first activated. Also, the start time difference in between adjacent
# notes is calculated and appended to the list. (For example, if one note
# is sounded 512 milliseconds after the one before it, then that note has
# a delta of 512.)
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def prepareTune(canvas):
    if (canvas.data["stopClicked"] == True):
        tune = canvas.data["tune"]
        if ((tune != []) and(len(tune[0]) == 3)):
            tune.sort(sortTune)
            for x in range(len(tune) - 1):
                delta = tune[x+1][1] - tune[x][1]
                tune[x+1].append(delta)
            tune[0].append(0)
            canvas.data["tune"] = tune

# Sorts lists in increasing order according to the second element.
# Parameters:
#   list1: the first list to be compared
#   list2: the second list to be compared
# Returns 1 if two lists are out of order, -1 if in order, 0 if equal
def sortTune(list1, list2):
    if list1[1] > list2[1]:
        return 1
    elif list1[1] < list2[1]:
        return -1
    else:
        return 0

# Plays back the tune that has been saved.
# note[0]: sound to be played
# note[1]: relative start time of sound (not used)
# note[2]: duration of note being played
# note[3]: time between adjacent notes
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def playBack(canvas):
    canvas.data["tunePlaying"] = True
    fadeOutTime = canvas.data["fadeOutTime"]
    canvas.data["playbackFadeOutTime"] = fadeOutTime / 6
    playbackFadeOutTime = canvas.data["playbackFadeOutTime"] 
    tune = canvas.data["tune"]
    for note in tune:
        wait(note[3])
        fade = note[2] / 8
        note[0].play(fade_ms=fade)
    canvas.data["tunePlaying"] = False

# Delays the program from playing the next note without taking a
# toll on the processor, incrementing by one up to a multiple of
# the delta.
# Parameters:
#    delta: time difference between adjacent notes
# Returns nothing
def wait(delta):
    i = 0
    while (i < (delta * 8000)):
        i += 1
    return

# Loads pitches from directory into dictionary and saves it to the canvas.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def initializePitches(canvas):
    allPitches = {}
    for theFile in os.listdir("pitches"):
        pitch = str(theFile)
        findWav = pitch.find(".wav")
        pitchName = pitch[:findWav]
        allPitches[pitchName] = pygame.mixer.Sound("pitches\\" + pitch)
    canvas.data["allPitches"] = allPitches   

# Draws the overall background and the piano keyboard's background.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def drawBackground(canvas):
    backgroundFill = canvas.data["backgroundFill"]
    outlineFill = canvas.data["outlineFill"]
    canvasWidth = canvas.data["canvasWidth"]
    canvasHeight = canvas.data["canvasHeight"]
    outlineStart = canvas.data["outlineStart"]
    outlineEndX = canvas.data["outlineEndX"]
    outlineEndY = canvas.data["outlineEndY"]
    canvas.create_rectangle(0, 0, canvasWidth, canvasHeight,
                            fill=backgroundFill)
    canvas.create_rectangle(outlineStart, outlineStart,
                            outlineEndX, outlineEndY,
                            fill=outlineFill)

# Draws the composition buttons and the help button.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def drawButtons(canvas):
    drawRecordButton(canvas)
    drawStopButton(canvas)
    drawPlayButton(canvas)
    drawHelpButton(canvas)

# Draws the play button.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def drawPlayButton(canvas):
    pianoWidth = canvas.data["pianoWidth"]
    pianoHeight = canvas.data["pianoHeight"]
    outlineFill = canvas.data["outlineFill"]
    playButtonFill = canvas.data["playButtonFill"] 
    playClickedFill = canvas.data["playClickedFill"]
    radius = pianoWidth / 16
    playCenterX = pianoWidth * 3 / 4
    playStart = (playCenterX - radius, pianoHeight)
    playMiddle = (playCenterX + radius, pianoHeight + radius)
    playEnd = (playCenterX - radius, pianoHeight + radius * 2)
    canvas.data["playCoords"] = [playStart, playMiddle, playEnd]
    if (canvas.data["playClicked"] == True):
        playColor = playClickedFill
    else:
        playColor = playButtonFill
    canvas.create_polygon(playStart, playMiddle, playEnd,
                          fill=playColor, outline=outlineFill)
    canvas.create_text(playCenterX - 10, pianoHeight + radius,
                       text="PLAY", fill="white")

# Draws the record button.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def drawRecordButton(canvas):
    pianoWidth = canvas.data["pianoWidth"]
    pianoHeight = canvas.data["pianoHeight"]
    outlineFill = canvas.data["outlineFill"]
    recButtonFill = canvas.data["recButtonFill"] 
    recClickedFill = canvas.data["recClickedFill"]
    radius = pianoWidth / 16
    recCenterX = pianoWidth / 4
    recStart = (recCenterX - radius, pianoHeight)
    recEnd = (recCenterX + radius, pianoHeight + radius * 2)
    canvas.data["recCoords"] = [recStart, recEnd]
    if (canvas.data["recActive"] == True):
        recColor = recClickedFill
    else:
        recColor = recButtonFill
    canvas.create_oval(recStart, recEnd, fill=recColor)
    canvas.create_text(recCenterX, pianoHeight+radius,
                       text="RECORD", fill="white")
# Draws the stop button.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def drawStopButton(canvas):
    pianoWidth = canvas.data["pianoWidth"]
    pianoHeight = canvas.data["pianoHeight"]
    outlineFill = canvas.data["outlineFill"]
    stopButtonFill = canvas.data["stopButtonFill"] 
    stopClickedFill = canvas.data["stopClickedFill"]
    radius = pianoWidth / 16
    stopCenterX = pianoWidth / 2
    stopStart = (stopCenterX - radius, pianoHeight)
    stopEnd = (stopCenterX + radius, pianoHeight + radius * 2)
    canvas.data["stopCoords"] = [stopStart, stopEnd]
    if (canvas.data["stopClicked"] == True):
        stopColor = stopClickedFill
    else:
        stopColor = stopButtonFill
    canvas.create_rectangle(stopStart, stopEnd, fill=stopColor)
    canvas.create_text(stopCenterX, pianoHeight + radius,
                       text="STOP", fill="white")
    
# Draws the stop button.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def drawHelpButton(canvas):
    pianoHeight = canvas.data["pianoHeight"]
    pianoWidth = canvas.data["pianoWidth"]
    message = canvas.data["helpButtonMessage"]
    helpButtonTextFill = canvas.data["helpButtonTextFill"]
    helpButtonFill = canvas.data["helpButtonFill"]
    buttonX = pianoWidth / 2
    buttonY = pianoHeight* 13 / 8
    buttonRadiusX = len(message) * 4
    buttonRadiusY = buttonRadiusX / 4
    buttonStart = (buttonX - buttonRadiusX, buttonY - buttonRadiusY)
    buttonEnd = (buttonX + buttonRadiusX, buttonY + buttonRadiusY)
    canvas.data["helpCoords"] = [buttonStart, buttonEnd]
    if (canvas.data["helpClicked"] == True):
        textColor = helpButtonFill
        buttonColor = helpButtonTextFill
    else:
        textColor = helpButtonTextFill
        buttonColor = helpButtonFill
    canvas.create_rectangle(buttonStart, buttonEnd, fill=buttonColor)
    canvas.create_text(buttonX, buttonY, text=message, fill=textColor)                            

# Draws the help screen.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def drawHelpScreen(canvas):
    canvasWidth = canvas.data["canvasWidth"]
    canvasHeight = canvas.data["canvasHeight"]
    helpScreenFill = canvas.data["backgroundFill"]
    centerX = canvasWidth / 2
    centerY = canvasHeight / 2
    titleY = canvasHeight / 10
    lineHeight = 20
    instructions = ("Play notes using your keyboard\n\n" +
                    "Click the red circle to begin recording\n" +
                    "Click the blue square to stop recording or playback\n" +
                    "Click the green triangle to play " +
                    "back your last recording\n\n" +
                    "[↑] - increase octave range\n" +
                    "[↓] - decrease octave range\n" +
                    "[h] - toggle keyboard display\n" +
                    "[m] - return to main screen\n" +
                    "[x] - close the program")
    canvas.create_rectangle(0, 0, canvasWidth, canvasHeight,
                            fill=helpScreenFill)
    canvas.create_text(centerX, titleY, font=("Helvetica", "36"),
                       text="Instructions")
    canvas.create_text(centerX, centerY,
                       text=instructions, font=("Helvetica", "14"))

# Determines the action to be taken depending on the x and y values.
# Parameters:
#    canvas: canvas where the data dictionary is stored
#    x: the x-value of the mouse click event
#    y: the y-value of the mouse click event
# Returns nothing
def buttonClicked(canvas, x, y):
    recCoords = canvas.data["recCoords"]
    stopCoords = canvas.data["stopCoords"]
    playCoords = canvas.data["playCoords"]
    helpCoords = canvas.data["helpCoords"]
    xPrior = canvas.data["lastClickCoords"][0]
    yPrior = canvas.data["lastClickCoords"][1]
    if (((recCoords[0][0] <= x <= recCoords[1][0]) and
        (recCoords[0][1] <= y <= recCoords[1][1])) and
        ((recCoords[0][0] <= xPrior <= recCoords[1][0]) and
         (recCoords[0][1] <= yPrior <= recCoords[1][1]))):
        recClicked(canvas)
    elif (((stopCoords[0][0] <= x <= stopCoords[1][0]) and
        (stopCoords[0][1] <= y <= stopCoords[1][1]))and
        ((stopCoords[0][0] <= xPrior <= stopCoords[1][0]) and
         (stopCoords[0][1] <= yPrior <= stopCoords[1][1]))):
        stopClicked(canvas)
    elif (((playCoords[0][0] <= x <= playCoords[1][0]) and
        (playCoords[0][1] <= y <= playCoords[2][1]))and
        ((playCoords[0][0] <= xPrior <= playCoords[1][0]) and
         (playCoords[0][1] <= yPrior <= playCoords[1][1]))):
        playClicked(canvas)
    elif (((helpCoords[0][0] <= x <= helpCoords[1][0]) and
        (helpCoords[0][1] <= y <= helpCoords[1][1]))and
        ((helpCoords[0][0] <= xPrior <= helpCoords[1][0]) and
         (helpCoords[0][1] <= yPrior <= helpCoords[1][1]))):
        helpClicked(canvas)

# Determines the action to be taken depending on the x and y values of
# the previous mouse click. Avoids the bug in which the user presses
# and releases the mouse button in different places, whether on or
# off the button on screen.
# Parameters:
#    canvas: canvas where the data dictionary is stored
#    x: the x-value of the prior mouse click event
#    y: the y-value of the prior mouse click event
# Returns nothing
def buttonReleased(canvas, x, y):
    recCoords = canvas.data["recCoords"]
    stopCoords = canvas.data["stopCoords"]
    playCoords = canvas.data["playCoords"]
    helpCoords = canvas.data["helpCoords"]
    if ((recCoords[0][0] <= x <= recCoords[1][0]) and
        (recCoords[0][1] <= y <= recCoords[1][1])):
        recClicked(canvas)
    elif ((stopCoords[0][0] <= x <= stopCoords[1][0]) and
          (stopCoords[0][1] <= y <= stopCoords[1][1])):
        stopClicked(canvas)
    elif ((playCoords[0][0] <= x <= playCoords[1][0]) and
          (playCoords[0][1] <= y <= playCoords[1][1])):
        playClicked(canvas)
    elif ((helpCoords[0][0] <= x <= helpCoords[1][0]) and
          (helpCoords[0][1] <= y <= helpCoords[1][1])):
        helpClicked(canvas)

# Actions taken if the record button is clicked.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def recClicked(canvas):
    if (canvas.data["recActive"] == False):
        canvas.data["tune"] = []
        canvas.data["tuneStart"] = pygame.time.get_ticks()
        canvas.data["recClicked"] = True 
        canvas.data["recActive"] = True

# Actions taken if the stop button is clicked.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def stopClicked(canvas):
    canvas.data["stopClicked"] = not canvas.data["stopClicked"]
    if (canvas.data["recActive"] == True):
        canvas.data["recActive"] = False
    if (canvas.data["stopClicked"] == True):
        prepareTune(canvas)

# Actions taken if the play button is clicked.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def playClicked(canvas):
    canvas.data["playClicked"] = not canvas.data["playClicked"]
    if ((canvas.data["recActive"] == False) and
        (canvas.data["playClicked"] == False) and
        (canvas.data["tunePlaying"] == False)):
        playBack(canvas)

# Actions taken if the help button is clicked.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def helpClicked(canvas):
    canvas.data["helpClicked"] = True

# Displays the splash screen at the beginning of the program.
# Parameters:
#    none
# Returns nothing
def displaySplashScreen():
    image = pygame.image.load('splashImage.jpg')
    screen = pygame.display.set_mode((760,341),pygame.NOFRAME)
    screen.blit(image, (0,0))
    pygame.display.update()
    wait(1000)
    pygame.display.quit()

# Initializes the program, setting states and loading initial graphics.
# Parameters:
#    canvas: canvas where the data dictionary is stored
# Returns nothing
def init(canvas):
    keys = {}
    tune = []
    canvas.data["keys"] = keys
    canvas.data["tune"] = []
    canvas.data["baseOctave"] = 4
    canvas.data["recActive"] = False
    canvas.data["playActive"] = False
    canvas.data["recClicked"] = False
    canvas.data["playClicked"] = False
    canvas.data["stopClicked"] = False
    canvas.data["helpClicked"] = False
    canvas.data["showKeySymMode"] = False
    canvas.data["tunePlaying"] = False
    initializePitches(canvas)
    loadPiano(canvas)
    displayOctave(canvas)
    displaySplashScreen()

# Gets the program up and running, setting important values and constants
# in the data dictionary. Ideally, each key is 20 pixels in width, but that
# setting is not hard-coded. The program is more flexible with respect to
# dimensions.
# Parameters:
#    width: Width of the piano keyboard plus outside margins.
#           Also the ultimate width of the canvas.
#    height: Height of the piano keyboard plus outside margins.
#            Also half the ultimate height of the canvas.
# Returns nothing.
def run(width, height):
    pygame.init()
    pygame.mixer.init(buffer=512)
    root = Tk()
    octaves = 2
    whiteKeysInOctave = 7
    blackKeysInOctave = 5
    whiteKeys = whiteKeysInOctave * octaves + 1
    blackKeys = blackKeysInOctave * octaves
    pianoWidth = width
    pianoHeight = height
    canvasWidth = width
    canvasHeight = height * 2
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=False, height=False)
    root.canvas = canvas.canvas = canvas
    margin = 50
    blackDefaultFill = "black"
    whiteDefaultFill = "white"
    playFill = "yellow"
    outlineFill = "black"
    backgroundFill = "medium turquoise"
    recButtonFill = "red"
    recClickedFill = "maroon"
    stopButtonFill = "blue"
    stopClickedFill = "navy blue"
    playButtonFill = "green"
    playClickedFill = "dark green"
    helpButtonTextFill = "gold"
    helpButtonFill = "black"
    helpButtonMessage = "Instructions"
    whiteKeyWidth = (width - 2 * margin) / whiteKeys
    blackKeyWidth = whiteKeyWidth / 2
    singleKeyGap = whiteKeyWidth - blackKeyWidth
    doubleKeyGap = whiteKeyWidth + blackKeyWidth
    marginAroundPiano = whiteKeyWidth / 4
    whiteKeyStart = margin
    blackKeyStartX = whiteKeyStart + singleKeyGap + blackKeyWidth / 2
    blackKeyStartY = margin
    whiteKeyHeight = height - 2 * margin
    blackKeyHeight = whiteKeyHeight * 2 / 3
    outlineStart = whiteKeyStart - marginAroundPiano
    outlineEndX = outlineStart + whiteKeyWidth * whiteKeys + marginAroundPiano * 2
    outlineEndY = outlineStart + whiteKeyHeight + marginAroundPiano * 2
    octaveWidth = whiteKeysInOctave * whiteKeyWidth
    fadeOutTime = 1000
    keySymListWhite = ["q", "w", "e", "r", "f",
                       "g", "t", "y", "u", "i",
                       "o", "p", "bracketleft",
                       "bracketright", "backslash"]
    keySymListBlack = ["2", "3", "4", "5", "6",
                       "7", "8", "9", "0", "minus"]
    canvas.data = {}
    canvas.data["margin"] = margin
    canvas.data["blackDefaultFill"] = blackDefaultFill
    canvas.data["whiteDefaultFill"] = whiteDefaultFill
    canvas.data["playFill"] = playFill
    canvas.data["outlineFill"] = outlineFill
    canvas.data["backgroundFill"] = backgroundFill
    canvas.data["recButtonFill"] = recButtonFill
    canvas.data["recClickedFill"] = recClickedFill
    canvas.data["stopButtonFill"] = stopButtonFill
    canvas.data["stopClickedFill"] = stopClickedFill
    canvas.data["playButtonFill"] = playButtonFill
    canvas.data["playClickedFill"] = playClickedFill
    canvas.data["helpButtonTextFill"] = helpButtonTextFill
    canvas.data["helpButtonFill"] = helpButtonFill
    canvas.data["helpButtonMessage"] = helpButtonMessage
    canvas.data["whiteKeyStart"] = whiteKeyStart
    canvas.data["blackKeyStartX"] = blackKeyStartX
    canvas.data["blackKeyStartY"] = blackKeyStartY
    canvas.data["singleKeyGap"] = singleKeyGap
    canvas.data["doubleKeyGap"] = doubleKeyGap
    canvas.data["whiteKeys"] = whiteKeys
    canvas.data["blackKeys"] = blackKeys
    canvas.data["whiteKeyWidth"] = whiteKeyWidth
    canvas.data["blackKeyWidth"] = blackKeyWidth
    canvas.data["whiteKeyHeight"] = whiteKeyHeight
    canvas.data["blackKeyHeight"] = blackKeyHeight
    canvas.data["pianoWidth"] = pianoWidth
    canvas.data["pianoHeight"] = pianoHeight
    canvas.data["canvasWidth"] = canvasWidth
    canvas.data["canvasHeight"] = canvasHeight
    canvas.data["outlineStart"] = outlineStart
    canvas.data["outlineEndX"] = outlineEndX
    canvas.data["outlineEndY"] = outlineEndY
    canvas.data["octaveWidth"] = octaveWidth
    canvas.data["fadeOutTime"] = fadeOutTime
    canvas.data["octaves"] = octaves
    canvas.data["keySymListWhite"] = keySymListWhite
    canvas.data["keySymListBlack"] = keySymListBlack
    canvas.data["tuneStart"] = 0
    root.bind("<Key>", keyPressed)
    root.bind("<KeyRelease>", keyReleased)
    root.bind("<Button-1>", mousePressed)
    root.bind("<ButtonRelease>", mouseReleased)
    init(canvas)
    root.mainloop()

run (650, 250)


