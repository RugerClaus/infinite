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

------------------------

An interesting mechanic would be to add some items that break depending on how high they were dropped from and others not breaking. Perhaps later some that could damage the ground. I'm getting ahead of myself here, but I'll see about giving this a try at some point. I'll need to integrate physics for falling objects at some point. Preferrably earlier in this cycle so that I can fix any game fucking bugs. That would really really ruin me. I get 3 months into this and BOOM I need to change the base layers of the game. I want to avoid that as much as I can. I worry I won't be able to get around to fixing the Y mechanics in time to make the game like that. Perhaps that could be for the better, but I'll give it a few more tries.

Combat mechanics, ragdoll physics, and project scarring mechanics aside - in this update, I'd like to finish the visual interaction and useability of the inventory system. At least implementing a hotbar.

-------------------------
 I may want to make this a space themed game. I have left the mechanics and the image names open enough to do so. It's just so hard to get art, and I am a musician not a visual artist, so one half of this game's effect is taken care of (audio), but the visual things are going to have to be done in MS paint. That's fine. I could use some experience with this.

 Sprites are a ton easier than physical drawing, but still take talent to make good. Which ultimately means mine will be shit. Thank you, sir whoever created these assets.

 I think the next thing to go will be these assets. I'll try to spend some time creating new sprites for the player and environments. 

 The update I've just finished is massive. And every single little feature has been a massive hurdle, but it's been fun for sure, and the fact the game is working as well as it is right now as of alpha 0.0.0.1.6 is very satisfying.

 I know I'll need to automate the spawning mechanics for the food. I think I'll have specific locations they're hidden and tie that to a level object. I feel like every time I feel I'm getting in the weeds, I realize around every corner I ain't seen shit yet.

 On another note, game.py is going to be the next major overhaul and that's going to fucking break everything if I'm not careful. I have been trying not to do much with it in the last few updates, and I feel I've been successful. 