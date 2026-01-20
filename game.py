import pygame 
import sys
import random
import numpy

vector = pygame.math.Vector2

class Game: #Game yeah OOPS

    def __init__(self, width: int, height:int): # [<var>: type] INITIALIZE ALL GAME MODULES
        
        pygame.init() #initialize all pygame modules to check

        self.height = height 
        self.width = width  
        
        self.screen = pygame.display.set_mode((self.width,self.height)) #Game Window size 
        pygame.display.set_caption("Reinforcement Flappy")
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.fps = 240 #bruh ive done something as frame effects velocity prolly clock related ill work on that in the future

        self.background_img = pygame.image.load(r"assets/background.png") #USE [r""] for raw strings
        self.Pipe_img = pygame.image.load(r"assets\Pipe_16x64.png")
        self.Pipe_rev_img = pygame.image.load(r"assets\pipe_upside.png")
        self.Bird_vel_up_img = pygame.image.load(r"assets\Bird_idle_1.png")
        self.Bird_vel_bwn_img = pygame.image.load(r"assets\Bird_idle_2.png")
        self.Bird_vel_down_img = pygame.image.load(r"assets\Bird_idle_3.png")
        self.ground_img = pygame.image.load(r"assets\ground.png") #ground image asset size is larger than background maybe due the way its drawn or
        self.pause_img_hud = pygame.image.load(r"assets\pause.png")

        # Using the transform library in pygame rescale image (note: doesnt blur can used filters in the future for a diff pixel game)
        self.background_img = pygame.transform.scale_by(self.background_img,3)
        self.Pipe_img = pygame.transform.scale_by(self.Pipe_img,3)
        self.Pipe_rev_img = pygame.transform.scale_by(self.Pipe_rev_img,3)
        self.Bird_vel_up_img = pygame.transform.scale_by(self.Bird_vel_up_img,1.75)
        self.Bird_vel_bwn_img = pygame.transform.scale_by(self.Bird_vel_bwn_img,1.75)
        self.Bird_vel_down_img = pygame.transform.scale_by(self.Bird_vel_down_img,1.75)        
        self.ground_img = pygame.transform.scale_by(self.ground_img,3)
        self.pause_img_hud = pygame.transform.scale_by(self.pause_img_hud,3)

        self.background_rect = self.background_img.get_rect()
        self.Pipe_rect = self.Pipe_img.get_rect()
        self.Pipe_rev_rect = self.Pipe_img.get_rect()
        self.Bird_rect = self.Bird_vel_bwn_img.get_rect()
        self.ground_rect = self.ground_img.get_rect()
        self.pause_img_hud_rect = self.pause_img_hud.get_rect()
        
        FONT_SCORE = 32 #px
        FONT_RL = 16
        # Font
        self.font_score = pygame.font.Font(r'assets\font\RasterForgeRegular.ttf',FONT_SCORE)
        self.font_rl = pygame.font.Font(r'assets\font\RasterForgeRegular.ttf',FONT_RL)

        # Bird rotation default angle
        self.bird_rot_angle = 0

        # Dev mode bool
        self.dev_mode = True

        # Velocity and Accelation initilization
        self.velocity = vector(0,0)
        self.accelation = vector(0,0)

        #Delta time initialization to 0
        self.dt = 0
        self.pos_y= (self.background_img.get_rect()[3]-self.ground_img.get_rect()[3])/2 #(480 - (480*7)/10)/2
        self.gnd_x = 0 # ground x pos initialization
        self.pipe_x_speed = 0
        self.pipes_config = [[],[],[],[],[]] # type: ignore
        self.score_count = 0
        self.pause = False

        self.pipe_distance =  0
        self.pipe_size = 0
        self.bird_dist = 0
        self.vel_current = 0
        self.game_over_flag = False






