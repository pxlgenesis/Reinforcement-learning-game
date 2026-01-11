import pygame 
import sys


vector = pygame.math.Vector2

class Game: #Game Structure template OOPS compliant indeed
    
    def __init__(self, width: int, height:int): # [<var>: type] INITIALIZE ALL GAME MODULES
        
        pygame.init() #initialize all pygame modules to check

        self.height = height 
        self.width = width
        
        self.screen = pygame.display.set_mode((self.width,self.height)) #Game Window size 
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.fps = 144 #bruh ive done something as frame effects velocity prolly clock related ill work on that in the future

        self.background_img = pygame.image.load(r"assets/background.png") #USE [r""] for raw strings
        self.Pipe_img = pygame.image.load(r"assets\Pipe_16x64.png")
        self.Pipe_rev_img = pygame.image.load(r"assets\pipe_upside.png")
        self.Bird_vel_up_img = pygame.image.load(r"assets\Bird_idle_1.png")
        self.Bird_vel_bwn_img = pygame.image.load(r"assets\Bird_idle_2.png")
        self.Bird_vel_down_img = pygame.image.load(r"assets\Bird_idle_3.png")
        self.ground_img = pygame.image.load(r"assets\ground.png") #ground image asset size is larger than background maybe due the way its drawn or

        # Using the transform library in pygame rescale image (note: doesnt blur can used filters in the future for a diff pixel game)
        self.background_img = pygame.transform.scale_by(self.background_img,3)
        self.Pipe_img = pygame.transform.scale_by(self.Pipe_img,3)
        self.Pipe_rev_img = pygame.transform.scale_by(self.Pipe_rev_img,3)
        self.Bird_vel_up_img = pygame.transform.scale_by(self.Bird_vel_up_img,2)
        self.Bird_vel_bwn_img = pygame.transform.scale_by(self.Bird_vel_bwn_img,2)
        self.Bird_vel_down_img = pygame.transform.scale_by(self.Bird_vel_down_img,2)        
        self.ground_img = pygame.transform.scale_by(self.ground_img,3)

        self.background_rect = self.background_img.get_rect()
        self.Pipe_rect = self.Pipe_img.get_rect()
        self.Pipe_rev_rect = self.Pipe_img.get_rect()
        self.Bird_rect = self.Bird_vel_bwn_img.get_rect()
        self.ground_rect = self.ground_img.get_rect()

        self.test = 0

        #bird rotation default angle
        self.bird_rot_angle = 0

        # Dev mode bool
        self.dev_mode = False

        # Velocity and Accelation initilization
        self.velocity = vector(0,0)
        self.accelation = vector(0,0)

        #Delta time initialization to 0
        self.dt = 0
        self.pos_y= (self.background_img.get_rect()[3]-self.ground_img.get_rect()[3])/2 #(480 - (480*7)/10)/2
        self.gnd_x = 0 # ground x pos initialization



    def background_draw(self): #################### Background Render ###########################
        
        self.screen.blit(self.background_img,self.background_rect)



    def grid_dev(self): #################### Grid Render ###########################
        
        # Draws grid vertically
        for i in range(1, 11):
            y = int(self.height * i / 10)
            pygame.draw.line(
                self.screen,
                "red",
                (0, y),
                (self.width, y),
                2
                )
            
        # Draws grid horizontally    
        for j in range(1,17):
            x = int(self.width * j / 16)
            pygame.draw.line(
                self.screen,
                "red",
                (x,0),
                (x,self.height),
                2
                )



    def draw_ground(self): #################### ground Render ###########################

        #draw rect
        move_ground_1 = pygame.Rect(self.gnd_x,(self.height*7)/10,self.ground_img.get_rect()[2],self.ground_img.get_rect()[3])
        move_ground_2 = pygame.Rect(self.gnd_x-self.width,(self.height*7)/10,self.ground_img.get_rect()[2],self.ground_img.get_rect()[3])

        #draw ground [note could be an issue with a little jitter, use group sprite next time] not on my pc tho as of right now
        self.screen.blit(self.ground_img,move_ground_1)
        self.screen.blit(self.ground_img,move_ground_2)        



    def player_draw(self): #################### Player Render ###########################
        
        # Player sprite size
        bird_sprite_size = self.Bird_vel_bwn_img.get_size() #bird_sprite_size: tuple[int, int] = (self.Bird_vel_bwn_img.get_rect()[2],self.Bird_vel_bwn_img.get_rect()[3]) 
        self.player_rect = pygame.Rect((self.width*5)/16,self.pos_y,*bird_sprite_size)

        # Bird sprite state 
        if self.velocity.y > 100:
            self.bird_img_final = self.Bird_vel_down_img
        elif self.velocity.y < -100:
            self.bird_img_final = self.Bird_vel_up_img
        else: 
            self.bird_img_final = self.Bird_vel_bwn_img

        # Current sprite state Rotation and draw
        self.bird_img_final = pygame.transform.rotate(self.bird_img_final,self.bird_rot_angle)
        self.screen.blit(self.bird_img_final,self.player_rect)
        


    def pipe_draw(self): #################### Pipe Render ###########################
        
        # Pipe sprite coordinates
        pipe_crd: tuple[ float, float, float, float] = (self.width - self.gnd_x ,(self.height*6)/10 ,self.width - self.gnd_x ,(self.height*0)/10 - (self.height*1)/10)

        

        self.screen.blit(self.Pipe_img,(pipe_crd[0],pipe_crd[1]))
        self.screen.blit(self.Pipe_rev_img,(pipe_crd[2],pipe_crd[3]))

        self.screen.blit(self.Pipe_img,(pipe_crd[0]+(self.width*3)/16,pipe_crd[1]))
        self.screen.blit(self.Pipe_rev_img,(pipe_crd[2]+(self.width*4)/16,pipe_crd[3]))

        self.screen.blit(self.Pipe_img,(pipe_crd[0]+(self.width*6)/16,pipe_crd[1]))
        self.screen.blit(self.Pipe_rev_img,(pipe_crd[2]+(self.width*8)/16,pipe_crd[3]))

        self.screen.blit(self.Pipe_img,(pipe_crd[0]+(self.width*9)/16,pipe_crd[1]))
        self.screen.blit(self.Pipe_rev_img,(pipe_crd[2]+(self.width*12)/16,pipe_crd[3]))


    def dev_boxes(self): ##################### Pipe Render ###########################
        
        """render all of the boxes for player,gnd and pipe collosion and more""" # """ used for 
        
        # Collision line ground
        pygame.draw.line(self.screen,"blue",(0,(self.height*7)/10),(self.ground_rect[2],(self.height*7)/10),2)

        # Collision line sky
        pygame.draw.line(self.screen,"blue",(0,0),(self.ground_rect[2],0),2)  
        
        # Collision box render
        pygame.draw.line(self.screen,"blue",(self.player_rect[0],self.pos_y),(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y),2) #top
        pygame.draw.line(self.screen,"blue",(self.player_rect[0],self.pos_y + self.Bird_vel_bwn_img.get_rect()[2]),(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y+ self.Bird_vel_bwn_img.get_rect()[2]),2) #bottom
        pygame.draw.line(self.screen,"blue",(self.player_rect[0],self.pos_y),(self.player_rect[0],self.pos_y + self.Bird_vel_bwn_img.get_rect()[2]),2) #left
        pygame.draw.line(self.screen,"blue",(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y),(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y+ self.Bird_vel_bwn_img.get_rect()[2]),2) #right



    def handle(self): #################### Check Player Input ###########################
        
        # Constants
        JUMP_VELOCITY = -350

        #Game Termination event.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                    self.game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.velocity.y = JUMP_VELOCITY     
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

        # Constants
        GROUND_SPD = 140
        GRAVITY = 1000 # based px/sec
        MAX_VELOCITY = 500

        # Current delta time calculation and last_time updation
        self.dt = self.clock.tick(self.fps)/1000
        
        # [new_value = new_min + value * (new_max - new_min)] rotation angle transformtion from velocity to rotation
        PRCNT_VAL = (self.velocity.y / MAX_VELOCITY)
        self.bird_rot_angle = 30 + (PRCNT_VAL) * (-30-(30))
        
        # Accelation
        self.accelation = GRAVITY 
        self.velocity.y += self.accelation * self.dt # Velocity is px/frame in short

        if self.velocity.y > MAX_VELOCITY:
            self.velocity.y = MAX_VELOCITY
        
        # Collision detection of ground
        if (self.pos_y +self.Bird_vel_bwn_img.get_rect()[3]) > (self.height * 7)/10:
                pygame.QUIT
                sys.exit()

        # Collision detection of sky
        if (self.pos_y ) < 0:
                pygame.QUIT
                sys.exit()

        # Updating Y positon
        self.pos_y += self.velocity.y * self.dt

        
        # Simple 2D scrolling by using 2 images and upating their values based on if it touches the end or not.
        self.gnd_x += GROUND_SPD * self.dt
        if self.gnd_x >= self.width:
            self.gnd_x = 0 
                

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
            self.grid_dev()
            self.dev_boxes()
            
        
        #Update all parts of the display
        pygame.display.update()
        #pygame.display.update() [to update only certain parts]

        #debug shi
        print(f"bird_y:{int(self.pos_y)} | int(velocity:{int(self.velocity.y)}) | dt: {int(self.dt)} | {int(self.bird_rot_angle)} | {int(self.accelation)} | {self.velocity.x}")
        


        
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