import wx
import os
import socket
import threading
import random
WIDTH = 800
HEIGHT = 600

class MainWindow(wx.Frame):
    def __init__(self, parent, title, width, height):
        wx.Frame.__init__(self, parent, title=title, size=(width, height), style=wx.SYSTEM_MENU | wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.sizer = wx.GridSizer(1, 1)
        self.SetSizer(self.sizer)
        fileMenu = wx.Menu()
        menuNew = fileMenu.Append(wx.ID_NEW, 'New Game', '')
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT, 'Exit', '')
        
        onlineMenu = wx.Menu()
        menuConnect = onlineMenu.Append(wx.ID_OPEN, 'Connect', '')
        menuHost = onlineMenu.Append(wx.ID_REFRESH, 'Host', '')
        
        helpMenu = wx.Menu()
        menuAbout = helpMenu.Append(wx.ID_ABOUT, 'About', '')
        
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, 'File')
        menuBar.Append(onlineMenu, 'Online')
        menuBar.Append(helpMenu, 'Help')
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.newGamePopup, menuNew)
        self.Bind(wx.EVT_MENU, self.exitProgram, menuExit)
        self.Bind(wx.EVT_MENU, self.hostPopup, menuHost)
        self.Bind(wx.EVT_MENU, self.connectPopup, menuConnect)
        self.Bind(wx.EVT_MENU, self.aboutProgram, menuAbout)
        
        self.titleScreen = wx.Panel(self)
        self.sizer.Add(self.titleScreen, flag=wx.EXPAND)
        startButton = wx.Button(self.titleScreen, -1, label='Start Game', pos=(30, 30))
        startButton.Bind(wx.EVT_BUTTON, self.newGamePopup)

    def newGamePopup(self, e):
        ''' Brings up a pop up menu that sets up a game based on the number of players specified.'''
        self.gamePrompt = NewGamePrompt(None, self, 'New Game', 200, 300)
        self.gamePrompt.Show(True)

    def newGameStart(self, e):
        ''' Starts a game with the specified nunber of players.'''
        numberOfPlayers = self.gamePrompt.numberOfPlayers
        playerNameList = []
        playerNameList.append("Empty")
        playerNameList.append(self.gamePrompt.playerOneName)
        playerNameList.append(self.gamePrompt.playerTwoName)
        playerNameList.append(self.gamePrompt.playerThreeName)
        playerNameList.append(self.gamePrompt.playerFourName)
        
        self.gamePrompt.Close()
        self.table = Table(self, numberOfPlayers, playerNameList)
        
    def hostPopup(self, e):
        ''' Brings up the Online Host popup.'''
        self.hostPrompt = hostOnline(None, self, 'Host', 200, 300)
        self.hostPrompt.Show(True)
        
    def connectPopup(self, e):
        ''' Brings up the Online Connect popup.'''
        self.connectPrompt = connectOnline(None, self, 'Connect', 200, 300)
        self.connectPrompt.Show(True)
        
    def aboutProgram(self, e):
        prompt = wx.MessageDialog(self, 'Created by Jordan Barnes\nrjordanbarnes@gmail.com', 'About', wx.OK)
        prompt.ShowModal()
        prompt.Destroy()

    def exitProgram(self, e):
        try:
            self.gamePrompt.Close(True)
            self.Close(True)
        except:
            self.Close(True)

