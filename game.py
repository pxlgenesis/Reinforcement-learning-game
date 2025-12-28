import pygame 
import sys

vector = pygame.math.Vector2

class Game: #Game Structure template OOPS compliant
    
    def __init__(self, width: int, height:int): # [<var>: type] INITIALIZE ALL GAME MODULES
        
        pygame.init() #initialize all pygame modules to check

        self.height = height 
        self.width = width
        
        self.screen = pygame.display.set_mode((self.width,self.height)) #Game Window size 
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.fps = 60

        self.background_img = pygame.image.load(r"assets/background.png") #USE [r""] for raw strings
        self.Pipe_img = pygame.image.load(r"assets\Pipe_16x64.png")
        self.Bird_img = pygame.image.load(r"assets\Bird_idle_1.png")
        self.Bird_img2 = pygame.image.load(r"assets\Bird_idle_3.png")
        self.ground_img = pygame.image.load(r"assets\ground.png")

        self.background_img = pygame.transform.scale_by(self.background_img,3)
        self.Pipe_img = pygame.transform.scale_by(self.Pipe_img,3)
        self.Bird_img = pygame.transform.scale_by(self.Bird_img,2)
        self.Bird_img2 = pygame.transform.scale_by(self.Bird_img2,2)
        self.ground_img = pygame.transform.scale_by(self.ground_img,3)

        self.background_rect = self.background_img.get_rect()
        self.Pipe_rect = self.Pipe_img.get_rect()
        self.Bird_rect = self.Bird_img.get_rect()
        self.Bird_rect2 = self.Bird_img2.get_rect()
        self.ground_rect = self.ground_img.get_rect()

        #velocity and gravity
        self.velocity = vector(0,0)

        #Delta time initialization to 0
        self.dt = 0
        self.pos_y= (self.background_img.get_rect()[3]-self.ground_img.get_rect()[3])/2 #(480 - (480*7)/10)/2
        self.gnd_x = 0 # ground x pos initialization

    def background_draw(self): #################### Background Render ###########################
        
        self.screen.blit(self.background_img,self.background_rect)

    def draw_ground(self): #################### ground Render ###########################

        ground_speed = 120
        # initial movement 
        self.gnd_x += ground_speed * self.dt
        if self.gnd_x >= self.width:
            self.gnd_x = 0 

        #draw rect
        move_ground_1 = pygame.Rect(self.gnd_x,(self.height*7)/10,self.ground_img.get_rect()[2],self.ground_img.get_rect()[3])
        move_ground_2 = pygame.Rect(self.gnd_x-self.width,(self.height*7)/10,self.ground_img.get_rect()[2],self.ground_img.get_rect()[3])

        #draw ground [note could be an issue with a little jitter, use group sprite next time]
        self.screen.blit(self.ground_img,move_ground_1)
        self.screen.blit(self.ground_img,move_ground_2)

    def player_draw(self): #################### Player Render ###########################
        #player sprite size

       
        bird_sprite_size: tuple[int, int] = (self.Bird_img.get_rect()[2],self.Bird_img.get_rect()[3])
        self.player_rect = pygame.Rect((self.width*5)/16,self.pos_y,*bird_sprite_size)

        #updating 
        self.pos_y += self.velocity.y
        
        # Collision box render
        pygame.draw.line(self.screen,"red",(self.player_rect[0],self.pos_y),(self.player_rect[0]+self.Bird_img.get_rect()[3],self.pos_y),2) #top
        pygame.draw.line(self.screen,"red",(self.player_rect[0],self.pos_y + self.Bird_img.get_rect()[2]),(self.player_rect[0]+self.Bird_img.get_rect()[3],self.pos_y+ self.Bird_img.get_rect()[2]),2) #bottom
        pygame.draw.line(self.screen,"red",(self.player_rect[0],self.pos_y),(self.player_rect[0],self.pos_y + self.Bird_img.get_rect()[2]),2) #left
        pygame.draw.line(self.screen,"red",(self.player_rect[0]+self.Bird_img.get_rect()[3],self.pos_y),(self.player_rect[0]+self.Bird_img.get_rect()[3],self.pos_y+ self.Bird_img.get_rect()[2]),2) #right

        #bird image render
        if self.velocity.y > 0:
            self.screen.blit(self.Bird_img,self.player_rect)
        if self.velocity.y < 0:
            self.screen.blit(self.Bird_img2,self.player_rect)
        


    def pipe_draw(self): #################### Pipe Render ###########################
        
        #pipe sprite size definition
        pipe_sprite_size: tuple[int, int] = (self.Pipe_img.get_rect()[2],self.Pipe_img.get_rect()[3])
        pipe_rect = pygame.Rect(12,3,*pipe_sprite_size)

        self.screen.blit(self.Pipe_img,pipe_rect)

    def handle(self): #################### Check Player Input ###########################
        
        #Game Termination event.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                    self.game_running = False
        
        #Get status of keys
        self.keys = pygame.key.get_pressed()

        #movement handling
        if self.keys[pygame.K_SPACE]:
            self.velocity.y = -3

    def update(self): #################### Simulation Loop ###########################

        # Current delta time calculation and last_time updation
        self.dt = self.clock.tick(self.fps)/1000
        

        # Bird velocity update cycle
        if self.velocity.y  < 3:
            self.velocity.y += 0.5 * self.dt * 9.8

        # Collision detection of ground
        if (self.pos_y +self.Bird_img.get_rect()[3]) > (self.height * 7)/10:
                pygame.QUIT
                sys.exit()
    
        # Loading Background and cleaning using black
        self.screen.fill("black")
        
        # Draw background func
        self.background_draw()

        # Call player draw 
        self.player_draw()

        #Load pipe
        self.pipe_draw()

        #Load ground
        self.draw_ground()
        
        #Update all parts of the display
        pygame.display.update()
        #pygame.display.update() [to update only certain parts]


        #debug shi
        print(f"bird_y:{self.pos_y} | velocity:{self.velocity} | dt: {self.dt}")
        


        
    def run(self): #################### Game Loop ###########################
        
        while self.game_running:
            
            self.update()
            self.handle()
            
            
        

def main():

    size: tuple[int, int] = (768,480)

    #Initilize window size
    game = Game(*size) #Create game object | [*var] is used to unpack a tuple. tuple can be created in ways eg a=() and accessed in a[] 
    game.run()

    #Terminate pygame and python interpretor
    pygame.quit()
    sys.exit()   

if __name__ == "__main__":
    main()