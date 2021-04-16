#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame
pygame.init()
import time

class Player:
    def __init__(self, score):
        self.score = str(score)
        
    def addPoint(self):
        self.score = str(int(self.score)+1)
       
    def removePoint(self):
        self.score = str(int(self.score)-1)
    
    def chosenCard(self, card):
        self.card = card
    
    def addDeck(self, deck):
        if(not hasattr(self, 'deck')):
            self.deck = deck
    
    def cardTotals(self, cardtotals = {}):
        self.cardtotals = {'Rock total': '0', 'Paper total': '0', 'Scissors total': '0'}
        # card totals surface objects should be tied to the keys and values of the self.cardtotals dictionary
        for i in self.deck.cards:
            if i == CardName.ROCK:
                self.cardtotals['Rock total'] =  str(int(self.cardtotals['Rock total'])+1)
            if i == CardName.PAPER:
                self.cardtotals['Paper total'] =  str(int(self.cardtotals['Paper total'])+1)
            if i == CardName.SCISSORS:
                self.cardtotals['Scissors total'] =  str(int(self.cardtotals['Scissors total'])+1)
        return self.cardtotals
    
    
    def chosenAndRemoveCard(self, card):
        self.chosenCard(card)
        self.deck.removeCard(card)
    
    def __str__(self):
        return f'Player has score: {self.score} with {self.cardTotals()}'
    
class Deck:
    def __init__(self, cards):
        self.cards = cards
        
    def getCards(self):
        return self.cards
        
    def addCard(self, card):
        self.cards.append(card)
        
    def removeCard(self, card):
        self.cards.remove(card)

    def __str__(self):
        return "cards: " + ", ".join([str(card) for card in self.cards])

class Card:
    def __init__(self, name):
        self.name = name

    def __eq__(self, obj):
        return self.name == obj.name
    
    def __str__(self):
        return f'{self.name}'
    
    def __lt__(self, other):
        return self.name < other.name
    