class hostOnline(wx.Frame):
    def __init__(self, parent, mainWindow, title, width, height):
        wx.Frame.__init__(self, parent, title=title, size=(width, height), style=wx.SYSTEM_MENU | wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.hostScreen = wx.Panel(self)
        
        # Layout Variables
        self.PLAYERNAMETEXTX = 15
        self.PLAYERNAMEBOXX = 105
        self.playerName = ""
        
        # Player name box
        self.playerNameText = wx.StaticText(self.hostScreen, label="Online Name ", pos=(self.PLAYERNAMETEXTX, 62))
        self.playerNameBox = wx.TextCtrl(self.hostScreen, value=self.playerName, pos=(self.PLAYERNAMEBOXX, 60), size=(80,-1))
        self.Bind(wx.EVT_TEXT, self.changePlayerName, self.playerNameBox)
        self.Bind(wx.EVT_CHAR, self.changePlayerName, self.playerNameBox)
        
        # Host button
        hostButton = wx.Button(self.hostScreen, -1, label='Host', pos=(55, 220))
        hostButton.Bind(wx.EVT_BUTTON, self.startHosting)
        
    def changePlayerName(self, e):
        self.playerName = e.GetString()
        print self.playerName
        
    def startHosting(self, e):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", 5084))
        server_socket.listen(5)

        print "Waiting for client..."

        client_socket, address = server_socket.accept()
        os.system("cls")
        print "Received a connection from ", address, "\n"
        while 1:
            data = raw_input ( "You: " )
            if (data.lower() == 'q'):
                client_socket.send (data)
                client_socket.close()
                break;
            else:
                print "\nWaiting for response..."
                client_socket.send(data)
                data = client_socket.recv(512)
                if (data.lower() == 'q'):
                    client_socket.close()
                    break;
                else:
                    os.system("cls")
                    print "Stranger: " , data
    
class connectOnline(wx.Frame):
    def __init__(self, parent, mainWindow, title, width, height):
        wx.Frame.__init__(self, parent, title=title, size=(width, height), style=wx.SYSTEM_MENU | wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.connectScreen = wx.Panel(self)
        
    def startConnecting(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverInput = raw_input ("Enter IP: ")
        client_socket.connect((serverInput, 5084))
        os.system("cls")
        address = client_socket.getpeername()
        print "Successfully connected to ", address, "\n"
        print "\nWaiting for response..."
        while 1:
            data = client_socket.recv(512)
            if (data.lower() == 'q'):
                client_socket.close()
                break;
            else:
                os.system("cls")
                print "Stranger: " , data
                data = raw_input ( "You: " )
                if (data <> 'Q' and data <> 'q'):
                    client_socket.send(data)
                    print "\nWaiting for response..."
                else:
                    client_socket.send(data)
                    client_socket.close()
                    break;
    
class NewGamePrompt(wx.Frame):  
    ''' The popup that appears that asks for the game parameters (player names, number of players).'''
    def __init__(self, parent, mainWindow, title, width, height):
        wx.Frame.__init__(self, parent, title=title, size=(width, height), style=wx.SYSTEM_MENU | wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.newGameScreen = wx.Panel(self)
        
        self.PLAYERNAMETEXTX = 15
        self.PLAYERNAMEBOXX = 105
        
        # The variables that are used in the Table
        self.numberOfPlayers = 1
        self.playerOneName = ""
        self.playerTwoName = ""
        self.playerThreeName = ""
        self.playerFourName = ""
        
        # Number of players dropdown
        self.numberOptions = ['1', '2', '3', '4']
        self.playersLabel = wx.StaticText(self.newGameScreen, label="Number of Players ", pos=(20, 18))
        self.numberDropdown = wx.ComboBox(self.newGameScreen, value=self.numberOptions[0], pos=(120, 15), size=(40, -1), choices=self.numberOptions, style=wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.changePlayers, self.numberDropdown)
        
        # Player name box
        self.playerOneText = wx.StaticText(self.newGameScreen, label="Player 1's Name ", pos=(self.PLAYERNAMETEXTX, 62))
        self.playerOneNameBox = wx.TextCtrl(self.newGameScreen, value=self.playerOneName, pos=(self.PLAYERNAMEBOXX, 60), size=(80,-1))
        self.Bind(wx.EVT_TEXT, self.changePlayerOneName, self.playerOneNameBox)
        self.Bind(wx.EVT_CHAR, self.changePlayerOneName, self.playerOneNameBox)
        
        # Confirm button
        confirmButton = wx.Button(self.newGameScreen, -1, label='Confirm', pos=(55, 220))
        confirmButton.Bind(wx.EVT_BUTTON, mainWindow.newGameStart)
        
    def changePlayers(self, e):
        ''' What happens when the number of players is changed.'''
        try:
            self.playerOneText.Destroy()
            self.playerOneNameBox.Destroy()
            self.playerTwoText.Destroy()
            self.playerTwoNameBox.Destroy()
            self.playerThreeText.Destroy()
            self.playerThreeNameBox.Destroy()
            self.playerFourText.Destroy()
            self.playerFourNameBox.Destroy()
        except:
            pass
        self.Refresh()
        
        self.numberOfPlayers = int(e.GetString())
        # Make player name boxes
        if self.numberOfPlayers is 1:
            self.playerOneText = wx.StaticText(self.newGameScreen, label="Player 1's Name ", pos=(self.PLAYERNAMETEXTX, 62))
            self.playerOneNameBox = wx.TextCtrl(self.newGameScreen, value=self.playerOneName, pos=(self.PLAYERNAMEBOXX, 60), size=(80,-1))
            self.Bind(wx.EVT_TEXT, self.changePlayerOneName, self.playerOneNameBox)
        elif self.numberOfPlayers is 2:
            self.playerOneText = wx.StaticText(self.newGameScreen, label="Player 1's Name ", pos=(self.PLAYERNAMETEXTX, 62))
            self.playerOneNameBox = wx.TextCtrl(self.newGameScreen, value=self.playerOneName, pos=(self.PLAYERNAMEBOXX, 60), size=(80,-1))
            self.Bind(wx.EVT_TEXT, self.changePlayerOneName, self.playerOneNameBox)
            
            self.playerTwoText = wx.StaticText(self.newGameScreen, label="Player 2's Name ", pos=(self.PLAYERNAMETEXTX, 92))
            self.playerTwoNameBox = wx.TextCtrl(self.newGameScreen, value=self.playerTwoName, pos=(self.PLAYERNAMEBOXX, 90), size=(80,-1))
            self.Bind(wx.EVT_TEXT, self.changePlayerTwoName, self.playerTwoNameBox)
        elif self.numberOfPlayers is 3:
            self.playerOneText = wx.StaticText(self.newGameScreen, label="Player 1's Name ", pos=(self.PLAYERNAMETEXTX, 62))
            self.playerOneNameBox = wx.TextCtrl(self.newGameScreen, value=self.playerOneName, pos=(self.PLAYERNAMEBOXX, 60), size=(80,-1))
            self.Bind(wx.EVT_TEXT, self.changePlayerOneName, self.playerOneNameBox)
            
            self.playerTwoText = wx.StaticText(self.newGameScreen, label="Player 2's Name ", pos=(self.PLAYERNAMETEXTX, 92))
            self.playerTwoNameBox = wx.TextCtrl(self.newGameScreen, value=self.playerTwoName, pos=(self.PLAYERNAMEBOXX, 90), size=(80,-1))
            self.Bind(wx.EVT_TEXT, self.changePlayerTwoName, self.playerTwoNameBox)
            
            self.playerThreeText = wx.StaticText(self.newGameScreen, label="Player 3's Name ", pos=(self.PLAYERNAMETEXTX, 122))
            self.playerThreeNameBox = wx.TextCtrl(self.newGameScreen, value=self.playerThreeName, pos=(self.PLAYERNAMEBOXX, 120), size=(80,-1))
            self.Bind(wx.EVT_TEXT, self.changePlayerThreeName, self.playerThreeNameBox)
        elif self.numberOfPlayers is 4:
            self.playerOneText = wx.StaticText(self.newGameScreen, label="Player 1's Name ", pos=(self.PLAYERNAMETEXTX, 62))
            self.playerOneNameBox = wx.TextCtrl(self.newGameScreen, value=self.playerOneName, pos=(self.PLAYERNAMEBOXX, 60), size=(80,-1))
            self.Bind(wx.EVT_TEXT, self.changePlayerOneName, self.playerOneNameBox)
            
            self.playerTwoText = wx.StaticText(self.newGameScreen, label="Player 2's Name ", pos=(self.PLAYERNAMETEXTX, 92))
            self.playerTwoNameBox = wx.TextCtrl(self.newGameScreen, value=self.playerTwoName, pos=(self.PLAYERNAMEBOXX, 90), size=(80,-1))
            self.Bind(wx.EVT_TEXT, self.changePlayerTwoName, self.playerTwoNameBox)
            
            self.playerThreeText = wx.StaticText(self.newGameScreen, label="Player 3's Name ", pos=(self.PLAYERNAMETEXTX, 122))
            self.playerThreeNameBox = wx.TextCtrl(self.newGameScreen, value=self.playerThreeName, pos=(self.PLAYERNAMEBOXX, 120), size=(80,-1))
            self.Bind(wx.EVT_TEXT, self.changePlayerThreeName, self.playerThreeNameBox)
            
            self.playerFourText = wx.StaticText(self.newGameScreen, label="Player 4's Name ", pos=(self.PLAYERNAMETEXTX, 152))
            self.playerFourNameBox = wx.TextCtrl(self.newGameScreen, value=self.playerFourName, pos=(self.PLAYERNAMEBOXX, 150), size=(80,-1))
            self.Bind(wx.EVT_TEXT, self.changePlayerFourName, self.playerFourNameBox)
            
    def changePlayerOneName(self, e):
        self.playerOneName = e.GetString()
        
    def changePlayerTwoName(self, e):
        self.playerTwoName = e.GetString()
        
    def changePlayerThreeName(self, e):
        self.playerThreeName = e.GetString()
        
    def changePlayerFourName(self, e):
        self.playerFourName = e.GetString()
                 
class Table(wx.Panel):
    def __init__(self, parent, numberOfPlayers, playerNames):
        '''Creates a table that creates all variables of the current game.'''
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour((52, 157, 117))
        self.parent = parent
        self.CARDX = 30
        self.CARDY = 300
        self.CARDWIDTH = 120
        self.CARDHEIGHT = 168
        self.CARDSPACING = self.CARDWIDTH + 5
        self.DEALERCARDX = 320
        self.DEALERCARDY = 30
        self.TEXTSPACING = 50
        if numberOfPlayers == 1:
            self.player1 = Player(playerNames[1])
            self.playerList = [self.player1]
        elif numberOfPlayers == 2:
            self.player1 = Player(playerNames[1])
            self.player2 = Player(playerNames[2])
            self.playerList = [self.player1, self.player2]
        elif numberOfPlayers == 3:
            self.player1 = Player(playerNames[1])
            self.player2 = Player(playerNames[2])
            self.player3 = Player(playerNames[3])
            self.playerList = [self.player1, self.player2, self.player3]
        elif numberOfPlayers == 4:
            self.player1 = Player(playerNames[1])
            self.player2 = Player(playerNames[2])
            self.player3 = Player(playerNames[3])
            self.player4 = Player(playerNames[4])
            self.playerList = [self.player1, self.player2, self.player3, self.player4]
        self.dealer = AI('Dealer', 2000)
        self.playerList.append(self.dealer)
        self.deck = Deck()
        self.deck.shuffle()
        self.currentPlayer = 0
        for player in self.playerList:
            player.state = 'waiting'
            player.draw(self.deck)
            player.draw(self.deck)

        parent.sizer.Clear(True)
        parent.sizer.Add(self, flag=wx.EXPAND)
        parent.sizer.Layout()
        self.renderTable(wx.EVT_PAINT)

    def newRound(self, e):
        ''' Resets all cards for a new round.'''
        for player in self.playerList:
            player.discardHand(self.deck)

        self.deck = Deck()
        self.deck.shuffle()
        for player in self.playerList:
            if player.state is not 'out':
                player.state = 'waiting'
                player.draw(self.deck)
                player.draw(self.deck)

        self.nextTurn(wx.EVT_PAINT)

    def renderTable(self, e):
        ''' Draws what's on the screen. Acts as the main loop.'''
        self.DestroyChildren()
        self.message = ''
        self.Refresh()
        self.Bind(wx.EVT_LEFT_DOWN, None)
        currentPlayer = self.playerList[self.currentPlayer]
        self.NAMEFONT = wx.Font(25, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL)
        self.NAMECOLOUR = 'white'
        gameEnded = self.checkGameEnd()
        ANNOUNCEMENTY = self.DEALERCARDY
        showAnnouncement = False
        for player in self.playerList:
            if player.state is 'out':
                showAnnouncement = True

        if showAnnouncement:
            self.Bind(wx.EVT_PAINT, self.voidCall)
            for player in self.playerList:
                if player.state is 'out':
                    outPlayerText = wx.StaticText(self, label=player.name + ' ran out of money!', pos=(self.CARDX, ANNOUNCEMENTY))
                    outPlayerText.SetFont(self.NAMEFONT)
                    outPlayerText.SetForegroundColour(self.NAMECOLOUR)
                    ANNOUNCEMENTY += self.TEXTSPACING

            for player in self.playerList:
                if player.state is 'out':
                    self.playerList.remove(player)

            self.Bind(wx.EVT_LEFT_DOWN, self.renderTable)
            for child in self.GetChildren():
                child.Bind(wx.EVT_LEFT_DOWN, self.renderTable)

            self.Refresh()
        elif gameEnded:
            self.Bind(wx.EVT_PAINT, self.voidCall)
            if self.playerList[0].name is 'Dealer':
                endResult = wx.StaticText(self, label='The dealer won.', pos=(self.CARDX, ANNOUNCEMENTY))
                endResult.SetFont(self.NAMEFONT)
                endResult.SetForegroundColour(self.NAMECOLOUR)
            else:
                for player in self.playerList:
                    endResult = wx.StaticText(self, label=player.name + ' ended with $' + str(player.money) + '.', pos=(self.CARDX, ANNOUNCEMENTY))
                    endResult.SetFont(self.NAMEFONT)
                    endResult.SetForegroundColour(self.NAMECOLOUR)
                    ANNOUNCEMENTY += self.TEXTSPACING

            newGameButton = wx.Button(self, -1, label='Play Again', pos=(350, 350))
            newGameButton.Bind(wx.EVT_BUTTON, self.parent.newGamePopup)
            self.Refresh()
        else:
            currentPlayer.state = 'playing'
            if currentPlayer.name is 'Dealer':
                currentPlayer.makeDecision(self.deck)
                self.Bind(wx.EVT_PAINT, self.renderDealerHands)
                self.calculateResults()
                dealerResult = ''
                if currentPlayer.calculatePoints() > 21:
                    currentPlayer.state = 'busted'
                    dealerResult = ' bust!'
                elif currentPlayer.calculatePoints() == 21 and len(currentPlayer.hand) < 3:
                    dealerResult = ' got Blackjack!'
                else:
                    dealerResult = ' got %s points' % currentPlayer.calculatePoints()
                dealerResultText = wx.StaticText(self, label=currentPlayer.name + dealerResult, pos=(self.CARDX, 30))
                dealerResultText.SetFont(self.NAMEFONT)
                dealerResultText.SetForegroundColour(self.NAMECOLOUR)
                self.checkPlayerStates()
                self.Refresh()
                self.Bind(wx.EVT_LEFT_DOWN, self.newRound)
                for child in self.GetChildren():
                    child.Bind(wx.EVT_LEFT_DOWN, self.newRound)

            else:
                points = currentPlayer.calculatePoints()
                if points > 21:
                    currentPlayer.state = 'busted'
                    self.message = 'Bust!'
                elif points == 21 and len(currentPlayer.hand) < 3:
                    currentPlayer.state = 'standing'
                    self.message = 'Blackjack!'
                self.currentPlayerName = wx.StaticText(self, label=self.message, pos=(300, 230))
                self.currentPlayerName.SetFont(self.NAMEFONT)
                self.currentPlayerName.SetForegroundColour(self.NAMECOLOUR)
                self.currentPlayerName = wx.StaticText(self, label=currentPlayer.name, pos=(30, 200))
                self.currentPlayerName.SetFont(self.NAMEFONT)
                self.currentPlayerName.SetForegroundColour(self.NAMECOLOUR)
                self.currentPlayerChips = wx.StaticText(self, label='$' + str(currentPlayer.money), pos=(30, 240))
                self.currentPlayerChips.SetFont(self.NAMEFONT)
                self.currentPlayerChips.SetForegroundColour(self.NAMECOLOUR)
                self.dealerName = wx.StaticText(self, label=self.dealer.name, pos=(600, 30))
                self.dealerName.SetFont(self.NAMEFONT)
                self.dealerName.SetForegroundColour(self.NAMECOLOUR)
                self.dealerChips = wx.StaticText(self, label='$' + str(self.dealer.money), pos=(600, 70))
                self.dealerChips.SetFont(self.NAMEFONT)
                self.dealerChips.SetForegroundColour(self.NAMECOLOUR)
                if currentPlayer.state is not 'playing':
                    self.Bind(wx.EVT_LEFT_DOWN, self.nextTurn)
                    for child in self.GetChildren():
                        child.Bind(wx.EVT_LEFT_DOWN, self.newRound)

                if currentPlayer.state is 'playing':
                    hitButton = wx.Button(self, -1, label='Hit', pos=(30, 500))
                    hitButton.Bind(wx.EVT_BUTTON, self.playerHit)
                    standButton = wx.Button(self, -1, label='Stand', pos=(120, 500))
                    standButton.Bind(wx.EVT_BUTTON, self.playerStand)
                self.Bind(wx.EVT_PAINT, self.renderHands)

    def renderHands(self, e):
        ''' Renders the player and dealer hand.'''
        width = self.CARDWIDTH
        height = self.CARDHEIGHT
        x = self.CARDX
        y = self.CARDY
        # Render the cards at the bottom of the screen (current player's card).
        for card in self.playerList[self.currentPlayer].hand:
            newCard = wx.PaintDC(self)
            newCard.BeginDrawing()
            newCard.SetPen(wx.Pen('black', style=wx.SOLID))
            newCard.SetBrush(wx.Brush('white', wx.SOLID))
            newCard.DrawRectangle(x, y, width, height)
            newCard.EndDrawing()
            newCard.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
            temp = card.split()
            if temp[2] == 'Diamonds':
                suite = 'suites/diamond.png'
                newCard.SetTextForeground('red')
            elif temp[2] == 'Hearts':
                suite = 'suites/heart.png'
                newCard.SetTextForeground('red')
            elif temp[2] == 'Clubs':
                suite = 'suites/club.png'
            elif temp[2] == 'Spades':
                suite = 'suites/spade.png'
            letter = ''
            letterWidth = 1
            if temp[0].isdigit():
                letter = temp[0]
                if temp[0] == '10':
                    letterWidth = 2
            elif temp[0] == 'Ace':
                letter = 'A'
            elif temp[0] == 'Jack':
                letter = 'J'
            elif temp[0] == 'Queen':
                letter = 'Q'
            elif temp[0] == 'King':
                letter = 'K'
            else:
                letter = ' '
            newCard.DrawText(letter, x + 14, y + 8)
            if letterWidth == 1:
                newCard.DrawText(letter, x + width - 28, y + height - 36)
            elif letterWidth == 2:
                newCard.DrawText(letter, x + width - 35, y + height - 35)
            suiteRender = wx.Bitmap(suite)
            newCard.DrawBitmap(suiteRender, x, y)
            x += self.CARDSPACING

        x = self.DEALERCARDX
        y = self.DEALERCARDY
        blankCard = True
        # Render the cards at the top of the screen
        if self.playerList[self.currentPlayer].name is not 'Dealer':
            for card in self.dealer.hand:
                newCard = wx.PaintDC(self)
                newCard.BeginDrawing()
                newCard.SetPen(wx.Pen('black', style=wx.SOLID))
                newCard.SetBrush(wx.Brush('white', wx.SOLID))
                newCard.DrawRectangle(x, y, width, height)
                newCard.EndDrawing()
                newCard.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
                if blankCard is False:
                    temp = card.split()
                    if temp[2] == 'Diamonds':
                        suite = 'suites/diamond.png'
                        newCard.SetTextForeground('red')
                    elif temp[2] == 'Hearts':
                        suite = 'suites/heart.png'
                        newCard.SetTextForeground('red')
                    elif temp[2] == 'Clubs':
                        suite = 'suites/club.png'
                    elif temp[2] == 'Spades':
                        suite = 'suites/spade.png'
                    letter = ''
                    letterWidth = 1
                    if temp[0].isdigit():
                        letter = temp[0]
                        if temp[0] == '10':
                            letterWidth = 2
                    elif temp[0] == 'Ace':
                        letter = 'A'
                    elif temp[0] == 'Jack':
                        letter = 'J'
                    elif temp[0] == 'Queen':
                        letter = 'Q'
                    elif temp[0] == 'King':
                        letter = 'K'
                    else:
                        letter = ' '
                    newCard.DrawText(letter, x + 14, y + 8)
                    if letterWidth == 1:
                        newCard.DrawText(letter, x + width - 28, y + height - 36)
                    elif letterWidth == 2:
                        newCard.DrawText(letter, x + width - 35, y + height - 35)
                    newCard.SetTextForeground('black')
                else:
                    suite = 'suites/blank.png'
                
                # Draws the suite (blank for cards that are flipped)                
                suiteRender = wx.Bitmap(suite)
                newCard.DrawBitmap(suiteRender, x, y)
                    
                x += self.CARDSPACING
                blankCard = False

    def renderDealerHands(self, e):
        ''' Renders the dealer's cards on the dealer screen.'''
        width = self.CARDWIDTH
        height = self.CARDHEIGHT
        x = self.CARDX
        y = self.DEALERCARDY + 60
        for card in self.dealer.hand:
            newCard = wx.PaintDC(self)
            newCard.BeginDrawing()
            newCard.SetPen(wx.Pen('black', style=wx.SOLID))
            newCard.SetBrush(wx.Brush('white', wx.SOLID))
            newCard.DrawRectangle(x, y, width, height)
            newCard.EndDrawing()
            newCard.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
            temp = card.split()
            if temp[2] == 'Diamonds':
                suite = 'suites/diamond.png'
                newCard.SetTextForeground('red')
            elif temp[2] == 'Hearts':
                suite = 'suites/heart.png'
                newCard.SetTextForeground('red')
            elif temp[2] == 'Clubs':
                suite = 'suites/club.png'
            elif temp[2] == 'Spades':
                suite = 'suites/spade.png'
            letter = ''
            letterWidth = 1
            if temp[0].isdigit():
                letter = temp[0]
                if temp[0] == '10':
                    letterWidth = 2
            elif temp[0] == 'Ace':
                letter = 'A'
            elif temp[0] == 'Jack':
                letter = 'J'
            elif temp[0] == 'Queen':
                letter = 'Q'
            elif temp[0] == 'King':
                letter = 'K'
            else:
                letter = ' '
            newCard.DrawText(letter, x + 14, y + 8)
            if letterWidth == 1:
                newCard.DrawText(letter, x + width - 28, y + height - 36)
            elif letterWidth == 2:
                newCard.DrawText(letter, x + width - 35, y + height - 35)
            suiteRender = wx.Bitmap(suite)
            newCard.DrawBitmap(suiteRender, x, y)
            x += self.CARDSPACING

    def calculateResults(self):
        y = self.CARDY
        dealerNetGain = 0
        result = ''
        for player in self.playerList:
            if player.name is not 'Dealer':
                if player.state is 'standing' or 'busted':
                    if player.state == 'busted':
                        result = '%s loses $100 (Bust)' % player.name
                        player.money -= 100
                    elif player.calculatePoints() < self.dealer.calculatePoints() and self.dealer.calculatePoints() <= 21:
                        result = '%s loses $100 (%i points)' % (player.name, player.calculatePoints())
                        player.money -= 100
                    elif player.calculatePoints() == self.dealer.calculatePoints() and self.dealer.calculatePoints() <= 21:
                        result = '%s pushes' % player.name
                    elif player.calculatePoints() == 21 and len(player.hand) < 3:
                        result = '%s wins $100 (Blackjack)' % player.name
                        player.money += 100
                        dealerNetGain -= 100
                    else:
                        result = '%s wins $100 (%i points)' % (player.name, player.calculatePoints())
                        player.money += 100
                        dealerNetGain -= 100
            elif dealerNetGain < 0:
                result = 'Dealer loses $%s' % (dealerNetGain * -1)
                self.dealer.money += dealerNetGain
            else:
                result = ''
            result = wx.StaticText(self, label=result, pos=(self.CARDX, y))
            result.SetFont(self.NAMEFONT)
            result.SetForegroundColour(self.NAMECOLOUR)
            y += self.TEXTSPACING

    def nextTurn(self, e):
        '''Changes the currentPlayer to the next player in the list.'''
        if self.currentPlayer < len(self.playerList) - 1:
            self.currentPlayer += 1
        else:
            self.currentPlayer = 0
        self.renderTable(wx.EVT_PAINT)

    def playerHit(self, e):
        self.playerList[self.currentPlayer].draw(self.deck)
        self.renderTable(wx.EVT_PAINT)

    def playerStand(self, e):
        self.playerList[self.currentPlayer].state = 'standing'
        self.nextTurn(wx.EVT_PAINT)

    def checkPlayerStates(self):
        for player in self.playerList:
            if player.money <= 0:
                player.state = 'out'

    def checkGameEnd(self):
        ''' Checks whether the game is over.'''
        if self.dealer.state == 'out':
            return True
        else:
            if self.playerList[0].name is 'Dealer':
                return True
            return False

    def voidCall(self, e):
        newCard = wx.PaintDC(self)

class Deck(object):
    '''A deck contains the cards. It's interacted with by the player(s).'''
    def __init__(self):
        self.contents = ['2 of Diamonds',
         '2 of Hearts',
         '2 of Clubs',
         '2 of Spades',
         '3 of Diamonds',
         '3 of Hearts',
         '3 of Clubs',
         '3 of Spades',
         '4 of Diamonds',
         '4 of Hearts',
         '4 of Clubs',
         '4 of Spades',
         '5 of Diamonds',
         '5 of Hearts',
         '5 of Clubs',
         '5 of Spades',
         '6 of Diamonds',
         '6 of Hearts',
         '6 of Clubs',
         '6 of Spades',
         '7 of Diamonds',
         '7 of Hearts',
         '7 of Clubs',
         '7 of Spades',
         '8 of Diamonds',
         '8 of Hearts',
         '8 of Clubs',
         '8 of Spades',
         '9 of Diamonds',
         '9 of Hearts',
         '9 of Clubs',
         '9 of Spades',
         '10 of Diamonds',
         '10 of Hearts',
         '10 of Clubs',
         '10 of Spades',
         'Jack of Diamonds',
         'Jack of Hearts',
         'Jack of Clubs',
         'Jack of Spades',
         'Queen of Diamonds',
         'Queen of Hearts',
         'Queen of Clubs',
         'Queen of Spades',
         'King of Diamonds',
         'King of Hearts',
         'King of Clubs',
         'King of Spades',
         'Ace of Diamonds',
         'Ace of Hearts',
         'Ace of Clubs',
         'Ace of Spades']

    def shuffle(self):
        '''Randomize the order of the cards in the deck.'''
        random.shuffle(self.contents)

    def removeTopCard(self):
        '''Remove the top card of the deck.'''
        self.contents.pop(0)

    def addCard(self, card):
        '''Add card to the bottom of the deck.'''
        self.contents.append(card)

class Player(object):
    '''A player has a hand and a name. Interacts with the deck.'''


    def __init__(self, playerName):
        self.hand = []
        self.name = playerName
        self.points = 0
        self.money = 1000
        self.state = 'waiting'

    def draw(self, deck):
        '''Draw a card from deck and tell the deck to remove its top card.'''
        self.hand.append(deck.contents[0])
        deck.removeTopCard()

    def discardHand(self, deck):
        '''Puts hand into deck and clears hand.'''
        for i in self.hand:
            deck.addCard(i)

        self.hand = []

    def calculatePoints(self):
        '''Figures out how many points the player's hand is worth.'''
        points = 0
        numberOfAces = 0
        for card in self.hand:
            temp = card.split()
            if temp[0].isdigit():
                points += int(temp[0])
            elif temp[0] == 'Ace':
                points += 11
                numberOfAces += 1
            else:
                points += 10

        while numberOfAces > 0 and points > 21:
            numberOfAces -= 1
            points -= 10

        return points

class AI(Player):

    def __init__(self, playerName, money):
        self.hand = []
        self.name = playerName
        self.points = 0
        self.money = money
        self.state = 'waiting'

    def makeDecision(self, deck):
        while self.calculatePoints() <= 16:
            self.draw(deck)

app = wx.App(False)
frame = MainWindow(None, 'Blackjack', WIDTH, HEIGHT)
frame.Show(True)
app.MainLoop()

