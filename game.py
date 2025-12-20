import pygame

class Game: #Game Structure template OOPS comppliant
    def __init__(self, width: int, height:int): # [<var>: type]
        self.height = height #both stored in class mem by [self.]
        self.width = width
        pygame.init() #initialize all pygame modules to check
        self.screen = pygame.display.set_mode((self.width,self.height)) #Defining game window size
        self.clock = pygame.time.Clock()
        self.game_running = True

    def handle(self):
        print("here")

    def update(self):
        print("here")

    def run(self): #Game Loop
        while self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #type of event is quit then self game is set to False and terminate the game loop
                    self.game_running = False   
            self.screen.fill("green")
            pygame.display.flip()       
            self.clock.tick(60)
        

def main():
    game = Game(800,600) #Create game obj
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()