from enum import Enum    
class CardName(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class GameGUI:
    
    display_width = 960
    display_height = 550
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    caption = pygame.display.set_caption('Restricted Rock Paper Scissors')
    clock = pygame.time.Clock()
    
class Mouse:
    mousePos = pygame.mouse.get_pos()
    
class Images:
    # Might need to explicitly open these images so that it won't run into problems when downloaded into an executable file
    
    # Maybe, in a zipfile, load these images into a file, and load the game executable too, and make the image locations so that they grab for the same file location
    AkagiVsKaiji=pygame.image.load(r'AkagiVsKaiji.jpg')
    ChairmanHappy = pygame.image.load(r'ChairmanHappy400wh622h.jpg')    
    RockImage = pygame.image.load(r'PlainRockImage70w98h.jpg')
    RockImageQuit = pygame.image.load(r'PlainRockImage70w98hQuit.jpg')
    PaperImage = pygame.image.load(r'PlainPaperImage70w98h.jpg')
    PaperImageStart = pygame.image.load(r'PlainPaperImage70w98hStart.jpg')
    ScissorsImage = pygame.image.load(r'PlainScissorsImage70w98h.jpg')
    
    RockCardImage = pygame.image.load(r'RockCard140w195h.jpg.png')
    PaperCardImage = pygame.image.load(r'PaperCard140w195h.jpg')
    ScissorsCardImage = pygame.image.load(r'ScissorsCard140w195h.jpg')
    
    cardsPicTransition = pygame.image.load(r'cardsPicTransition960w550h.jpg')
    
    kaijiupset = pygame.image.load(r'kaijiCrying740w370h.jpg')
    akaginormal = pygame.image.load(r'akagiSmile740w370h.jpg')
    
    Tonegawa = pygame.image.load(r'Tonegawa740w370h.jpg')
    
class Music:
    def __init__(self):
        self.ZawaIntro = r'youtubeZawa.wav'

    def playmusic(self):
        pygame.mixer.music.load(self.ZawaIntro)
        pygame.mixer.music.play(-1)
        
    def stopmusic(self):
        pygame.mixer.music.stop()

class Fonts:
    karmaticArcadefont = r"ka1.ttf"
    amaticBoldfont = r"Amatic-Bold.ttf"
    
class Colors:
    black = (0,0,0)
    white = (255,255,255)
    red = (150,0,0)  
    brightRed = (255,0,0)
    green = (0,200,0)
    brightGreen = (0,255,0)
    blue = (0,0,150)
    brightBlue = (0,0,255)

class Font(Fonts):
    def __init__(self, fontLocation, wordsSize):
        self.fontLocation = fontLocation
        self.wordsFont = pygame.font.Font(fontLocation,wordsSize)
    def __str__(self):
        return f'{self.fontLocation}'
                
class Text(Font, GameGUI):
    
    def __init__(self,color=Colors.red,fontLocation=Fonts.amaticBoldfont, wordsSize=20, words='', x=0, y=0, rectPosition='center', bgColor=None):
        Font.__init__(self, fontLocation, wordsSize)
        GameGUI.__init__(self)
        self.color = color
        self.x=x
        self.y=y
        self.words = f'{words}'
        self.rectPosition = rectPosition
        self.bgColor = bgColor
    def createText(self):
        self.wordsSurface = self.wordsFont.render(self.words, True, self.color, self.bgColor)
        return self.wordsSurface, self.wordsSurface.get_rect()
    
    def messageDisplay(self):
        self.TextSurf, self.TextRect = self.createText()
        return self.TextSurf, self.TextRect
    
    def centerTextRect(self):
        if self.rectPosition == 'center':
            self.TextRect.center = ((self.x),(self.y))
        if self.rectPosition == 'topleft':
            self.TextRect.topleft = ((self.x),(self.y))
        if self.rectPosition == 'topright':
            self.TextRect.topright = ((self.x),(self.y))
        
    def displayText(self):
        self.gameDisplay.blit(self.TextSurf, self.TextRect)
        
    def final(self):
        self.createText()
        self.messageDisplay()
        self.centerTextRect()

    
class Button:
    def __init__(self, command, fontLocation='', wordsSize='', color='',  words='', bgColor=None, rect=(0,0,50,70), imageSurface=''):
        self.rect = pygame.Rect(rect)
        self.imageSurface = imageSurface
        self.bgColor = bgColor
        self.words = words
        self.color = color
        self.command = command
        self.fontLocation = fontLocation
        self.wordsSize = wordsSize
        
    def renderImg(self, screen):
        screen.blit(self.imageSurface, self.rect)
        
    def renderTxt(self, screen):
        self.font = Font(self.fontLocation,self.wordsSize)
        self.wordsSurface = self.font.wordsFont.render(self.words, True, self.color,self.bgColor)
        screen.blit(self.wordsSurface, self.rect)
        
    def renderImgText(self,screen):
        self.renderImg(screen)
        self.renderTxt(screen)
        
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.command()
                game.waiting = False
                

class Game:
    music = Music()  
    def __init__(self, rock = Card(CardName.ROCK.name), paper = Card(CardName.PAPER.name), scissors = Card(CardName.SCISSORS.name)):
        self.rock = rock
        self.paper = paper
        self.scissors = scissors
        self.click_time = 0
    
    def createIntroText(self):
        self.Title1 = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=80,words='R  E  S  T  R  I  C  T  E  D', x=(GameGUI.display_width/2), y=(GameGUI.display_height/2)-120)
        self.Title2 = Text(color=Colors.brightRed,fontLocation=Fonts.karmaticArcadefont, wordsSize=30,words='R o c k', x=(GameGUI.display_width/2), y=(GameGUI.display_height/2)-40)
        self.Title3 = Text(color=Colors.brightGreen,fontLocation=Fonts.karmaticArcadefont, wordsSize=30,words='P a p e r', x=(GameGUI.display_width/2), y=(GameGUI.display_height/2)+10)
        self.Title4 = Text(color=Colors.brightBlue,fontLocation=Fonts.karmaticArcadefont, wordsSize=30,words='S c i s s o r s', x=(GameGUI.display_width/2), y=(GameGUI.display_height/2)+60)
        self.TitleList = [self.Title1, self.Title2, self.Title3, self.Title4]
        for t in self.TitleList:
            t.final()

    def createIntroButtons(self):
        self.startButton = Button(rect=(380,390,70,98), imageSurface=Images.PaperImageStart, fontLocation=Fonts.amaticBoldfont, words='     Start', wordsSize=29, color=Colors.brightGreen, command=self.transition)
        self.quitButton = Button(rect=(510,390,70,98), imageSurface=Images.RockImageQuit, fontLocation=Fonts.amaticBoldfont, words='      Quit', wordsSize=29, color=Colors.brightRed, command=pygame.quit)
        self.introButtonList = [self.startButton, self.quitButton]
            
    def run(self):
        self.music.playmusic()
        
        self.createIntroText()
        
        self.createIntroButtons()
        
        self.intro = True
        while(self.intro):
            
            for event in pygame.event.get():
