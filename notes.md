overall scope for now: 2d runner where you dodge shit. Perhaps integrating building entrance and exit physics both with front and band and left to right logic. 
Biggest note
When you render shit to the screen, it has to be in the order you want it in the z axis. For example, if I want to create a building that we can enter during side scrolling, and it is a bridge with rails, or a hallway with windows, I want to be able to render that building/transparent rectangle in front of the character and in order to keep the character/player underneath it, the player needs to be rendered first. Same goes for background/foreground objects such as trees


need to create new structures that generate in the background such as more trees, walls and more
likely want to integrate day and night. 
Need to work on the ground so that it moves while the player is running. I'll have to look into those techniques or create my own
Need to create a pause menu. Perhaps further options in the game for video, sound and multiplayer settings? emphasis on multiplayer. 
create a way to weave around trees, perhaps changing the rendering mid gameplay for the player to interact with minimum 3 layers depth: back, middle, front. Perhaps have to shrink/grow the rectangle/character model to simulate moving in 3d space. It would only have to be minor for the illusion to work. 
Perhaps try to use the rectangle object in pygame to shrink the player rectangle for this.

Update Version Alpha 0.0.0.0.6

What have I completed so far?

Ground moves while player running: check
Structures: not started
day and night: not started
pause menu: check
3d mapping: not started


debugging tips

debug inside every frame if necessary. Meaning whenever you're running an animation or checking a position, print the output of the conditional "if"
debug when any math changes. You will be left with horrible cockroaches of responsibility if you don't debug everything as you go. you will be fucked if you just implement
and don't test ur shit. I don't think I could even get **this** far if I didn't constantly debug. Perfect everything. There are some things I have not yet been able to 
crack such as the loading times on changing audio settings within the title. Fortunately those are left to menus.

---------------------

I wonder if it would take as long to modify audio settings with keys while playing the game actively. Probably wouldn't help. At least it's a minor annoyance in the menus and not in the game....

----------------------

There're a few of those. Yes I just used that contraction - bite me. There is a strange bug I haven't begun to troubleshoot where when you change keys too fast, the player animation stops blitting. It could be a problem with the way pygame handles input. Although, it seems to bypass my logic of the player's motion activating the animations. Not the keys, the motion. "Motion" more like it. There's no motion at all. It's like those cutout animations I made as a kid. This ups the cool ante by 10 though.

----------------------

I'm trying to think of other bugs, but most of the "bugs" have been my own fault so far. Easily fixable after hours of being stumped. I'm sure I will laugh at this later. I know I did with my first store database and interface. So much pain. I have to upgrade it. PHP 8 won't be around forever, and security is a concern, even for a local band.

-----------------------


Okay the biggest issue with the code so far is that it's fucking broken, but not completely because undo is a lifesaver. I knew I should have done an incremental commit at the point of adding the entity class and implementing the item and the inventory tests. I will do that now thanks to undo and the thankfully minor modification I had stupidly made to the debug class to fake it the y being inverted. 

Now we come the the crux of the issue. Inverting the Y axis will be essential for me to make this game a platformer. Or at least be able to do it with some ease. I'm not sure if this is game breaking yet, regardless of what I want to do. 

I think in the meantime I'm going to put that project on hiatus for now. 

To follow on, I would like to continue implementing the inventory system and item mechanics and working toward a combat system.
