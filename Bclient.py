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

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

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

            