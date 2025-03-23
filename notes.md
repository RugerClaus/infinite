overall scope for now: 2d runner where you dodge shit. Perhaps integrating building entrance and exit physics both with front and band and left to right logic. 
Biggest note
When you render shit to the screen, it has to be in the order you want it in the z axis. For example, if I want to create a building that we can enter during side scrolling, and it is a bridge with rails, or a hallway with windows, I want to be able to render that building/transparent rectangle in front of the character and in order to keep the character/player underneath it, the player needs to be rendered first. Same goes for background/foreground objects such as trees


need to create new structures that generate in the background such as more trees, walls and more
likely want to integrate day and night. 
Need to work on the ground so that it moves while the player is running. I'll have to look into those techniques or create my own
Need to create a pause menu. Perhaps further options in the game for video, sound and multiplayer settings? emphasis on multiplayer. 
create a way to weave around trees, perhaps changing the rendering mid gameplay for the player to interact with minimum 3 layers depth: back, middle, front. Perhaps have to shrink/grow the rectangle/character model to simulate moving in 3d space. It would only have to be minor for the illusion to work. 
Perhaps try to use the rectangle object in pygame to shrink the player rectangle for this.

