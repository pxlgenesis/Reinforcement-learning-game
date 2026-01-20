import gymnasium as gym
from gymnasium import spaces
import numpy
from game import Game

class FlappyEnv(gym.Env):
    metadata = {'render_modes': ['human']}
    
    def __init__(self):

        # Initialize the parent class which is gym.ENV
        super().__init__() # super(FlappyEnv, self).__init__()

        # Game window size Initialized
        size: tuple[int, int] = (768,480)
        self.game = Game(*size)


        self.action_space = spaces.Discrete(2) # total number of discrete non continous actions [up down not a joystick which is gradient]

        self.observation_space = spaces.Box(    low = 5 , # mathematical limits
                                                high = 5 , # could be using np.inf but this way we control the output better
                                                shape = (4,),       #                                                         
                                                dtype = numpy.float32) # Basically the type of data it is float32 suitable for now 
    
    
    
    def reset( self, seed=None, options=None ): # From the base class for reset
    
        # Reset the game state
        self.game.game_state_reset()

        # Reset wrapper score tracker
        self.last_score = 0

        # Get initilizating Observation data
        obs = self.game.game_observation_state() 

        # These obs will be passes to AI
        return obs , {}
    
    
    
    def render(self):

        # Just calling game class render function
        self.game.render() 
        pass
    
    
    def step( self , action ):
        
        # Basically Ai jumps for us
        if action == 1:
            self.game.velocity.y = -400

        # Run the physics update
        self.game.update()


        # Reward calculation
        reward = 0.1 # for the all the time its been alive
        if self.game.game_over_flag:
            reward = -10 # death penalty

        # Bird state dead or not
        terminated = self.game.game_over_flag
        
        obs = self.game.game_observation_state()

        return obs, reward, terminated, False, {} 
    