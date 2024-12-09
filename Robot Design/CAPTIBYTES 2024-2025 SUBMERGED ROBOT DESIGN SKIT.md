**Robot Design Skit**   
**Jacob will have the porter board**  
**Anthony responsible for bin of robots and attachments**

**\[slide 1 AND 2 Eli\]**  
**The welcome/intro slide** 

**Arsh:** LETS GOOOOOOO (said in very British accent)

**\[Slide 2\]**  Eli \- We start our presentation with a timeline of our season which started back in August.  

**\[slide 3 Panchami\]**

**Panchami**: Meet our robots Mary, Gary, Sherry, our new and improved bots which use the Engineering Design Process to design and code our bots to complete as many missions as possible on this year’s FLL Submerged robot game\!  
   
**\[slide 4 Swara\]**

**\[Panchami will be holding one of the bots and pointing to the different motors while Swara speaks\] Swara:** Our robot design uses a spike prime hub and has the most advanced hardware and firmware, featuring 

- 2 medium motors for attachments,   
- 2 medium movement motors,   
- 3 small black wheels for balance.  
- 2 light sensors,  
- An internal gyro  to make runs more reliable,   
- A flat frame makes it easy to align onto the walls of the field.  
- AND it was coded in python 

**Eli (holding his own bot, puts the** **Pythagoras onto the bot):** Due to the robot’s universal interface, attachments can be fit onto the front of   
the robot easily uses bevel gears. Here is an example of the interface.

***Eli fits an attachment on the robot to present the robot’s attachment interface to the judges***

**\[slide 5 Griffin\]**  
**Griffin:**  First A PICK chart was used to identify missions based on point value, and difficulty.  PICK stands for Possible, Implement, Challenge, or Kill.  We used this data to group our missions for team members to work on and to design  attachments.

**\[slide 6 Jacob\]**

**Eli:** A robot path diagram was used to group missions to maximize points and time. \[point to image\]

**Jacob:**. Pseudocode was used to help figure out plans and code for missions. Here are two examples for missions out of the red and blue bases.

**\[slide 7 Arsh\]**

**Arsh:** We used fun names for our attachments, one such being Pythagoras, whichwe voted as our most creative attachment. Before, Mjonlir completed Mission \#3 \- Coral Reef, and Mission \#2 \- Release Shark, and Mission \#1 Coral Nursery. This run was worth 75 pts. Now, we added Mission \#6 \- Raise the Mast  Mission \#5 \- Angler Fish. With these extra points the run is currently worth 125 points.

   
**\[slide 8 Anthony\]**

**Anthony:** The team grouped the missions into color runs. Everyone split up into groups to complete these runs. Here is a list of all our missions \[point to the map\]. Our coded missions add up to 310 points.

**\[slide 9 Anthony\]**

**Anthony:** We improved over the season….at the first rumble our score was 155, at the qualifier we planned for it to be 310\. The increase in value is due to many changes after debriefing from the rumble. 

**Griffin:**  Amazing\! However, nothing can work without learning the software\! Here we have two  of our programmers to discuss more on the topic.

**\[slide 10\]**

**Jacob**: Here is our mission code for the red run which includes coral nursery, shark, coral reef, and raise the mast.. 

**Jacob:** *\*hands code to each of the judges\** \[there should be 3 copies\]

**\[slide 11\]**

**Colin:**   (THESE ARE JUST NOTES, DON‘T ACTUALLY SAY THIS) In the last 2 pages of the code you have, you’ll find our boilerplate. There are different commands such as a simple forward move and a gyro assisted turn. For example, in a gyro turn function, the angle the robot is facing is set to 0 in order for the robot to use its gyro. We also comment on our code so that it’s easier for others to understand and debug.

**Arsh**: Wow, the mission code looks really complex but I really like the idea of a boilerplate to make coding easier for everyone\!

**Colin:** We put our code in a shared google drive so that it is easy to access for everyone on our team, and this makes it easier to edit. 