###################################################### Render Block #####################################################################

    def background_draw(self): #################### Background Render #############################
        
        self.screen.blit(self.background_img,self.background_rect)



    def grid_dev_draw(self): #################### Grid Render ###########################
        
        # Draws grid vertically
        for i in range(1, 11):
            y = int(self.height * i / 10)
            pygame.draw.line(
                self.screen,
                "magenta",
                (0, y),
                (self.width, y),
                2
                )
            
        # Draws grid horizontally    
        for j in range(1,17):
            x = int(self.width * j / 16)
            pygame.draw.line(
                self.screen,
                "magenta",
                (x,0),
                (x,self.height),
                2
                )



    def draw_ground(self): #################### Ground Render ###########################

        GRN_Y_DRAW = (self.height*7)/10

        # Ground Position
        move_ground_1 = pygame.Rect(self.gnd_x,
                                    GRN_Y_DRAW,
                                    self.ground_img.get_rect()[2],
                                    self.ground_img.get_rect()[3])
        
        move_ground_2 = pygame.Rect(self.gnd_x-self.width,
                                    GRN_Y_DRAW,
                                    self.ground_img.get_rect()[2],
                                    self.ground_img.get_rect()[3])

        #draw ground [note could be an issue with a little jitter, use group sprite next time] not on my pc tho as of right now
        self.screen.blit(self.ground_img,move_ground_1)
        self.screen.blit(self.ground_img,move_ground_2)        



    def player_draw(self): #################### Player Render ###########################
        
        PLAYER_X_POS = (self.width*5)/16

        # Player sprite size
        bird_sprite_size = self.Bird_vel_bwn_img.get_size() #bird_sprite_size: tuple[int, int] = (self.Bird_vel_bwn_img.get_rect()[2],self.Bird_vel_bwn_img.get_rect()[3]) 
        
        self.player_rect = pygame.Rect(PLAYER_X_POS
                                       ,self.pos_y,
                                       *bird_sprite_size)

        # Bird sprite state 
        if self.velocity.y > 100:
            self.bird_img_final = self.Bird_vel_down_img
        elif self.velocity.y < -100:
            self.bird_img_final = self.Bird_vel_up_img
        else: 
            self.bird_img_final = self.Bird_vel_bwn_img

        # Current sprite state Rotation and draw
        self.bird_img_final = pygame.transform.rotate(self.bird_img_final,
                                                      self.bird_rot_angle)
        self.screen.blit(self.bird_img_final,
                         self.player_rect)
        


    def pipe_draw(self): #################### Pipe Render ###########################

        # When we reset we need to skip rendering the pipes without any information inside goddamn no wonder shi is all RED ~ WAEEEEEE

        if self.pipes_config[0] == []:
            return
        for pipe_num in range(0,5):

            # Drawing all pipes every single frame
            self.screen.blit(self.Pipe_img,(self.pipes_config[pipe_num][0],self.pipes_config[pipe_num][1]))
            self.screen.blit(self.Pipe_rev_img,(self.pipes_config[pipe_num][2],self.pipes_config[pipe_num][3]))

            # Drawing bounding boxes and Scoring area for all boxes
            if self.dev_mode == True:
                # Ground pipe Blue outlines
                pygame.draw.line(self.screen,"red",(self.pipes_config[pipe_num][0],self.pipes_config[pipe_num][1]),(self.pipes_config[pipe_num][0],self.pipes_config[pipe_num][1]+self.Pipe_img.get_size()[1]),3)
                pygame.draw.line(self.screen,"red",(self.pipes_config[pipe_num][0]+self.Pipe_img.get_size()[0],self.pipes_config[pipe_num][1]),(self.pipes_config[pipe_num][0]+self.Pipe_img.get_size()[0],self.pipes_config[pipe_num][1]+self.Pipe_img.get_size()[1]),3)
                pygame.draw.line(self.screen,"red",(self.pipes_config[pipe_num][0],self.pipes_config[pipe_num][1]),(self.pipes_config[pipe_num][0]+self.Pipe_img.get_size()[0],self.pipes_config[pipe_num][1]),3)
                pygame.draw.line(self.screen,"red",(self.pipes_config[pipe_num][0],self.pipes_config[pipe_num][1]+self.Pipe_img.get_size()[1]),(self.pipes_config[pipe_num][0]+self.Pipe_img.get_size()[0],self.pipes_config[pipe_num][1]),3)
                
                pygame.draw.line(self.screen,"red",(self.pipes_config[pipe_num][2],self.pipes_config[pipe_num][3]),(self.pipes_config[pipe_num][2],self.pipes_config[pipe_num][3]+self.Pipe_img.get_size()[1]),3)
                pygame.draw.line(self.screen,"red",(self.pipes_config[pipe_num][2]+self.Pipe_img.get_size()[0],self.pipes_config[pipe_num][3]),(self.pipes_config[pipe_num][2]+self.Pipe_img.get_size()[0],self.pipes_config[pipe_num][3]+self.Pipe_img.get_size()[1]),3)
                pygame.draw.line(self.screen,"red",(self.pipes_config[pipe_num][2],self.pipes_config[pipe_num][3]+self.Pipe_img.get_size()[1]),(self.pipes_config[pipe_num][2]+self.Pipe_img.get_size()[0],self.pipes_config[pipe_num][3]+self.Pipe_img.get_size()[1]),3)
                pygame.draw.line(self.screen,"red",(self.pipes_config[pipe_num][2],self.pipes_config[pipe_num][3]+self.Pipe_img.get_size()[1]),(self.pipes_config[pipe_num][2]+self.Pipe_img.get_size()[0],self.pipes_config[pipe_num][3]),3)

                # Green space rect
                green_score_rect = pygame.Rect(self.pipes_config[pipe_num][2],self.pipes_config[pipe_num][3]+self.Pipe_img.get_size()[1],self.Pipe_img.get_size()[0],self.Pipe_img.get_size()[1]*3/4)
                
                

                if self.pipes_config[pipe_num][4] == True and self.pipes_config[pipe_num][5] == False: 
                    pygame.draw.rect(self.screen,"green",green_score_rect,3)
                
                if self.pipes_config[pipe_num][4] == False and self.pipes_config[pipe_num][5] == False: 
                    pygame.draw.rect(self.screen,"red",green_score_rect,3)

                if self.pipes_config[pipe_num][5] == True: 
                    pygame.draw.rect(self.screen,"yellow",green_score_rect,3)


    def dev_boxes(self): ##################### Object Outline Render ###########################
        
        """render all of the boxes for player,gnd and pipe collosion and more""" # """ used for 
        
        # GROUND COLLISON LINE
        pygame.draw.line(self.screen,"red",(0,(self.height*7)/10),(self.ground_rect[2],(self.height*7)/10),2)

        # SKY COLLISON LINE
        pygame.draw.line(self.screen,"red",(0,0),(self.ground_rect[2],0),2)  
        
        # BIRD COLLISION BOX
        pygame.draw.line(self.screen,"green",(self.player_rect[0],self.pos_y),(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y),2) #top
        pygame.draw.line(self.screen,"green",(self.player_rect[0],self.pos_y + self.Bird_vel_bwn_img.get_rect()[2]),(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y+ self.Bird_vel_bwn_img.get_rect()[2]),2) #bottom
        pygame.draw.line(self.screen,"green",(self.player_rect[0],self.pos_y),(self.player_rect[0],self.pos_y + self.Bird_vel_bwn_img.get_rect()[2]),2) #left
        pygame.draw.line(self.screen,"green",(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y),(self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3],self.pos_y+ self.Bird_vel_bwn_img.get_rect()[2]),2) #right

        # BIRD DISTANCE FROM GROUND
        pygame.draw.line(   self.screen,
                            "blue",
                            (self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3]/2,self.pos_y),
                            (self.player_rect[0]+self.Bird_vel_bwn_img.get_rect()[3]/2,self.height * 7 / 10 ) ,
                            2 
                        )

    def hud(self, score_num: int): #################### Hud Render ###########################

        # Hud Position

        SCORE_POS: tuple [ int , float ] = ( int(self.width * 1 / 16) , self.height * 9 / 10)
        RL_HUD_X_Y: tuple [ float , float , float , float , int ] = ( self.height * 8 / 10 , self.height * 8.5 / 10 , self.height * 9 / 10 , self.height * 9.5 / 10 , int ( self.width * 6/ 16 )) 

        # Text is being rendered and stored as an image each time its being displayed
        score_render = self.font_score.render(f"SCORE : {self.score_count}",False,"white",None)
        score_render_rect = score_render.get_rect().center
        score_render_rect = (SCORE_POS)
        self.screen.blit(score_render,score_render_rect)
       
        if self.dev_mode == True:
            rl_hud_render_1 = self.font_rl.render(f"PIPE DISTANCE : {float(self.game_observation_state()[0])}",False,"white",None)
            rl_hud_render_2 = self.font_rl.render(f"PIPE GAP : {self.game_observation_state()[1]}",False,"white",None)
            rl_hud_render_3 = self.font_rl.render(f"BIRD Y : {self.game_observation_state()[2]}",False,"white",None)
            rl_hud_render_4 = self.font_rl.render(f"VELOCITY : {self.game_observation_state()[3]}",False,"white",None)
            
            rl_hud_render_1_rect = rl_hud_render_1.get_rect().center 
            rl_hud_render_2_rect = rl_hud_render_2.get_rect().center
            rl_hud_render_3_rect = rl_hud_render_3.get_rect().center
            rl_hud_render_4_rect = rl_hud_render_4.get_rect().center

            rl_hud_render_1_rect = (RL_HUD_X_Y[4],RL_HUD_X_Y[0])
            rl_hud_render_2_rect = (RL_HUD_X_Y[4],RL_HUD_X_Y[1])
            rl_hud_render_3_rect = (RL_HUD_X_Y[4],RL_HUD_X_Y[2])
            rl_hud_render_4_rect = (RL_HUD_X_Y[4],RL_HUD_X_Y[3])

            self.screen.blit(rl_hud_render_1,rl_hud_render_1_rect)
            self.screen.blit(rl_hud_render_2,rl_hud_render_2_rect)
            self.screen.blit(rl_hud_render_3,rl_hud_render_3_rect)
            self.screen.blit(rl_hud_render_4,rl_hud_render_4_rect)
        
        
        if self.pause == True:
            self.screen.blit(self.pause_img_hud,self.pause_img_hud_rect)


    def render(self): #################### Render Main ###########################
        
        # Loading Background and cleaning using black
        self.screen.fill("black")
        
        # Draw background
        self.background_draw()

        # Draw Player
        self.player_draw()
        

        #draw development boxes
        if self.dev_mode == True:
            self.grid_dev_draw()

        # Draw pipe
        self.pipe_draw()
        # Draw Ground
        self.draw_ground()
        self.hud(self.score_count)
        
        if self.dev_mode == True:
            self.dev_boxes()
        
        #Update all parts of the display
        pygame.display.update()
        #pygame.display.update() [to update only certain parts]
        