#                 print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_time = pygame.time.get_ticks()
                self.quitButton.get_event(event)
                self.startButton.get_event(event)
                
            GameGUI.gameDisplay.fill(Colors.black)
            GameGUI.gameDisplay.blit((Images.AkagiVsKaiji), (0, 0))
            
            for t in self.TitleList:    
                t.displayText()
            for b in self.introButtonList:
                b.renderImgText(GameGUI.gameDisplay)

#             Mouse.mousePos
            pygame.display.update()
            GameGUI.clock.tick(15)
            
    def createTransitionText(self):
        self.line1 = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=50,words="Show me what you're worth, kouzu.", x=250, y=100)
        self.line2 = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont, wordsSize=50,words='Only one of you can be free...', x=250, y=180)
        self.line3 = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont, wordsSize=100,words="Heh HEH heh.", x=250, y=260)
        self.line4 = Text(color=Colors.white,fontLocation=Fonts.amaticBoldfont,wordsSize=40,words='What the hell is this...', x=(GameGUI.display_width/2), y=(GameGUI.display_height-25))
        self.transitionwords = [self.line1, self.line2, self.line3, self.line4]
        ly = 20
        
        for l in self.transitionwords:
            if l != self.line4:
                l.x = 300
                l.y = ly+80
                ly = l.y
            l.final()
            
    def transition(self):
        self.intro = False
        GameGUI.gameDisplay.fill(Colors.black)
        GameGUI.gameDisplay.blit((Images.ChairmanHappy), (((GameGUI.display_width-400)), ((GameGUI.display_height-622)/2)))
        
        self.createTransitionText()
        
        skipTransition = False
        passed_time = 0
        self.transitionScene = True
        while(self.transitionScene):
#             current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
#                 print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    skipTransition = True
                    
            #timer starts after startButton click in intro loop    
            if self.click_time != 0:  # If timer has been started.
            # Calculate the passed time since the click.
                passed_time = (pygame.time.get_ticks()-self.click_time) / 1000

            if skipTransition == False:
                if passed_time >= 1:
                    self.line1.displayText()
                if passed_time >= 3:
                    self.line2.displayText()
                if passed_time >= 5:
                    GameGUI.gameDisplay.fill(Colors.black)
                    GameGUI.gameDisplay.blit((Images.ChairmanHappy), (((GameGUI.display_width-400)), ((GameGUI.display_height-622)/2)))
                    self.line3.displayText()
                if passed_time >= 7:
                    GameGUI.gameDisplay.fill(Colors.black)
                if passed_time >=9:
                    GameGUI.gameDisplay.blit((Images.cardsPicTransition), (0,0))
                    self.line4.displayText()
                if passed_time >=13:
                    self.transitionScene = False
                    self.mainLoop()
            else: 
                self.transitionScene = False
                self.mainLoop()
            pygame.display.update()
            GameGUI.clock.tick(15)
        
    def getNewPlayer(self, score):
        player = Player(score)
        deck = Deck([])
        for i in range(4):
            deck.addCard(self.rock)
            deck.addCard(self.paper)
            deck.addCard(self.scissors)
        deck.cards = sorted(deck.cards)
        player.addDeck(deck)
        player.cardTotals()

        return player
    
    def getPlayerCardDicts(self):
        self.allcardtotals = {'p1':0,'p2':0}
        self.allPlayersCardDicts = []
        self.allPlayersCardDicts.append(self.player1.cardTotals())
        self.allPlayersCardDicts.append(self.player2.cardTotals())
        for i, j in zip(self.allPlayersCardDicts[0].values(), self.allPlayersCardDicts[1].values()):
            self.allcardtotals['p1'] += int(i)
            self.allcardtotals['p2'] += int(j)
                
    def RockWinner(self):
        return True if(self.player1.card == self.rock and self.player2.card == self.scissors) else False 

    def PaperWinner(self):
        return True if(self.player1.card == self.paper and self.player2.card == self.rock) else False 

    def ScissorsWinner(self):
        return True if(self.player1.card == self.scissors and self.player2.card == self.paper) else False
    
    def tie(self):
        if((self.player1.card == self.rock and self.player2.card == self.rock) or (self.player1.card == self.paper and self.player2.card == self.paper) or (self.player1.card == self.scissors and self.player2.card == self.scissors)):
            return True
        else: return False
        
    def distributePoint(self):
        if self.tie():
            self.showWinnerCardscene(self.nowinnerRoundtext, self.showcardwin0)
            print('Tie')
        elif self.RockWinner() or self.PaperWinner() or self.ScissorsWinner():
            self.player1.addPoint(), self.player2.removePoint()
            self.showWinnerCardscene(self.p1winsRoundtext, self.showcardwin1)
        else:
            self.player2.addPoint(), self.player1.removePoint()
            self.showWinnerCardscene(self.p2winsRoundtext, self.showcardwin2)
            
        self.rockClick = False
        self.paperClick = False
        self.scissorsClick = False
    def getWinner(self):