**\[slide 12\]**

**Colin:** We also upload it to Github to share with others outside our team. There is a link on our website to this code.

**\[slide 13\]**

**Anthony: ** One of our team members created instructions in Bricklink by reverse engineering the existing bot. This made it possible for the newer members to understand the design and its implementation. 

**\[slide 14\]** 

**Eli:** We also track progress with our missions through a spreadsheet.  It keeps track of what is working and changes needed. 

**\[slide 15\]**

**Swara: For coding, not everyone knew how to code in python.** 

- FOR EXAMPLE: Veteran members like Eli and Jacob taught newer members python

- Colin created a boilerplate of reusable code to make coding more efficient

- AND we commented on our code so that others understand and can edit it easily.


\[slide 16\]

**Matthew:** Here are the things we do to share our work out….  
For example:

- We advertise our boilerplate through the QR code you saw earlier  
  - The QR code is posted on our website  
- And we help club students learn to code.


  
**\[Slide 17\]**

**Everyone**: *\*looking at the judges\** ***That’s a wrap —- any questions.*** 

  **— — — — — — — — — — — — — — — — — — — — — — — — — — — —**  
***\*next page is code\****

**from hub import light\_matrix, motion\_sensor, port**  
**import motor\_pair**  
**import motor**  
**import runloop**

**import math**  
**import sys**

**print(sys.version)**

**\# Some constants for calculations**  
**d \= 5.5    \# Diameter of one wheel**  
**r \= 8      \# Radius of turning (using one wheel)**

**\# Takes distance in centimeters (cm), and stop (whether or not to stop moving after the instruction)**  
**async def forward(dist:float,stop:bool\=False,\*\*kwargs):**  
   **'''Move bot forwards by a number of centimeters.**

   **\- \`dist: float:\` The distance in centimeters**  
   **\- \`stop: bool:\` Controls whether or not motors will be issued a stop command at the end of the function.**  
   **\- \`\*\*kwargs: dict\[str, Unknown\]:\` Allows the user to pass acceleration/deceleration arguments optionally.**

   **Examples:**  
   **\`\`\`**  
       **forward(46)      \# Move forwards 46 centimeters**  
       **forward(-23)     \# Move backwards**  
       **forward(11,True) \# Move forwards and stop at the end**  
   **\`\`\`**  
   **'''**  
   **degrees \= dist\*(360.0/(math.pi\*d))**  
    
   **velocity \= kwargs.get("velocity",360)**  
   **if (degrees \< 0):**  
       **velocity \= \-1\*velocity**

   **time \= round((degrees/velocity)\*1000)**  
   **time \= abs(time)**

   **print('FORWARD: degrees:{degrees},time:{time}, velocity:{velocity}'.format(degrees=degrees,time=time,velocity=velocity)) \#Debug**

   **motor\_pair.move(motor\_pair.PAIR\_1,0,velocity=velocity,\*\*kwargs)**  
   **await runloop.sleep\_ms(time)**

   **if (stop \== True):**  
       **motor\_pair.stop(motor\_pair.PAIR\_1)**

