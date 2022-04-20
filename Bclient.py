from tabnanny import check
import pygame
from Bnetwork import Network
import pickle
#impot pygame and then start the thing to do its thing to make the thing. (initalise and access its fuctions)
pygame.font.init()

#set window perams and give name to window
width = 800
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Becca-RPS")

class Button: 
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 75
        self. height = 50

    def draw(self, win): # draw fucntion
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("AvantGarde", 20)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2),
                        self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos): # AABB collision
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redrawWindow(win, game, p):
    win.fill((225, 225, 225))

    if not (game.connected()):
        font = pygame.font.SysFont("AvantGarde", 40)
        text = font.render("waiting for player", 1, (255,125,125), True)
        win.blit(text, (width/2 - text.get_width() 
                 /2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("AvantGarde", 30)
        text = font.render("Your move", 1, (0, 255,255))
        win.blit(text, (30,100))

        text = font.render("Opponents", 1,(0,255,255))
        win.blit(text, (200,100))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0,0,0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("locked in", 1, (0,0,0))
            else:
                text1 = font.render("waiting", 1, (0,0,0))

            if game.p2Went and p == 1:
                text2 = font.render(move1, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("locked in", 1, (0,0,0))
            else:
                text2 = font.render("waiting", 1, (0,0,0))

        if p == 1:
            win.blit(text2, (50, 175))
            win.blit(text1, (200, 175))
        else:
            win.blit(text1, (50, 175))
            win.blit(text2, (200, 175))
        for btn in btns:
            btn.draw(win)

    pygame.display.update()

btns = [Button("Rock", 25, 250, (0, 0, 0)), Button(
    "scissors", 125, 250, (255, 0, 0)), Button("Paper", 255, 250, (0,255,0))]

LoginUsr = [Button("A", 25, 250, (0, 0, 0)), Button(
    "B", 125, 250, (255, 0, 0)), Button("C", 255, 250, (0,255,0)), Button("D", 355, 250, (0,255,255))]

LoginPass = [Button("1", 25, 250, (0, 0, 0)), Button(
    "2", 125, 250, (255, 0, 0)), Button("3", 255, 250, (0,255,0)), Button("4", 355, 250, (0,255,255))]

def main():
    run = False
    clock = pygame.time.Clock()
    n = Network()
    
    login = True 
    while login: # loop to check login
        clock.tick(60)
        pygame.display.update()
        win.fill((225, 225, 225)) #change window to color
        pygame.display.update()
        # example send n.send_data(btn.text)
        font = pygame.font.SysFont("AvantGarde", 40)
        SendUser = True
        SendPass = True
        while SendUser: # loop to send username to server
            Message = n.receive_data()
            print(Message)
            for btn in LoginUsr: #draw login numpad
                btn.draw(win)
            UserName=('')  
            i = 0  
            while (i<4): #while loop to get player input with buttons using pos

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for btn in LoginUsr:
                            if btn.click(pos):
                                UserName += btn.text #add the button pressed to the string
                                
                                i = i + 1
                pygame.display.update()
            
            if i == 4: #once password limit reached, send to server (Yes 4 is a small number, proof of concept only)
                n.send_data(UserName)
                print(UserName)
                SendUser = False

        while SendPass: # same function as sending username just for a password instead
            
            print('Enter Password:')
            for btn in LoginPass:
                btn.draw(win)
            PassName=('')  
            i = 0  
            while (i<4):

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for btn in LoginPass:
                            if btn.click(pos):
                                PassName += btn.text
                                print(PassName)
                                i = i + 1
                pygame.display.update()
            
            
           
            
            if i == 4: 
                n.send_data(PassName)
                SendPass = False


        Check = n.Check_msg() # checking messages from the server
        print(Check)
        UsrReg = ('Registration Successful')
        UsrDeni = ('Login failed')
        UsrConn = ('Connection successful')
        if Check == UsrReg: # if new user, ask user to login
            SendPass = True
            SendUser = True
            print('Please login with new account: ')

        if Check == UsrDeni: #if password wrong ask again
            SendPass = True
            SendUser = True
            print('Incorrect password, please try again: ')
        
        if Check == UsrConn: #if correct user /pass then proceed to game
            login = False
            player = int(n.getP())
            print("You are player", player)
            run = True
            

    

    while run:
        clock.tick(60)
        try:
            game = n.send_data("get")
        except:
            run = False
            print("Could not get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send_data("reset")
            except:
                run = False
                print("could not get game")
                break

            font = pygame.font.SysFont("AvantGarde", 40)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("you won", 1, (0, 255, 0))
            elif game.winner() == -1:
                text = font.render("Tie", 1, (125,125,125))
            else:
                text = font.render("you lost", 1, (255,0,0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send_data(btn.text)
                        else:
                            if not game.p2Went:
                                n.send_data(btn.text)
            
            redrawWindow(win,game,player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0,0,0))
        font = pygame.font.SysFont("AvantGarde", 40)
        text = font.render("Click to Begin", 1,(255,255,255))
        win.blit(text, (1,1))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()

while True:
    menu_screen()

            