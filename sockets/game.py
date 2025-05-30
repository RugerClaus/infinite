import pygame 
from network import Network

width ,height = 500,500

win = pygame.display.set_mode((width,height))

clientNumber = 0

class Player():
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.val = 3

    def draw(self,win,):
        pygame.draw.rect(win,self.color,self.rect)
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_A]: #left
            self.x -= self.val
        if keys[pygame.K_D]: #right
            self.x += self.val
        if keys[pygame.K_W]: #up
            self.y -= self.val
        if keys[pygame.K_S]: #down
            self.y += self.val

        self.update()

    def update(self):
        self.rect = (self.x,self.y,self.width,self.height)


def redrawWindow(win,player,player2):
    win.fill("white")
    player.draw(win)
    player2.draw(win)
    pygame.display.flip()

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def main():
    

    clock = pygame.time.Clock()

    run = True
    n = Network()
    startpos = read_pos(n.get_pos())
    p = Player(startpos[0],startpos[1],100,100,(0,255,128))
    p2 = Player(0,0,100,100,(0,255,128))
    while run:
        clock.tick(60)
        p2pos = read_pos(n.send(make_pos((p.x,p.y))))
        p2.x = p2pos[0]
        p2.y = p2pos[1]
        p.update()
        p2.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
        p.move()
        redrawWindow(win,p,p2)
main()