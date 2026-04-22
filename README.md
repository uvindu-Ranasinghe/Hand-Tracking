# Hand-Tracking-Practice-
log 10.04/2026 

Log 1
Im trying to have acurate volume controls and volume disaply. 

Problem 1 : The reason why im doing this is that I noticed that my displayed values did not match 
the values I see on the windows volume bar. 

Reason : I was using raw dB values - the windows UI is logrythmic so my linear float calc did not work.

Solution : calculated the rawVol as a float then used simple 0 to 1 values to mimic the presentage by converting the rawValues. 

Problem 2 : I was using previous frames volume for my calculations so it didnt match with the displayed current frame. 

Reason : Modulo use was a bad idea as it had many bugs, it would make my volume jump crazily. 

Solution : My main purpose was to create a volume snapping effect, I changed the sequence of events. I started with rawVolume % calculation 
-> converted that to a snap volume % while rounding the values. 

Also to test out Im going to snap it in increments of 5 but in the future im gonna do it by 2 because thats how my windows UI does it. 

commit was called "Clean Code : "Clean Code : gotten ride of all the unecessary comments from practice, then rewrote the calculations for the volume converstoins while trying to match the volume to my windows UI and realistic settings"

Log 2

I'm going to try to clean up the code now, I will get rid of any dead code and try to
find a way to make sure it looks easy to read with good comments. 
-I need to find out if the naming system I learned in 281 still applies to python or not. 

Log 3 

I finally manged to get the code to clearly work. The UI matches the volume changes. 

Log 4 
Delted the unecessary hand number count project. I will be pivoting my approach of this project to make windows OS more accesible for individuals. 
This means that I will be creating a way to use the windows OS without using a keyboard or mouse. 
I also focused on making the hanTrackingModule clean. This means I got rid of unecesary codes and comments. I also flipped the camera allowing me
to get a mirrored representation of myself. This will allow me to properly identify left and right. 
I have also implimented this in the handTrackingVolume project. 

commit was called : Clean Code : Cleaned up the handTrackingModules code(refer to log), added a mirroring effect to my camera captures allowing me to have a mirroed look of my self throughout the project

Log 5

I am creating a new module called handGestureControl which will detect the fingers and recognize certian gestures. Depending on the gestures it will allow me to change different functions. Eg: scroll if my hand is pointing up or change volume if im pinching. 
These changes are still to be determined. (more info will be added in later logs)

Log 6

I am going to try to merge clean-code with main on git. 

Log 7 - created a new feature for the HandGestureControl module and created a new branch on git. 

Log 8 

Creating the logic to see if the hand is opened or closed. I will be using the x of the thumb as the thumb moves in the x direction 
and y coordinates of rest of the fingers as they move horizontally. ____Limitation____ : this is making an assumption that hands will 
be horizontally placed. Also added handType based detection to see if the thumb is open or closed. This will look 
at thumb movement in the x-axis (horizontally) 

