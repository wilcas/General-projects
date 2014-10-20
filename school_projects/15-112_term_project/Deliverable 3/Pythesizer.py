import pygame, numpy, scipy, threading, time
from scikits.samplerate import resample

#bare bones Animation  in pythesizer class Taken 
#from Fall 2013 CA Veronica Ebert

#Class in which the app runs
class Pythesizer(object):

    #deals with mouse click events: i.e. collisions
    def mousePressed(self, event):
        for switch in self.controlSwitches:
            if switch.rect.collidepoint(self.mousePos):
                switch.isClicked = True
        for tone in self.toneSelections:
            if tone.rect.collidepoint(self.mousePos):
                tone.isSelected = not tone.isSelected
        for song in self.recordingSelections:
            if song.rect.collidepoint(self.mousePos):
                song.isSelected = not song.isSelected
        for project in self.projectSelections:
            if project.rect.collidepoint(self.mousePos):
                project.isSelected = not project.isSelected
        if self.makeProjectButton.rect.collidepoint(self.mousePos):
            if self.selectedProject != None:
                if self.projects[self.selectedProject] == []:
                    self.makeProject()
        if self.isTutorial and self.tutorialIndex < len(self.tutorialSlides)-1:
            self.tutorialIndex += 1

    #deals with events related to releasing presses
    def stopPressing(self, event):
        for switch in self.controlSwitches:
            switch.isClicked = False 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.isSustained = False 
                pygame.mixer.stop()  

    #key event handler
    def keyPressed(self, event):
        self.notePressed(event)
        if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
            self.isSustained =  True
        if event.key == pygame.K_DOWN and self.octave < self.minOctave:
            self.octave += 1
        if event.key == pygame.K_UP and self.octave  > self.maxOctave:
            self.octave -= 1
        if event.key == pygame.K_r:
            self.recordingMaintenance()
        if event.key == 8: #8 represents the delete key for pygame on mac
            self.deleteRecording()
        if event.key == pygame.K_p:
            self.playMaintenance()
        if event.key == pygame.K_RETURN:
            self.isTutorial = False
            self.tutorialIndex = 0
        if event.key == 47: #47 represents question mark in pygame on mac
            self.isTutorial = True

    #sets booleans pertaining to recording
    def recordingMaintenance(self):
        self.startTime = time.time()
        if self.selectedSong != None:
            self.isRecording = not self.isRecording
            self.recordCount += 1
            if self.recordCount%2 == 0:
                self.songCount +=1

    #deletes recordings if a filled song is selected
    def deleteRecording(self):
        if self.selectedSong != None:
            if self.songs[self.selectedSong] != {}:
                self.songs[self.selectedSong] = {}
                self.songCount -= 1

    #deals with booleans controlling playing recordings/projects
    def playMaintenance(self):
        self.playStart = time.time()
        if self.selectedProject != None:
            if self.projects[self.selectedProject] != []:
                self.playProject()
        if self.selectedSong != None:
            if self.songs[self.selectedSong] != {}: 
                self.playRecording()

    #calls to play a note with its index
    def notePressed(self, event):
        if self.selectedSound != None:
            if event.key in self.notes:
                note = self.notes[event.key][0]
                noteIndex = self.notes[event.key][1]
                self.playSound(note*self.octave, noteIndex)

    #getSelected Functions gets index of selected boxes at all times

    def getSelectedSong(self):
        for i in xrange(len(self.recordingSelections)):
            if self.recordingSelections[i].isSelected:
                return i
        return None

    def getSelectedProject(self):
        for i in xrange(len(self.projectSelections)):
            if self.projectSelections[i].isSelected:
                return i
        return None

    def getSelectedSound(self):
        for i in xrange(len(self.toneSelections)):
            if self.toneSelections[i].isSelected:
                return i
        return None

    #deals with events that change with time
    def timerFired(self):
        self.selectedSong = self.getSelectedSong()
        self.selectedProject = self.getSelectedProject()
        self.selectedSound = self.getSelectedSound()
        self.mousePos = pygame.mouse.get_pos()
        self.animations()
        for switch in self.controlSwitches:
            switch.update(self.mousePos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.mode = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mousePressed(event) 
            elif event.type == pygame.MOUSEBUTTONUP:
                self.stopPressing(event)
            elif event.type == pygame.KEYDOWN:
                self.keyPressed(event)
            elif event.type == pygame.KEYUP:
                self. stopPressing(event)

    #deals with moving line animation when songs are played
    def animations(self):
        if self.selectedSong != None:
            if (self.isPlaying and
                self.songs[self.selectedSong] != {}):
                self.updateRecordingAnimation()
        if self.selectedProject != None:
            if (self.isPlayingProject and 
                self.projects[self.selectedProject] != []):
                self.updateProjectAnimation()

    #updates all drawings
    def redrawAll(self):  
        self.screen.fill(self.backgroundColor)
        self.drawEffectLabels()
        self.drawSelectionLabels()
        self.drawPianoKeys()
        self.drawSongVisualization()
        self.makeProjectButton.draw(self.screen)
        for background in self.controlBackgrounds:
            background.draw(self.screen)
        for switch in self.controlSwitches:
            switch.draw(self.screen)
        for tone in self.toneSelections:
            tone.draw(self.screen)
        for song in self.recordingSelections:
            song.draw(self.screen)
        for project in self.projectSelections:
            project.draw(self.screen)
        if self.isTutorial:
            self.drawTutorial()
        pygame.display.flip() 

        #basic algorithm for making text taken from
        #pygame tutorial: http://www.pygame.org/docs/tut/tom/games2.html
        #following label functions SpecifiedLabels
    def drawEffectLabels(self):
        effectLabels = ["Volume:","Length:","Fade:","Attack:"]
        fontColor = (255,30,30) #red
        for i in xrange(1, len(effectLabels)+1):
            font = pygame.font.Font(None, 20)
            text = font.render("%s"%effectLabels[i-1], 1, fontColor)
            textPos = text.get_rect()
            factor = 4.0
            width = self.width/factor - self.width/(factor*10) 
            height = (self.height/(len(effectLabels)*factor))
            xCoord, yCoord = 25 , self.height - ((1.9*height)*i)-height
            textPos.left, textPos.top = (xCoord,yCoord)
            self.screen.blit(text, textPos)

    def drawSelectionLabels(self):
        fontColor = (255,30,30)
        margin = 150
        factor = 30
        self.drawSynthLabel()
        self.drawSongLabel()
        self.drawHelpLabel()
        self.drawProjectLabel()
        self.drawTrackLabel()
        
    def drawSynthLabel(self):
        fontColor = (255,30,30)
        margin = 150
        factor = 30
        synthFont = pygame.font.Font(None, 40)
        synthText = synthFont.render("Synths", 1, fontColor)
        synthPos = synthText.get_rect()
        synthPos.center = (margin, self.height/factor)
        self.screen.blit(synthText, synthPos)

    def drawSongLabel(self):
        fontColor = (255,30,30)
        fontSize = 40
        margin = 150
        factor = 30
        songFont = pygame.font.Font(None, fontSize)
        songText = songFont.render("Recordings", 1, fontColor)
        songPos = songText.get_rect()
        songPos.center = (self.width - margin, self.height/factor)
        self.screen.blit(songText, songPos)

    def drawTrackLabel(self):
        fontColor = (255,30,30)
        fontSize = 40
        margin = 150
        factor = 30
        trackFont = pygame.font.Font(None, fontSize)
        trackText = trackFont.render("Current Track",1, fontColor)
        trackPos  = trackText.get_rect()
        trackPos.center = (self.width/2, self.height/factor)
        self.screen.blit(trackText, trackPos)

    def drawProjectLabel(self):
        fontColor = (255,30,30)
        fontSize = 40
        margin = 150
        factor = 30
        ratio = 2.8
        projectFont = pygame.font.Font(None, fontSize)
        projectText = projectFont.render("Projects", 1, fontColor)
        projectPos = projectText.get_rect()
        projectPos.center = (self.width - margin,
                             self.height - self.height/ratio)#
        self.screen.blit(projectText, projectPos)

    def drawHelpLabel(self):
        fontColor = (0,150,255)
        margin = 30
        helpFont = pygame.font.Font(None, 20)
        helpText = helpFont.render("(Press '?' to view the tutorial again.)",
                                    1, fontColor)
        helpPos = helpText.get_rect()
        helpPos.center = (self.width/2, self.height - margin)
        self.screen.blit(helpText, helpPos)

    def drawPianoKeys(self):
        ratio1 = 3
        ratio2 = 2.5
        image = self.pianoKeys
        image = pygame.transform.scale(image,
                                     (self.width/ratio1, self.height/ratio1))
        pos = image.get_rect()
        pos.left, pos.top = (self.width/ratio1, 
                            self.height - self.height/ratio2)
        self.screen.blit(image, pos)

    #draws tutorial at specified slide (changed in mousePress)
    def drawTutorial(self):
        i = self.tutorialIndex
        image = self.tutorialSlides[i]
        image = pygame.transform.scale(image,(self.width,self.height))
        pos = image.get_rect()
        pos.center = (self.width/2, self.height/2)
        self.screen.blit(image,pos)

    #draws visual representation of recordings(spaces based on time and pitch)
    def drawSongVisualization(self):
        #@TODO make this
        width, height = self.width/3, self.height/3
        color = (255,255,255) #white
        self.songSurface = pygame.Surface((width, height))
        self.songSurface.fill(color)
        pos = self.songSurface.get_rect()
        pos.center = (self.width/2, 50+height/2)#@TODO remove magic nums
        self.drawNotes()
        if self.isPlaying:
            self.recordingAnimation()
        if self.isPlayingProject:
            self.projectAnimation()
        if self.isRecording:
            self.drawRecordingText()
        self.screen.blit(self.songSurface, pos)

        #draws 'notes' on song surface, scales with length and time
    def drawNotes(self):
        width,height=self.songSurface.get_width(),self.songSurface.get_height()
        color = (0,0,0)#black
        if not self.isRecording:
            if self.selectedSong != None:
                selectedSong = self.songs[self.selectedSong]
                if selectedSong != {}:
                    self.drawRecordingNotes(width, height, selectedSong, color)
            if self.selectedProject != None:
                selectedProject = self.projects[self.selectedProject]
                if selectedProject != []:
                    self.drawProjectNotes(width,height,selectedProject, color)
        
        #draws notes when a recording is visualized
    def drawRecordingNotes(self, width, height, selectedSong, color):
        for time in selectedSong:
            #get total time interval of song in seconds
            last = selectedSong.keys()[-1]
            totalTime = time + selectedSong[last].length/100.0 #sec
            x1 = (time/totalTime)*width
            x2 = x1 + (selectedSong[time].length/100.0)
            y1 = y2 = height-(selectedSong[time].index/14.0)*height
            pygame.draw.line(self.songSurface, color,(x1,y1),(x2,y2), 5)

        #draws notes when a project is visualized
    def drawProjectNotes(self, width, height, selectedProject, color):
        for song in selectedProject:
            for time in song:
                #get total time interval of song in seconds
                last = song.keys()[-1]
                totalTime = time + song[last].length/100.0 #sec
                x1 = (time/totalTime)*width
                x2 = x1 + (song[time].length/100.0)
                y1 = y2 = height-(song[time].index/14.0)*height
                pygame.draw.line(self.songSurface, color,(x1,y1),(x2,y2), 5)

        #draws text signifying that recording is happening
    def drawRecordingText(self):
        surface = self.songSurface
        color = (255,0,0)#red
        width, height = surface.get_width(), surface.get_height
        font = pygame.font.Font(None, 30)
        text = font.render("RECORDING...",1, color)
        textPos = text.get_rect()
        textPos.center = surface.get_rect().center
        surface.blit(text,textPos)

        #overall initizalizer
    def init(self):
        self.mode = None
        self.isTutorial = True
        self.tutorialIndex = 0
        self.numControls = 4
        self.initImages()
        self.initControlBackgrounds()
        self.initControlSwitches()
        self.initSounds()
        self.initProjects()
        self.initRecordings()
        self.initToneSelections()
        self.initRecordingSelections()
        self.initProjectSelections()
        self.initButtons()
        self.backgroundColor = (0, 0, 75)

        #loads all images from data folder
    def initImages(self):
        self.pianoKeys = pygame.image.load("data/pianoKeys.gif")
        tutorialFiles = ["data/Slide1.gif","data/Slide2.gif",
                          "data/Slide3.gif","data/Slide4.gif",
                          "data/Slide5.gif","data/Slide6.gif"]
        self.tutorialSlides = []
        for path in tutorialFiles:
            image = pygame.image.load(path)
            self.tutorialSlides.append(image)

        #makes backgrounds for slider controls
    def initControlBackgrounds(self):
    	self.controlBackgrounds = []
    	for i in xrange(1, self.numControls+1):
    		factor = 4.0
    		width = self.width/factor - self.width/(factor*10) 
    		height = (self.height/(self.numControls*factor))
    		xCoord, yCoord = 25 , self.height - ((2.0005*height)*i)
    		pos = (xCoord,yCoord)
    		background = ControlBackground(width, height, pos)
    		self.controlBackgrounds.append(background)

        #makes switches for slider controls
    def initControlSwitches(self):
        self.controlSwitches = []
        for i in xrange(1, self.numControls+1):
            factor = 4.0
            width = (self.width/factor - self.width/(factor*10))/10
            height = (self.height/(self.numControls*factor))
            xCoord, yCoord = 25 , self.height - ((2.0005*height)*i)
            pos = (xCoord,yCoord)
            switch = ControlSwitch(width, height,
                                   pos, self.controlBackgrounds[i-1].rect)
            self.controlSwitches.append(switch) 

        #makes select boxes for tones
    def initToneSelections(self):
        self.toneSelections = []
        for i in xrange(1, len(self.soundFiles)+1):
            factor = 4.0
            width = (self.width/factor - self.width/(factor*10))
            height = (self.height/(self.numControls*factor))
            xCoord, yCoord = 25 , ((1.1*height)*i)
            pos = (xCoord,yCoord)
            button = SelectBox(width, height, pos, self.soundFiles[i-1])
            self.toneSelections.append(button)
        
        #makes Select Boxes for recordings
    def initRecordingSelections(self):
        self.recordingSelections = []
        for i in xrange(1, len(self.songs)+1):
            factor = 4.0
            width = (self.width/factor - self.width/(factor*10))
            height = (self.height/(len(self.songs)*factor))
            xCoord, yCoord = self.width - (25+width) , ((1.1*height)*i)
            pos = (xCoord,yCoord)
            button = SelectBox(width, height, pos, "Recording#%d"%i)
            self.recordingSelections.append(button)

        #makes select Boxes for Projects
    def initProjectSelections(self):
        self.projectSelections = []
        for i in xrange(self.maxProjects, 0, -1):
            factor = 4.0 
            width = (self.width/factor - self.width/(factor*10))
            height = (self.height/(self.maxProjects*factor))
            (xCoord, yCoord)= (self.width - (25+width),
                               self.height - ((1.1*height)*i))
            pos = (xCoord, yCoord)
            number = self.maxProjects+1-i
            button = SelectBox(width, height, pos, "Project #%d"%number)
            self.projectSelections.append(button)

    #sets up attrbutes for default sound files
    def initSounds(self):
        factor = 20,0
        self.soundFiles = ["data/tone1short.wav", "data/Drum.wav",
                           "data/Bass.wav"]
        self.selectedSound = None 
        self.volume = self.controlSwitches[0].controlVal
        self.length = int(1000*self.controlSwitches[1].controlVal)#milliseconds
        self.fade = int(100 *self.controlSwitches[2].controlVal)
        self.attack = self.controlSwitches[3].controlVal*factor
        self.minOctave = 5
        self.octave = self.minOctave
        self.soundArrays = []
        self.makeNotes()
        for sound in self.soundFiles: #makes sounds arrays for less delay
            tone = pygame.mixer.Sound(sound)
            toneArray = pygame.sndarray.array(tone)
            self.soundArrays.append(toneArray)
        
        #makes a dictionary mapping a key to a samplerate(pitch), and an index
    def makeNotes(self):
        self.notes={pygame.K_a:[2.1,1],pygame.K_w:[2.0,2],pygame.K_s:[1.9,3],
                pygame.K_e:[1.8,4],pygame.K_d:[1.7,5],pygame.K_f:[1.6,6],
                pygame.K_t:[1.5,7],pygame.K_g:[1.4,8],pygame.K_y:[1.3,9],
                pygame.K_h:[1.2,10],pygame.K_u:[1.1,11],pygame.K_j:[1.0,12],
                pygame.K_k:[0.9,13]}
        
        #initializes values related to recording
    def initRecordings(self):
        self.maxOctave = 1
        self.isSustained = False
        self.isRecording = False
        self.songs = [{},{},{},{},{}]
        self.songCount = 0
        self.selectedSong = None 
        self.startTime = None
        self.recordCount = 0
        self.isPlaying = False
        self.lineX0, self.lineX1 = 0, 0
        self.playStart = None 

        #initializes values related to projects
    def initProjects(self):
        self.projects = [[],[],[],[],[]]
        self.maxProjects = 5
        self.selectedProject = None
        self.isPlayingProject = False

        #initializes single press button
    def initButtons(self):
        factor = 4.0 
        ratio = 3.0
        margin = 25
        color = (200,0,0)
        width = (self.width/factor - self.width/(factor*10))
        height = (self.height/(self.maxProjects*factor))
        (xCoord, yCoord) = (self.width - (margin+width),
                            self.height-self.height/ratio)
        pos = (xCoord, yCoord)
        self.makeProjectButton = Button(width, height, pos, 
                                            color,"Make Project")

        #plays a sound with specfied attributes
        #if recording, relays sound o function that saves values
    def playSound(self, pitch, noteIndex):
        self.getControlVals()
        toneArray = self.soundArrays[self.selectedSound]
        if self.attack != 0:
            changedArray = resample(toneArray*self.attack,
                           pitch,"sinc_fastest").astype(toneArray.dtype)
        else: 
            changedArray = resample(toneArray,
             pitch,"sinc_fastest").astype(toneArray.dtype)#makes correct type
        newSound = pygame.sndarray.make_sound(changedArray)
        newSound.set_volume(self.volume)
        if (self.isRecording and self.songCount < len(self.songs) and
            self.selectedSong != None):
            currentTime = time.time()
            timePlayed = currentTime - self.startTime  
            self.makeRecording(newSound,timePlayed,noteIndex,self.volume,
                            self.length,self.fade,self.isSustained)
        if self.isSustained: self.length = -1
        if self.fade != 0: newSound.play(0,self.length,0).fadeout(self.fade)
        elif self.isSustained: newSound.play(0,-1,0)
        else: newSound.play(0,self.length,0)

        #sets how sound is played based on sliders
    def getControlVals(self):
        self.volume = self.controlSwitches[0].controlVal
        self.length = int(1000*self.controlSwitches[1].controlVal)#milliseconds
        self.fade = int(1000 *self.controlSwitches[2].controlVal)
        self.attack = 20.0*self.controlSwitches[3].controlVal

    #makes a 'song' which maps a time to an object containing sound attributes
    def makeRecording(self,sound,time,index,volume,length,fade,isSustained):
        nextSound = RecordedSound(sound,index,volume,length,fade,isSustained)
        currentTrack = self.songs[self.selectedSong]
        currentTrack[time] = nextSound

    #plays sound with its saved attributes
    def playBack(self, recordedSound):
        recordedSound.playBack()

    #uses a timer object to play recorded sound objects   
    def playRecording(self):
        self.isPlaying = True
        currentTrack = self.songs[self.selectedSong]
        for time in currentTrack: #keys are time, map to sounds
            t =  threading.Timer(time, self.playBack, [currentTrack[time]])
            t.start()#starts Timer object

        #line animation for playing recording
    def recordingAnimation(self):
        surface = self.songSurface
        width,height= surface.get_width(), surface.get_height()
        y0, y1 = 0, height
        x0, x1 = self.lineX0, self.lineX1
        pygame.draw.line(surface,(0,0,0),(x0,y0),(x1,y1),2)

        #moves line at speed based on total time of recording
    def updateRecordingAnimation(self):
        currentTime = time.time()
        timePlayed = currentTime- self.playStart
        surface = self.songSurface
        width= surface.get_width()
        song = self.songs[self.selectedSong]
        timeList = song.keys()
        finalTime = timeList[-1]
        totalTime = finalTime + song[finalTime].length/100.0
        self.lineX0= (timePlayed/totalTime)*width
        self.lineX1 = (timePlayed/totalTime)*width
        if self.lineX1 > width:
            self.isPlaying = False
            self.lineX0 = 0
            self.lineX1 = 0

        #line animation for project
    def projectAnimation(self):
        surface = self.songSurface
        width,height= surface.get_width(), surface.get_height()
        y0, y1 = 0, height
        x0, x1 = self.lineX0, self.lineX1
        pygame.draw.line(surface,(0,0,0),(x0,y0),(x1,y1),2)

        #moves line a speed related to length of longest track
    def updateProjectAnimation(self):
        currentTime = time.time()
        timePlayed = currentTime - self.playStart
        surface = self.songSurface
        width,height= surface.get_width(), surface.get_height()
        project = self.projects[self.selectedProject]
        finalTime, song = self.getFinalTime(project)
        totalTime = finalTime + project[song][finalTime].length/100.0
        self.lineX0= (timePlayed/totalTime)*width
        self.lineX1 = (timePlayed/totalTime)*width
        if self.lineX1 > width:
            self.isPlayingProject = False
            self.lineX0 = 0
            self.lineX1 = 0

        #gets longest length of recording in a project
    def getFinalTime(self, project):
        maxtime = 0
        for song in project:
            timeList = song.keys()
            finalTime = timeList[-1]
            if finalTime > maxtime:
                maxTime = finalTime
                songIndex = project.index(song)
        return maxTime, songIndex

        #combines  dictionary of selected recordings into one list
    def makeProject(self):
        currentProject = self.projects[self.selectedProject]
        for i in xrange(len(self.recordingSelections)):
            if self.recordingSelections[i].isSelected:
                currentProject.append(self.songs[i])
        self.projects.append(currentProject)

        #plays projects
    def playProject(self):
        self.isPlayingProject = True
        currentProject = self.projects[self.selectedProject]
        for song in currentProject:
            for time in song:
                t = threading.Timer(time, self.playBack, [song[time]])
                t.start()

        #runs the entire program
    def run(self, width=1000, height=600):
        pygame.init()
        pygame.mixer.init(frequency = 22050, size= 8, channels=2,buffer=4096)
        self.screenSize = (width, height)
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("Pythesizer")
        self.clock = pygame.time.Clock()
        self.init()
        counter = 0
        while self.mode != False:
            counter += 1
            self.timerFired()
            if counter % 10 == 0:#only draw when necessary (fixes sound delay)
                self.redrawAll()


#Backgrounds for switches
class ControlBackground(pygame.sprite.Sprite):

    def __init__(self, width, height, pos):
    	pygame.sprite.Sprite.__init__(self)
    	color = (255,255,255)#white
    	self.image = pygame.Surface((width,height))
    	self.image.fill(color)
    	self.rect = self.image.get_rect()
    	self.rect.left, self.rect.top = pos
        self.pos = pos
    	self.width = width
    	self.height = height

    def draw(self, surface): 
        surface.blit(self.image, self.pos)

#switches that map to values modifying synths
class ControlSwitch(pygame.sprite.Sprite):

    def __init__(self, width, height, pos,  bindingRect): 
        pygame.sprite.Sprite.__init__(self)
        color = (75,75,75)#gray
        self.width, self.height = width , height
        self.bindingRect = bindingRect 
        self.image = pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos
        self.pos = pos
        self.isClicked = False
        self.controlVal = 0

    def draw(self, surface):
        surface.blit(self.image, self.pos)

    def update(self, mousePos):
        if self.isClicked:
            self.rect.left = mousePos[0]
            if self.rect.left < self.bindingRect.left:
                self.rect.left = self.bindingRect.left
            if self.rect.right > self.bindingRect.right:
                self.rect.right = self.bindingRect.right
            self.pos = (self.rect.left, self.rect.top)
        self.controlVal = (self.rect.left - self.bindingRect.left)/(1.0*self.bindingRect.width)

#holds data and plays back recordings
class RecordedSound(object):

    def __init__(self, sound, index, volume, length, fade, isSustained):
        self.sound = sound
        self.index = index
        self.volume = volume
        self.length = length
        self.fade = fade
        self.isSustained = isSustained

    def playBack(self):
        self.sound.set_volume(self.volume)
        if self.isSustained: self.length = -1
        if self.fade != 0:
            self.sound.play(0,self.length,0).fadeout(self.fade)
        else: 
            self.sound.play(0,self.length,0)

#object that serves to deal with both synth and song selections
class SelectBox(pygame.sprite.Sprite):

    def __init__(self, width, height, pos, name):
        pygame.sprite.Sprite.__init__(self)
        color = (255,255,255)
        self.image = pygame.Surface((width,height))
        self.width, self.height = width, height
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos
        self.pos = pos
        self.isSelected = False
        self.name = name

    def draw(self, surface):
        selectedColor = (255,237,70) #yellow
        color = (255,255,255) #white
        if self.isSelected:
            self.image.fill(selectedColor)
        else:
            self.image.fill(color)
        self.drawText()
        surface.blit(self.image, self.pos)

    #paraphrases some code fromhttp://www.pygame.org/docs/tut/tom/games2.html
    def drawText(self):
        fontSize = 20
        fontColor = (0,0,0) #black
        font = pygame.font.Font(None, fontSize)
        text = font.render("%s"%self.name,1, fontColor)
        textPos = text.get_rect()
        textPos.center = self.image.get_rect().center
        self.image.blit(text, textPos)

#class of single press control buttons
class Button(pygame.sprite.Sprite): 

    def __init__(self, width, height, pos, color, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width,height))
        self.width, self.height = width, height
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos
        self.pos = pos
        self.name = name

    def draw(self, surface):
        self.drawText()
        surface.blit(self.image, self.pos)

    def drawText(self):
        fontSize = 20
        fontColor = (0,0,0) #black
        font = pygame.font.Font(None, fontSize)
        text = font.render("%s"%self.name,1, fontColor)
        textPos = text.get_rect()
        textPos.center = self.image.get_rect().center
        self.image.blit(text, textPos)



app = Pythesizer()
app.run()