#         print(self.allcardtotals)
        if(int(self.player1.score) == 6) or ((self.allcardtotals['p1']+self.allcardtotals['p2']==0) and int(self.player1.score) > int(self.player2.score)):
#             self.winner=True
            self.winScene(self.p1winstext)
#             return True, print('p1 wins')

        elif(int(self.player2.score) == 6) or ((self.allcardtotals['p1']+self.allcardtotals['p2']==0) and int(self.player2.score) > int(self.player1.score)):
#             self.winner=True
            self.winScene(self.p2winstext)
#             return True, print('p2 wins')
            
        elif((self.allcardtotals['p1']+self.allcardtotals['p2']==0) and int(self.player1.score) == int(self.player2.score)):
#             self.winner=True
            self.winScene(self.nowinnertext)
#             return True, print('no winner')
        else:
            return False
           
    def cardInput(self):
    
        handPlayed = 0
        cardName = '' 
        self.mainbgcolor=0
        
        #for displaying round winner
        self.showcardwin0 = ''
        self.showcardwin1 = ''
        self.showcardwin2 = ''
        
        while(handPlayed < 2):

            self.waiting = True
            self.inputLoop()

            try:
                if self.rockClick:
                    cardName = CardName.ROCK.name
                    self.rockClick = False
                    if handPlayed == 0:
                        self.showcardwin1 = 'R'
                    if handPlayed == 1:
                        self.showcardwin2 = 'R'
                    
                elif self.paperClick:
                    cardName = CardName.PAPER.name
                    self.paperClick = False
                    if handPlayed == 0:
                        self.showcardwin1 = 'P'
                    if handPlayed == 1:
                        self.showcardwin2 = 'P'
                elif self.scissorsClick:
                    cardName = CardName.SCISSORS.name
                    self.scissorsClick = False
                    if handPlayed == 0:
                        self.showcardwin1 = 'S'
                    if handPlayed == 1:
                        self.showcardwin2 = 'S'

                cardPlayed = Card(cardName)

                if(handPlayed % 2 == 0):
                    self.player1.chosenAndRemoveCard(cardPlayed)
#                     print('p1:', self.player1.score)
#                     print('p1:', self.player1)
                    self.mainbgcolor=1

                    #SET the CLICK to FALSE again
                else:
                    self.player2.chosenAndRemoveCard(cardPlayed)
#                     print('p2:', self.player2.score)
#                     print('p2:', self.player2)
                    #SET the CLICK to FALSE again

                    self.waiting = False
                handPlayed += 1
            except:
                #try blitting an image here
                print('check if you have the card left')
            

    def rocktrue(self):
        self.rockClick = True
    def papertrue(self):
        self.paperClick = True
    def scissorstrue(self):
        self.scissorsClick = True
        
    def inputLoop(self):