**\# Takes angle of turn (theta), wheel (which wheel to turn with), and stop (whether or not to stop moving after the instruction)**  
**async def turn(pivot\_on:str,theta:int,stop:bool\=False,\*\*kwargs):**  
   **'''Turn bot by a number of degrees.**

   **\- \`pivot\_on: str:\` The wheel that the bot will pivot on.**  
   **\- \`theta: int:\` The angle that the bot will turn.**  
   **\- \`stop: bool:\` Controls whether or not motors will be issued a stop command at the end of the function.**  
   **\- \`\*\*kwargs: dict\[str, Unknown\]:\` Allows the user to pass acceleration/deceleration arguments optionally.**

   **Examples:**  
   **\`\`\`**  
       **turn("left",90)   \# Pivot by 90° on the left wheel**  
       **turn("left",-90)  \# Pivot back by 90° on the left wheel**  
       **turn("right",180) \# Pivot by 180° on the right wheel**  
   **\`\`\`**  
   **'''**  
    
   **motion\_sensor.reset\_yaw(0)**  
   **dist \= (2\*math.pi\*r)\*(theta/360.0)**  
   **degrees \= dist\*(360.0/(math.pi\*d))**

   **velocity \= kwargs.get("velocity",360)**  
   **if (degrees \< 0):**  
       **velocity \= \-1\*velocity**

   **print('TURN: wheel:{pivot\_on}, degrees:{degrees}, dist:{dist}, velocity:{velocity}'.format(pivot\_on=pivot\_on,degrees=degrees,dist=dist,velocity=velocity)) \#Debug**

   **if (pivot\_on \== "right"):**  
       **motor.stop(port.F,stop=1)**  
       **motor.run(port.C,velocity,\*\*kwargs)**  
       **if (theta \> 0):**  
           **while (motion\_sensor.tilt\_angles()\[0\] \< theta\*10):**  
               **await runloop.sleep\_ms(1)**  
       **elif (theta \< 0):**  
           **while (motion\_sensor.tilt\_angles()\[0\] \> theta\*10):**  
               **await runloop.sleep\_ms(1)**

   **elif (pivot\_on \== "left"):**  
       **motor.stop(port.C,stop=1)**  
       **motor.run(port.F,velocity,\*\*kwargs)**  
       **if (theta \> 0):**  
           **while (motion\_sensor.tilt\_angles()\[0\] \< theta\*10):**  
               **await runloop.sleep\_ms(1)**  
       **elif (theta \< 0):**  
           **while (motion\_sensor.tilt\_angles()\[0\] \> theta\*10):**  
               **await runloop.sleep\_ms(1)**

   **if (stop \== True):**  
       **motor.stop(port.C)**  
       **motor.stop(port.F)**

   **print('TURN ERROR:', theta\*10, ' ', motion\_sensor.tilt\_angles()\[0\], ' ', (motion\_sensor.tilt\_angles()\[0\]-theta\*10)/10)**  
   **motion\_sensor.reset\_yaw(0)**

**\# Example of what you could do using this code:**  
**async def main():**  
   **print("Hello World\! \-=- Welcome to the SuperSecretCode API")**  
   **motor\_pair.pair(motor\_pair.PAIR\_1,port.C,port.F)**  
   **await turn("left",90)**  
   **await turn("left",\-90)**  
   **await forward(20,True)**  
   **await forward(\-20)**  
   **await turn("right",\-90)**  
   **await turn("right",90,True)**

**runloop.run(main())**

* Why did you use colors to group missions?  
  * Jacob: we used colors to organize and keep track of missions in each group  
* How did you group missions together?  
  * Rishabh: We grouped missions together based on their difficulty and how close they were to each other.   
  * Prishita: Give an example and share how one attachment can help accomplish all missions  
* Who helped code missions?  
  * Panchami: We all helped code missions. Rishabh and Ei were most experienced members of our team and helped everyone learn how to code.   
  * Yuhan: We assigned each team member to each group of missions. Rishabh and Eli went around to help team members solve any issues they encountered.   
* Why did you choose python to code your missions?  
  * Sasha: We chose python because it has more options and flexibility to control the robot.   
  * Prishita: Python helped us create a boilerplate code that was reusable. Once we knew that it worked, we were able to use it to program all our mission runs.  
* What was your most innovative attachment?’  
  * Audrey: Captain Hook because it helped us attempt multiple missions, it incorporated unique parts like lego rubber bands, and there were no motors used in this attachment, and it still helped us score 70 points using this attachment.  
* What is the boilerplate, how does it work/help with coding missions?  
* How did you choose what missions to do, and which not to do?  
* What is a PICK chart?  
* How did your team make sure everyone had an equal amount of work?