############################################ Render Block End ###################################################################




############################################ Input Handler Start ################################################################

    def handle(self): #################### Check Player Input ###########################
        
        # Constants
        JUMP_VELOCITY = -400

        #Game Termination event.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                    self.game_running = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE) and (self.pause == False):
                    self.velocity.y = JUMP_VELOCITY     
                if event.key == pygame.K_2 and self.dev_mode == False:
                    self.dev_mode = True        
                if event.key == pygame.K_1 and self.dev_mode == True:
                    self.dev_mode = False  
                if event.key == pygame.K_r:
                    self.game_state_reset()
                if event.key == pygame.K_p:
                    self.game_state_pause()
                    
                    
        #this would be used if i want to detect this per frame but i only need to detect it once hence event type.
        #Get status of keys
        #self.keys = pygame.key.get_pressed()

        #movement handling
        #if self.keys[pygame.K_SPACE]:
        #    self.velocity.y = -3

############################################ Input Handler Block End ##############################################################





############################################ Simulation Block Start ###############################################################
    
    def pipe_generation(self): ############################################ Simulation Block Start ###############################

        VALID_PIPES_ORIENTATIONS = [[5,2],[6,1],[4,3]]
        PIPE_GEN_END = -self.width * 4/16
        PIPE_GEN_START = -self.width*1/16
        PIPE_SEP = 5

        # Initialize Pipes
        if self.pipes_config[0] == []:
            
            for i in range(0,5):
                
                gnd_y = 0
                sky_y = 0

                # Decides random initializing orientation of pipes
                RND_PIPE = random.randint(1,3)
                if RND_PIPE == 1:
                    gnd_y = VALID_PIPES_ORIENTATIONS[0][0]
                    sky_y = VALID_PIPES_ORIENTATIONS[0][1]
                if RND_PIPE == 2:
                    gnd_y = VALID_PIPES_ORIENTATIONS[1][0]
                    sky_y = VALID_PIPES_ORIENTATIONS[1][1]
                if RND_PIPE == 3:
                    gnd_y = VALID_PIPES_ORIENTATIONS[2][0]
                    sky_y = VALID_PIPES_ORIENTATIONS[2][1]
                
                self.pipe_x_speed = PIPE_GEN_START
                CMN_PIPE_X = self.width - self.pipe_x_speed + (self.width * (PIPE_SEP * i)/20 )
                
                PIPE_GND_Y = (self.height * gnd_y )/10 
                PIPE_SKY_Y = (self.height * 0 ) / 10 - (self.height * sky_y )/10
                
                # [ gnd x, gnd y, sky x, sky y]

                self.pipes_config[i].append(CMN_PIPE_X)
                self.pipes_config[i].append(PIPE_GND_Y)
                self.pipes_config[i].append(CMN_PIPE_X)
                self.pipes_config[i].append(PIPE_SKY_Y)
                self.pipes_config[i].append(True)
                if i == 0:
                    self.pipes_config[i].append(True)
                else:
                    self.pipes_config[i].append(False)
        
        # Update and reuse pipes
        for i in range(0,5):
        
            self.pipes_config[i][0] -= self.pipe_x_speed 
            self.pipes_config[i][2] -= self.pipe_x_speed 
            if int(self.pipes_config[i][0]) <= PIPE_GEN_END:
                gnd_y = 0
                sky_y = 0

                # Randomization of pipes
                RND_PIPE = random.randint(1,3)
                if RND_PIPE == 1:
                    gnd_y = VALID_PIPES_ORIENTATIONS[0][0]
                    sky_y = VALID_PIPES_ORIENTATIONS[0][1]
                if RND_PIPE == 2:
                    gnd_y = VALID_PIPES_ORIENTATIONS[1][0]
                    sky_y = VALID_PIPES_ORIENTATIONS[1][1]
                if RND_PIPE == 3:
                    gnd_y = VALID_PIPES_ORIENTATIONS[2][0]
                    sky_y = VALID_PIPES_ORIENTATIONS[2][1]
                self.pipes_config[i][0] = self.width
                self.pipes_config[i][2] = self.width  
                self.pipes_config[i][1] = (self.height * gnd_y )/10 
                self.pipes_config[i][3] = (self.height * 0 ) / 10 - (self.height * sky_y )/10  
                self.pipes_config[i][4] = True # score
                



    def Collision(self): #################### Collison Based Logic ###########################
        
        PLAYER_X_POS = (self.width*5)/16

        player_rect = pygame.Rect(PLAYER_X_POS,
                                  self.pos_y,
                                  self.Bird_vel_bwn_img.get_size()[0],
                                  self.Bird_vel_bwn_img.get_size()[1])

       
        for pipe_num in range(0,5):
            
            pipe_gnd = pygame.Rect(self.pipes_config[pipe_num][0],self.pipes_config[pipe_num][1],*self.Pipe_rev_img.get_size())
            pipe_sky = pygame.Rect(self.pipes_config[pipe_num][2],self.pipes_config[pipe_num][3],*self.Pipe_rev_img.get_size())
            


            if player_rect.colliderect(pipe_gnd) or player_rect.colliderect(pipe_sky):
                # self.game_state_reset() for human player
                self.game_over_flag = True
                
                
                
         # Collision detection of ground
        if (self.pos_y +self.Bird_vel_bwn_img.get_rect()[3]) > (self.height * 7)/10:
                #self.game_state_reset()
                self.game_over_flag = True # This flag is for the Ai to setup an understand the its time to reset the game and call upon reset func in the in the flappy env class
                return

        # Collision detection of sky
        if (self.pos_y ) < 0:
                #self.game_state_reset()
                self.game_over_flag = True
                return

    def score_counter(self): #################### Counter Based Logic ###########################
        
        if self.pipes_config[0] == []:
            return
        
        PLAYER_X_POS = (self.width*5)/16

        player_rect = pygame.Rect(PLAYER_X_POS,
                                  self.pos_y,
                                  self.Bird_vel_bwn_img.get_size()[0],
                                  self.Bird_vel_bwn_img.get_size()[1])

        for pipe_num in range(0,5):
            
            green_score_rect = pygame.Rect(self.pipes_config[pipe_num][2],
                                           self.pipes_config[pipe_num][3]+self.Pipe_img.get_size()[1],
                                           self.Pipe_img.get_size()[0],
                                           self.Pipe_img.get_size()[1]*3/4)    
            
            if self.pipes_config[pipe_num][4] == True and player_rect.colliderect(green_score_rect):
                self.score_count += 1        
                self.pipes_config[pipe_num][4] = False
                
                # Basically on collison we set the next pipe as true for marking the nearest

                if pipe_num == 4: 
                    self.pipes_config[pipe_num][5] = False # nearest
                    self.pipes_config[0][5] = True
                if pipe_num < 4:
                    self.pipes_config[pipe_num][5] = False # nearest
                    self.pipes_config[pipe_num+1][5] = True
            

    def update(self): #################### Simulation Loop ###########################

        # Constants
        GROUND_SPD = 140
        GRAVITY = 1000 # based px/sec
        MAX_VELOCITY = 500
        BIRD_DEGREE = 20 #45 is too much, 30 looks weird =<25 is best
        PIPE_SPD = 200
        
        # Current delta time calculation and last_time updation
        
        # self.dt = 0.016 # use this when training
        self.dt = self.clock.tick(self.fps)/1000  # [this is for when we want to wait for a frame.] [right now we are using 0.016 value as to replicate 60fps per second to constantly run it at that speed as fast as we can to quickly go through the training as compared to waiting for the cpu to wait for the frame to render.] 
        
        
        # Bird Rotation Calculation
        PRCNT_VAL = (self.velocity.y / MAX_VELOCITY)
        
        self.bird_rot_angle = self.gradient_conversion(-BIRD_DEGREE,BIRD_DEGREE,PRCNT_VAL) #BIRD_DEGREE + (PRCNT_VAL) * (- BIRD_DEGREE - (BIRD_DEGREE)) # [new_value = new_min + value * (new_max - new_min)] rotation angle transformtion from velocity to rotation.

        # Velocity Bird
        self.accelation = GRAVITY 
        
        if self.pause == False:
            self.velocity.y += self.accelation * self.dt # Velocity is px/frame in short
        
        if self.velocity.y > MAX_VELOCITY:
            self.velocity.y = MAX_VELOCITY
        
        if self.pause == False: 
            self.pos_y += self.velocity.y * self.dt # Updating Y positon

        # Pipe Speed and Generation
        if self.pause == False:
            self.pipe_x_speed = PIPE_SPD * self.dt

            self.pipe_generation()

        self.Collision()
        self.score_counter()

        # Ground - Simple 2D scrolling by using 2 images and upating their values based on if it touches the end or not.
        if self.pause == False:
            self.gnd_x += GROUND_SPD * self.dt
        if self.gnd_x >= self.width:
            self.gnd_x = 0 
        
        #debug shi
        #print(f"bird_y:{int(self.pos_y)} | int(velocity:{int(self.velocity.y)}) | dt: {int(self.dt)} | pipe_speed_x {int(self.pipe_x_speed)} | {int(-self.width * 4/16 )} | {self.pipes_config[0][0]}")
        