#         self.waiting = True
        while self.waiting:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_time = pygame.time.get_ticks()
                    
                for i in self.mainloopButtons:
                    i.get_event(event)

            if self.mainbgcolor == 0:
                GameGUI.gameDisplay.fill(Colors.black)
                GameGUI.gameDisplay.blit(Images.kaijiupset,(110,0))
                self.p1rocks.words = self.player1.cardtotals['Rock total']
                self.p1papers.words = self.player1.cardtotals['Paper total']
                self.p1scissors.words = self.player1.cardtotals['Scissors total']
                for i in self.p1cardtotalslist:
                    i.final()
                    i.displayText()
                for i in self.scoreTextlist:
                    i.final()
                    i.displayText()
                    
            if self.mainbgcolor == 1:
                GameGUI.gameDisplay.fill(Colors.black)
                GameGUI.gameDisplay.blit(Images.akaginormal,(110,0)) 
                self.p2rocks.words = self.player2.cardtotals['Rock total']
                self.p2papers.words = self.player2.cardtotals['Paper total']
                self.p2scissors.words = self.player2.cardtotals['Scissors total']
                
                for i in self.p2cardtotalslist:
                    i.final()
                    i.displayText()
                for i in self.scoreTextlist:
                    i.final()
                    i.displayText()
            for b in self.mainloopButtons:
                if b.words=='':
                    b.renderImg(GameGUI.gameDisplay)
                else:
                    b.renderTxt(GameGUI.gameDisplay)
                    
            mouse = pygame.mouse.get_pos()
            if 180+140 > mouse[0] > 180 and 330+194 > mouse[1] > 330:
                self.selectTextrock.displayText()
            if 410+140 > mouse[0] > 410 and 330+194 > mouse[1] > 330:
                self.selectTextpaper.displayText()
            if 640+140 > mouse[0] > 640 and 330+194 > mouse[1] > 330:
                self.selectTextscissors.displayText()
            
                
            pygame.display.update()
            GameGUI.clock.tick(15)
    
    def setVariablesfalse(self):
        self.winner = False
        self.rockClick=False
        self.paperClick=False
        self.scissorsClick=False
        self.backClick=False
        
    def createInputLoopButtons(self):
        self.rockButton = Button(rect=(180,330,140,194), imageSurface=Images.RockCardImage, command=self.rocktrue)
        self.paperButton = Button(rect=(410,330,140,195), imageSurface=Images.PaperCardImage, command=self.papertrue)
        self.scissorsButton = Button(rect=(640,330,140,195), imageSurface=Images.ScissorsCardImage, command=self.scissorstrue)
        self.backButton = Button(fontLocation=Fonts.amaticBoldfont, words='BACK', wordsSize=35, color=Colors.red, bgColor=Colors.white, rect=(5,5,45,40), command=self.run)
        self.mainloopButtons = [self.rockButton,self.paperButton,self.scissorsButton,self.backButton]
        
    def createSelectText(self):
        self.selectTextrock = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=40,words="Select", x=250, y=300)
        self.selectTextpaper = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=40,words="Select", x=480, y=300)
        self.selectTextscissors = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=40,words="Select", x=710, y=300)
        selectTextlist = [self.selectTextrock,self.selectTextpaper,self.selectTextscissors]
        for i in selectTextlist:
            i.final()
        
    def createScoreText(self):
        self.p1score = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=50,words=f'P1: {self.player1.score}', x=50, y=100)
        self.p2score = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=50,words=f'P2: {self.player2.score}', x=900, y=100)
        self.scoreTextlist = [self.p1score,self.p2score]
        for i in self.scoreTextlist:
            i.final()
        
    def createCardTotalsText(self):
        self.p1rocks = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=40,words=self.player1.cardtotals['Rock total'], x=150, y=450)
        self.p2rocks = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=40,words=self.player2.cardtotals['Rock total'], x=150, y=450)
        
        self.p1papers = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=40,words=self.player1.cardtotals['Paper total'], x=380, y=450)
        self.p2papers = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=40,words=self.player2.cardtotals['Paper total'], x=380, y=450)
        
        self.p1scissors = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=40,words=self.player1.cardtotals['Scissors total'], x=610, y=450)
        self.p2scissors = Text(color=Colors.red,fontLocation=Fonts.amaticBoldfont,wordsSize=40,words=self.player2.cardtotals['Scissors total'], x=610, y=450)
        
        self.p1cardtotalslist = [self.p1rocks, self.p1papers, self.p1scissors]
        self.p2cardtotalslist = [self.p2rocks, self.p2papers, self.p2scissors]
        
    def createWinnerText(self):
        self.p1winstext = Text(color=Colors.red,fontLocation=Fonts.karmaticArcadefont,wordsSize=40,words="Player 1 Wins", x=(GameGUI.display_width/2), y=(GameGUI.display_height/2))
        self.p2winstext = Text(color=Colors.red,fontLocation=Fonts.karmaticArcadefont,wordsSize=40,words="Player 2 Wins", x=(GameGUI.display_width/2), y=(GameGUI.display_height/2))
        self.nowinnertext = Text(color=Colors.red,fontLocation=Fonts.karmaticArcadefont,wordsSize=40,words="The Company Wins", x=(GameGUI.display_width/2), y=(GameGUI.display_height/2))
        
        self.p1winsRoundtext = Text(color=Colors.red,fontLocation=Fonts.karmaticArcadefont,wordsSize=40,words="Player 1 Wins", x=(GameGUI.display_width/2), y=(40))
        self.p2winsRoundtext = Text(color=Colors.red,fontLocation=Fonts.karmaticArcadefont,wordsSize=40,words="Player 2 Wins", x=(GameGUI.display_width/2), y=(40))
        self.nowinnerRoundtext = Text(color=Colors.red,fontLocation=Fonts.karmaticArcadefont,wordsSize=40,words="The Company Wins", x=(GameGUI.display_width/2), y=(40))
        
        self.winnertextlist = [self.p1winstext, self.p2winstext, self.nowinnertext, self.p1winsRoundtext, self.p2winsRoundtext, self.nowinnerRoundtext]
        for i in self.winnertextlist:
            i.final()        
        
    def createPlayers(self):
        self.player1 = self.getNewPlayer(3)
        self.player2 = self.getNewPlayer(3)
        self.getPlayerCardDicts()
        
    def mainLoop(self):
        self.transitionScene = False
        self.createPlayers()
        
        self.setVariablesfalse()
        
        self.createInputLoopButtons()

        self.createSelectText()
        
        self.createWinnerText()
        
        self.createScoreText()
        
        self.createCardTotalsText()
        
        
        while(self.winner==False):
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 

            self.createScoreText()
            self.p1score.displayText()
            self.p2score.displayText()
            
            self.getPlayerCardDicts()
            self.getWinner()
            self.cardInput()
            self.distributePoint()

            GameGUI.clock.tick(15)
    
    def winScene(self, playerwinner):
        GameGUI.gameDisplay.fill(Colors.black)
        
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                self.backButton.get_event(event)
            self.backButton.renderTxt(GameGUI.gameDisplay)
            playerwinner.displayText()

            pygame.display.update()
            GameGUI.clock.tick(15)
            
    def createWinningCards(self):
        pass
            
    def showWinnerCardscene(self, playerwinner, showcardwin):
