REINFORCEMENT LEARNING IN FLAPPY BIRD :

About the project:

This project is basically learning how reinforcement learning can be applied to simple games like flappy bird.
Since the entire project is made previously with pygame, I took a simpler approach of using value-based reinforcement 
learning instead of using the more resource consuming vision based RL.

Libraries to install:

    -All Libraries availible in Requirements.txt 
    -Non Cuda devices install torch via website

    [pip freeze > requirements.txt]
    

    Docs - [https://stable-baselines3.readthedocs.io/en/master/guide/install.html] - also installs gymnasium library used for wrapping the env.
         - [https://www.pygame.org/docs/]

[0.1v]

 - Entire Game engine for The reinforcement learning Flappy bird is made from scratch. 
 - Pygame is just to draw assests on the screen.
 - Currently configured to be played by RL model using gymnasium wrapper but change a few things and run the game.py.

 Things to remember while setting it for training:

1) Under game.update()
    set delta time to A while training and B while Playing. if reversed it would be funny asf. 
    A) self.dt = 0.016 
    B) self.dt = self.clock.tick(self.fps)/1000  

2) To train a custom model.
    - Set model name to properly show your timesteps
    - Use your specific Pytorch Library | [https://pytorch.org/get-started/locally/] Find specific cuda version using nvidia-smi. 
    - Saved model present under models.
    - Incase you are not sure for cuda, set device="auto" under PPO() model details. 

3) To play the game using a RL model.
    - I've already trained 2 models for anyone to try it out. 
        [100K and 1 Million timesteps]
    - Follow above advice for cuda issues.
    - Add model path and run :]

Game engine and assets are made by me and free for anyone else to use.

Reinforcement Flappy @ 2026 | Ugly code written by me
        