############################################ Simulation Block End ###############################################################





############################################ Gym Env Block End ###############################################################

    def game_observation_state(self): 

        """Returns a list of pipe distance, pipe size, bird distance and current velocity."""

        PLAYABLE_SPACE = self.height * 7 / 10
        MAX_VAL = -400
        MIN_VAL = 500
        CALC_VLCTY_VAL = self.velocity.y / (MIN_VAL - MAX_VAL)
        # Reinforcement Observation Space

        # All normalized values 
        self.pipe_distance =  self.pipe_observation()[1] 
        self.pipe_size = self.pipe_observation()[0] 
        self.bird_dist = self.pos_y / PLAYABLE_SPACE
        self.vel_current = self.gradient_conversion( 1 , 0 , CALC_VLCTY_VAL )
        
        observation_space = [ self.pipe_distance , self.pipe_size , self.bird_dist , self.vel_current ] # type: ignore

        return numpy.array(observation_space, dtype= numpy.float32) 
    
    def pipe_observation(self): 

        nearest = 1
        pipe_size = 0

        """Returns a gradient of 0 - 1 in a list for pipe distance [0] and pipe size [1]."""

        ## For pipe size
        # 0.1 small 
        # 0.2 medium
        # 0.3 large

        ## For pipe gap its a simple 0 to 1 gradient based on which pipe is currently marked as active

        DEAD_ZONE_GND = self.height * 7/10 

        for pipe_num in range(0,5):
            if self.pipes_config[pipe_num][5] == True:
                nearest = ( self.pipes_config[pipe_num][0] - ( self.width * 5 ) / 16 ) / self.width * 4
                pipe_size = ( self.pipes_config[pipe_num][1] - DEAD_ZONE_GND ) / self.height 

        if nearest > 1:
            nearest = 1
        
        result = [nearest,pipe_size * -2]

        return numpy.array( result , dtype = float )
    