#         GameGUI.gameDisplay.fill(Colors.black)
        self.cardwinimage = ''
        if showcardwin == '':
            self.cardwinimage = Images.Tonegawa
        else:
            if playerwinner == self.p1winsRoundtext:
                if showcardwin == 'R':
                    self.cardwinimage = Images.RockCardImage
                if showcardwin == 'P':
                    self.cardwinimage = Images.PaperCardImage
                if showcardwin == 'S':
                    self.cardwinimage = Images.ScissorsCardImage
            if playerwinner == self.p2winsRoundtext:
                if showcardwin == 'R':
                    self.cardwinimage = Images.RockCardImage
                if showcardwin == 'P':
                    self.cardwinimage = Images.PaperCardImage
                if showcardwin == 'S':
                    self.cardwinimage = Images.ScissorsCardImage

        passed_time = 0
        self.cardwinscene=True
        while (self.cardwinscene):
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                self.backButton.get_event(event)
            self.backButton.renderTxt(GameGUI.gameDisplay)
                            
            if self.click_time != 0:
                passed_time = (pygame.time.get_ticks()-self.click_time) / 1000
                GameGUI.gameDisplay.fill(Colors.black)
                
                if passed_time >= 1:
                    if showcardwin == '':
                        GameGUI.gameDisplay.blit(self.cardwinimage, ((GameGUI.display_width-740)/2, (GameGUI.display_height-370)/2))
                    else:
                        GameGUI.gameDisplay.blit(self.cardwinimage, ((GameGUI.display_width-140)/2,(GameGUI.display_height-195)/2))
                    playerwinner.displayText()
                    
                if passed_time >=3.5:
                    self.cardwinscene = False

            pygame.display.update()
            GameGUI.clock.tick(15)
            
game = Game()
game.run()


# In[ ]:




