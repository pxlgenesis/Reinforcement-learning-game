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
        self.Bird_vel_up_img = pygame.image.load(r"assets\Bird_idle_1.png")
        self.Bird_vel_bwn_img = pygame.image.load(r"assets\Bird_idle_2.png")
        self.Bird_vel_down_img = pygame.image.load(r"assets\Bird_idle_3.png")
        self.ground_img = pygame.image.load(r"assets\ground.png")

        self.background_img = pygame.transform.scale_by(self.background_img,3)
        self.Pipe_img = pygame.transform.scale_by(self.Pipe_img,3)
        self.Bird_vel_up_img = pygame.transform.scale_by(self.Bird_vel_up_img,2)
        self.Bird_vel_bwn_img = pygame.transform.scale_by(self.Bird_vel_bwn_img,2)
        self.Bird_vel_down_img = pygame.transform.scale_by(self.Bird_vel_down_img,2)        
        self.ground_img = pygame.transform.scale_by(self.ground_img,3)

        self.background_rect = self.background_img.get_rect()
        self.Pipe_rect = self.Pipe_img.get_rect()
        self.Bird_rect = self.Bird_vel_bwn_img.get_rect()
        self.ground_rect = self.ground_img.get_rect()

        self.test = 0

        #bird rotation default angle
        self.bird_rot_angle = 0

        # Dev mode bool
        self.dev_mode = False

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

       
        bird_sprite_size: tuple[int, int] = (self.Bird_vel_bwn_img.get_rect()[2],self.Bird_vel_bwn_img.get_rect()[3])
        self.player_rect = pygame.Rect((self.width*5)/16,self.pos_y,*bird_sprite_size)

        #updating 
        self.pos_y += self.velocity.y

        #bird image render
        if self.velocity.y > 1:
            self.bird_img_final = self.Bird_vel_down_img
        elif self.velocity.y < -1:
            self.bird_img_final = self.Bird_vel_up_img
        else: 
            self.bird_img_final = self.Bird_vel_bwn_img

        
        self.bird_img_final = pygame.transform.rotate(self.bird_img_final,self.bird_rot_angle)

        self.screen.blit(self.bird_img_final,self.player_rect)
        
    def pipe_draw(self): #################### Pipe Render ###########################
        
        #pipe sprite size definition
        pipe_sprite_size: tuple[int, int] = (self.Pipe_img.get_rect()[2],int(self.height*1/10))
        pipe_rect = pygame.Rect(600,3,*pipe_sprite_size)

        pipe_img_rot = pygame.transform.rotate(self.Pipe_img,self.test)

        self.test  += 50 * self.dt
        
        if self.test >= 360:
            self.test = 0

        self.screen.blit(pipe_img_rot,pipe_rect)

    def dev_boxes(self): ##################### Pipe Render ###########################
        #render all of the boxes for player,gnd and pipe collosion and more.
        
        # Collision line ground
        pygame.draw.line(self.screen,"red",(0,(self.height*7)/10),(self.ground_rect[2],(self.height*7)/10),2)

        # Collision line sky
        pygame.draw.line(self.screen,"red",(0,0),(self.ground_rect[2],0),2)  
        
        # Collision box render
        pygame.draw.line(self.screen,"red",(self.player_rect[0],self.pos_y),(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y),2) #top
        pygame.draw.line(self.screen,"red",(self.player_rect[0],self.pos_y + self.Bird_vel_bwn_img.get_rect()[2]),(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y+ self.Bird_vel_bwn_img.get_rect()[2]),2) #bottom
        pygame.draw.line(self.screen,"red",(self.player_rect[0],self.pos_y),(self.player_rect[0],self.pos_y + self.Bird_vel_bwn_img.get_rect()[2]),2) #left
        pygame.draw.line(self.screen,"red",(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y),(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y+ self.Bird_vel_bwn_img.get_rect()[2]),2) #right


    def handle(self): #################### Check Player Input ###########################
        
        #Game Termination event.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                    self.game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.velocity.y = -3        
                if event.key == pygame.K_2 and self.dev_mode == False:
                    self.dev_mode = True        
                if event.key == pygame.K_1 and self.dev_mode == True:
                    self.dev_mode = False  

        #this would be used if i want to detect this per frame but i only need to detect it once hence event type.
        #Get status of keys
        #self.keys = pygame.key.get_pressed()

        #movement handling
        #if self.keys[pygame.K_SPACE]:
        #    self.velocity.y = -3

       


    def update(self): #################### Simulation Loop ###########################

        # Current delta time calculation and last_time updation
        self.dt = self.clock.tick(self.fps)/1000
        
        #new_value = new_min + value * (new_max - new_min) rotation angle transformtion from velocity to rotation
        self.bird_rot_angle = 30 + (((self.velocity.y*1)+3)/6) * (-30-(30))
        

        # Bird velocity update cycle
        if self.velocity.y < 3:
            self.velocity.y += 0.5 * self.dt * 9.8
            self.velocity.y = min(self.velocity.y,3)
        
        
        


        # Collision detection of ground
        if (self.pos_y +self.Bird_vel_bwn_img.get_rect()[3]) > (self.height * 7)/10:
                pygame.QUIT
                sys.exit()

        # Collision detection of sky
        if (self.pos_y ) < 0:
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

        #draw development boxes
        if self.dev_mode == True:
            self.dev_boxes()
        
        #Update all parts of the display
        pygame.display.update()
        #pygame.display.update() [to update only certain parts]

        #debug shi
        print(f"bird_y:{self.pos_y} | int(velocity:{self.velocity.y}) | dt: {self.dt} | {self.bird_rot_angle}")
        


        
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