############################################ Gym Env Block End ###############################################################




############################################ Tool ###############################################################

    @staticmethod
    def gradient_conversion( new_max: float , new_min: float , value: float ): # Does what it says yo
        new_value = new_min + value * (new_max - new_min)
        return new_value
    



############################################ Tool ###############################################################




############### Game Loop States ################     

    def run(self): #################### Game Loop ###########################
        
        while self.game_running:
            
            self.update()
            self.render()
            self.handle() 

    def game_state_reset(self):        

        #bird rotation default angle
        self.bird_rot_angle = 0

        # Dev mode bool
        self.dev_mode = True

        # Velocity and Accelation initilization
        self.velocity = vector(0,0)
        self.accelation = vector(0,0)

        # Delta time initialization to 0
        self.dt = 0

        self.pos_y= (self.background_img.get_rect()[3]-self.ground_img.get_rect()[3])/2 #(480 - (480*7)/10)/2
        self.gnd_x = 0 # ground x pos initialization
        self.pipe_x_speed = 0
        self.pipes_config = [[],[],[],[],[]] # type: ignore

        # reset the score count to 0
        self.score_count = 0

        # Reinforcement learning state variables
        self.game_over_flag = False

        self.pipe_generation()
        

    def game_state_quit(self):
        #pygame.quit
        #sys.exit()
        self.k = 0

    def game_state_pause(self):
        if self.pause == False:
            self.pause = True
            return
        if self.pause == True:
            self.pause = False
            return 
        print(f"{self.pause}")   
        

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