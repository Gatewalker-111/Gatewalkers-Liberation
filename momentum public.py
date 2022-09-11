import json
import math
import os 
import discord
Intents = discord.Intents(messages=True, guilds=True,message_content=True,)
client = discord.Client(intents=Intents)
white_list = ['539596142002962442', '245387424748929024', '137267493776392194' , '246015579880685568', '498682085951930388' ,'183007580824666112', '244201502967595010','260254296795381760','258189519956738048']
#base discord setup stuff. Whitelist == all the mods and sierra's discord ID things, to govern who can edit the bot's memory and wipe it.



@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))
#tells me the bot loads.
global shipnumber_creation
global shipnames 
global up_down
global left_up_right_down
global right_up_left_down
global faction  
global s
global r
global q
global x
global y
global maxa 
global destroyed
global update_message 
global last_command


shipnumber_creation = -1
shipnumber_indentification = -1
#shipnumber_creation == used to put each ships information in the correct array position during creation.
#shipnumber_indentification == used to indentify which ship the command == calling on.
#Use Indentification for everything but adding new ships
shipnames = []
up_down = []
left_up_right_down = []
right_up_left_down = []
faction = []
s = []
r = []
q = []
x = []
y  = []
maxa = []
destroyed = []
#Each of these stores a ships information in the same row. So if the ship Phoenix == in 1, its data are all stored in spot one of the every array.
# S,R, and Q are the coordinates of the ship tshis program handles. X and Y are the human-readable part, and are NOT GENERATAED LIVE.
#Destroyed asks if the ship has been destroyedor rendered inoperable. 0 == no, 1 == yes.

update_message = 'Acceleration applied, momentum ==: '
messagecontent = 'placeholder'
csv_string =''
#update_message == where I construct the messages to be put in discord, messagecontent == just the content of the message its looking at,
# because ToLowerCase doesn't work with message.content
#csv_string houses the string of commands that are passed to dark
arrow_array_list = ['⇑', '⇗', '⇘', '⇓', '⇙', '⇖']

last_command = 0
#Tells me how I should update the CSV file for Dark

def Easter_Egg_Manager ():
  egg_name = ['chocolate chip cookie', 'sugar cookie', 'snickerdoodle']
  egg_lines = ['Chocolate Chip Cookies? Admiral Epsilone would like to know your location.',
  'Olea would like to speak to you at your earliest conviencence', '*Kliflosial hyper-speeds next to you and steals the snickerdoodles.* "Too slow!"']
  egg_found = 0
  egg_number = 0
  while(egg_found == 0 and egg_number < (len.egg_name + 1)) :
    if(egg_name[egg_number] in messagecontent) :
      egg_found = 1
      print('easter egg found!')
    
    else :
      egg_number = egg_number + 1
      print('still searching')
    
    if(egg_found == 1) :
      update_message = egg_lines[egg_number]
    
    else :
      update_message = ('The ' + messagecontent[9:(messagecontent.find(':') - 2)] + ' has joined the fleet!')
    
  

#This just handles any easter eggs I threw in. Also, if you are reading this Jimbo,
#giving some more in-character quotes would be nice, cause I wrote these before the Campaign Test and have not remade them.

def Use_relevant_momentum (relevant_momentum,relevant_arrow_1,relevant_arrow_2):
  global update_message
  print('use relevant momentum has activated')
  if(int(relevant_momentum[shipnumber_indentification]) > 0) :
    update_message = update_message + ' ' + relevant_arrow_1 + str(relevant_momentum[shipnumber_indentification])

  if((relevant_momentum[shipnumber_indentification]) < 0) :
    update_message = update_message + " " + relevant_arrow_2 + + abs(int(relevant_momentum[shipnumber_indentification]))

  #The above part runs through every direction, and if its > 0 it adds it to the message.

#Constructs a discord message with all the non-zero and non-negative velocities.

def Extract_relevant_momentum():
  global update_message
  applied_speed = 0
  if('⇑' in messagecontent):
    applied_speed +=  int((messagecontent[messagecontent.find('⇑'): messagecontent.find('⇑') + 3])[1])

  if('⇓' in messagecontent):
    applied_speed +=  int((messagecontent[messagecontent.find('⇓'): messagecontent.find('⇓') + 3])[1])

  if('⇗' in messagecontent):
    applied_speed +=  int((messagecontent[messagecontent.find('⇗'): messagecontent.find('⇗') + 3])[1])

  if('⇘' in messagecontent):
    applied_speed +=  int((messagecontent[messagecontent.find('⇘'): messagecontent.find('⇘') + 3])[1])

  if('⇙' in messagecontent):
    applied_speed +=  int((messagecontent[messagecontent.find('⇙'): messagecontent.find('⇘') + 3])[1])

  if('⇖' in messagecontent):
    applied_speed +=  int((messagecontent[messagecontent.find('⇖'): messagecontent.find('⇖') + 3])[1])

  #This adds up all the ordered acceleration and checks if its over the max acceleration of the ship
  print(applied_speed)
  if(int(applied_speed) > int(maxa[shipnumber_indentification])) :
    update_message = 'Error: Too much acceleration applied, engine strain outside of acceptable parameters.'
  
  else :
    Update_Backups()
    print('max a check has suceeded')
    if '⇑' in messagecontent:
      print(up_down)
      print((up_down[shipnumber_indentification]))
      (up_down[shipnumber_indentification]) = int(up_down[shipnumber_indentification]) + int((messagecontent[messagecontent.find('⇑'):messagecontent.find('⇑') + 3])[1])
      print((up_down[shipnumber_indentification]))

    if '⇓' in messagecontent:
      up_down[shipnumber_indentification] = int(up_down[shipnumber_indentification]) - int(((messagecontent[messagecontent.find('⇓'):
         messagecontent.find('⇓') + 3]))[1])
      print((messagecontent[messagecontent.find('⇓'):
        messagecontent.find('⇓') + 3])[1])

    if '⇖' in messagecontent:
      left_up_right_down[shipnumber_indentification] = int(left_up_right_down[shipnumber_indentification]) + int(((messagecontent[messagecontent.find('⇖'):
        messagecontent.find('⇖') + 3])[1]))

    if '⇘' in messagecontent:
      left_up_right_down[shipnumber_indentification] = int(left_up_right_down[shipnumber_indentification]) - int(((messagecontent[messagecontent.find('⇘'):
        messagecontent.find('⇘') + 3])[1]))

    if '⇗' in messagecontent:
      right_up_left_down[shipnumber_indentification] = int(right_up_left_down[shipnumber_indentification]) + int(((messagecontent[messagecontent.find('⇗'):
        messagecontent.find('⇗') + 3])[1]))

    if '⇙' in messagecontent:
      right_up_left_down[shipnumber_indentification] = int(right_up_left_down[shipnumber_indentification]) - int(((messagecontent[messagecontent.find('⇙'):
        messagecontent.find('⇙') + 3])[1]))

#and this part adds all the momentums into the correct areas.
  

#This looks at the acceleration order and uses string and index to extract momentum.
#The way the string mess works == that the first string looks through the entire message for where the arrow ==, then takes that and the next 2 characters.
#That == then run through a string that takes the numbers and ignores the arrow.

def Update_Position():
  q[shipnumber_indentification] = int(q[shipnumber_indentification]) + int(right_up_left_down[shipnumber_indentification]) - int(left_up_right_down[shipnumber_indentification])
  print('Q is ' + str(q[shipnumber_indentification]))
  s[shipnumber_indentification] = int(s[shipnumber_indentification]) + int(up_down[shipnumber_indentification]) + int(left_up_right_down[shipnumber_indentification])
  r[shipnumber_indentification] = int(r[shipnumber_indentification]) + int(up_down[shipnumber_indentification]) + int(right_up_left_down[shipnumber_indentification])

#This updates a ship position in qrs based on an accel order.

def extract_starting_position (mode_number):
  print(messagecontent)
  x.insert(mode_number, int(messagecontent[messagecontent.find('(') + 1: messagecontent.find(',')]))
  y.insert(mode_number, int(messagecontent[messagecontent.find(',') + 1: messagecontent.find(')')]))
  q.insert(mode_number, x[mode_number])
  s.insert(mode_number, y[mode_number] - math.floor((x[mode_number])/2))
  r.insert(mode_number, s[mode_number] + q[mode_number])
  #print('Q:' + q[mode_number] + ' R:' + r[mode_number] + ' S:' + s[mode_number])

#This takes the xy coord input and turns it into qrs.

#def UpdateBackups ():
#  TestJSON = JSON.stringify([shipnames,left_up_right_down,up_down,right_up_left_down,q,r,s,maxa,destroyed,faction]);
#This updates the JSON that Dark Map pulls from, as well as the backup JSON for the undo command.


def Find_Called_Ship ():
  global shipnumber_indentification
  shipfound = 0
  shipnumber_indentification = 0
  while(shipfound == 0 and shipnumber_indentification < (len(shipnames))):
    if messagecontent.find(shipnames[shipnumber_indentification]) > -1 :
      shipfound = 1
      print('ship found! Ship is ' + shipnames[shipnumber_indentification])
    
    else :
      shipnumber_indentification +1
      print('still searching for ship')
    
  

def Update_Backups ():
  backup_string = [shipnames,left_up_right_down,up_down,right_up_left_down,q,r,s,maxa,destroyed,faction]
  with open('GatewalkerBackupStats.JSON', 'w') as json_file:
    json.dump(backup_string, json_file)

#This searches through a given message to find what ship the message == refering to.

@client.event
async def on_message(message):
  global shipnumber_creation
  global shipnames 
  global up_down
  global left_up_right_down
  global right_up_left_down
  global faction  
  global s
  global r
  global q
  global x
  global y
  global maxa 
  global destroyed
  global update_message 

  if message.author == client.user:
    return
  global messagecontent
  messagecontent = (message.content).lower()
  print('message content is' + message.content)
  print('test')
  await message.channel.send('Message recieved')
 

#######################
######/Action Commands#########
#######################

  if 'add ship' in messagecontent:
   Update_Backups()
   global shipnumber_creation
   global shipnames 
   global up_down
   global left_up_right_down
   global right_up_left_down
   global faction  
   global s
   global r
   global q
   global x
   global y
   global maxa 
   global destroyed
   global update_message 
   global last_command

   last_command = 1
   print('ship added')
   shipnumber_creation = shipnumber_creation + 1
   shipnames.insert(shipnumber_creation,messagecontent[9:(messagecontent.find(':') - 2)])
   up_down.insert(shipnumber_creation, 0)
   left_up_right_down.insert(shipnumber_creation, 0)
   right_up_left_down.insert(shipnumber_creation, 0)
   destroyed.insert(shipnumber_creation, 0)
   extract_starting_position(shipnumber_creation)
   print(shipnumber_creation)
   maxa.insert(shipnumber_creation, int(messagecontent[messagecontent.find(':') + 1 :][(messagecontent[messagecontent.find(':') + 1 :]).find(':') + 1: (messagecontent[messagecontent.find(':') + 1 :]).find(':') + 3]))
   print('Maxa is ' + str(maxa[shipnumber_creation]))
   faction.insert(shipnumber_creation,(messagecontent[messagecontent.rfind(':') + 1 : messagecontent.rfind(':') + 2]))
   #Easter_Egg_Manager()
   update_message = 'The ' + shipnames[shipnumber_creation] + ' has joined the fleet!'
   await message.channel.send(update_message)
     #This == the add ship command. It replaces all the data in that row with baseline, then checks if an easter egg == applicable, sends the message, and updates the CSV and the bot.
  

  if 'acceleration order' in messagecontent:
    global shipnumber_indentification
    print('acceleration order has been passed')
    update_message = 'Acceleration applied, momentum is '
    Find_Called_Ship()
    if destroyed[shipnumber_indentification] == 0:
      print('destroyed check has been passed')
      Extract_relevant_momentum()
      print('Extract Momentum has ended')
      if update_message != 'Error: Too much acceleration applied, engine strain outside of acceptable parameters.':
        Use_relevant_momentum(up_down,'⇑','⇓')
        Use_relevant_momentum(left_up_right_down,'⇖','⇘')
        Use_relevant_momentum(right_up_left_down,'⇗','⇙')
        print('Update position has been reached')
        if messagecontent != 'second': Update_Position()
        if(update_message == "Acceleration applied, momentum is ") : update_message = 'Acceleration applied, ship is stationary.'

  
    else: update_message = 'Error: ship is inoperable.'
    await message.channel.send(update_message)
    #This first finds the called ship, runs extrat momentum, and if it hasn not exceeded
  

  if 'destroy' in messagecontent :
    Update_Backups()
    Find_Called_Ship()
    destroyed[shipnumber_indentification] = 1
    print(destroyed[shipnumber_indentification])
    update_message = shipnames[shipnumber_indentification] + ' has been destroyed. Prepare for a long meeting with Epsilone.'
    await message.channel.send(update_message)

#Just destroys the ship listed. Pretty simple.

#######################
######/QOL Commands##########/
#######################
  if 'query momentum' in messagecontent :
    Find_Called_Ship()
    update_message = 'Momentum of ' + shipnames[shipnumber_indentification] + ' is '
    Use_relevant_momentum(up_down,'⇑','⇓')
    Use_relevant_momentum(left_up_right_down,'⇖','⇘')
    Use_relevant_momentum(right_up_left_down,'⇗','⇙')
    if update_message == 'Momentum of ' + shipnames[shipnumber_indentification] + ' is ' :
      update_message = 'The ' + shipnames[shipnumber_indentification] + ' is stationary.'   
    await message.channel.send(update_message)
  
  if 'query position' in messagecontent :
    Find_Called_Ship()
    update_message = 'Position of ' + shipnames[shipnumber_indentification] + ' is '
    x[shipnumber_indentification] = q[shipnumber_indentification]
    print('S is ' + str(s[shipnumber_indentification]))
    print('Q is ' + str(q[shipnumber_indentification]))
    print('Half of Q is ' + str(math.floor(q[shipnumber_indentification]/2)))
    y[shipnumber_indentification] = (s[shipnumber_indentification]) + (math.floor(+q[shipnumber_indentification]/2))
    print ('query position: X is '+ str(x[shipnumber_indentification]) + ', y is ' + str(y[shipnumber_indentification]))
    update_message = update_message + 'x:'+ str(x[shipnumber_indentification]) + ' y:' + str(y[shipnumber_indentification])
    await message.channel.send(update_message)
  

  if 'query ships' in messagecontent :
    update_message = 'The ships are: ' + str([shipnames])
    await message.channel.send(update_message)

  if 'command list' == messagecontent :
    update_message = 'Add ship: adds ship to combat engagement. \n Format: "add ship [shipname] P:([starting x],[starting y]) A:[maximum acceleration]". \n';
    update_message = update_message + '\n Acceleration Order: applies stated acceleration to called ship. \n format: acceleration order: [ship name] [arrow followed by number without space] [repeat for all called directions] \n';
    update_message = update_message + '\n Destroy: destroys target ship. \nformat: destroy [shipname] \n';
    update_message = update_message + '\n Query momentum: gives the momentum of the called ship. \n format: Query momentum [shipname] \n';
    update_message = update_message + '\n Query position: gives the position of the called ship in xy coords. \n format: Query position [shipname]\n';
    update_message = update_message + '\n Query ships: lists the ships.\n format: Query ships \n';
    update_message = update_message + '\n command list: lists all commands. \n format:command list \n';
    update_message = update_message + '\n wipe bot memory: resets bot. Note: only jimbo, the mods, and sierra can use this command. \n format: wipe bot memory \n';
    update_message = update_message + '\n undo last command: undos the last command. Can undo wipe bot memory, should work through a hard reset of bot (though you will loose the final command.) \n Format: undo last command \n';
    update_message = update_message + '\n Note: all commands are not case sensitive.';
    await message.channel.send(update_message)
  

            #########################
            ##########/CONSOLE COMMANDS######/
            #########################


  if messagecontent == 'undo last command' and str(message.author.id) in white_list :
    await message.channel.send('Undoing last command.')
    backup_string = 'placeholder'
    with open('GatewalkerBackupStats.JSON', 'r') as GateFile:
      backup_string = json.load(GateFile)
    print('Undo Last Command Has Fired')
    print(backup_string)
    print('Update == happening')
    shipnames = backup_string[0]
    left_up_right_down = backup_string[1]
    up_down = backup_string[2]
    right_up_left_down = backup_string[3]
    q = backup_string[4]
    r = backup_string[5]
    s = backup_string[6]
    maxa = backup_string[7]
    destroyed = backup_string[8]
    faction = backup_string[9]
    if(last_command == 1): shipnumber_creation = shipnumber_creation - 1
    Update_Backups()
  
#This takes the backup files and replaces the existing data from them. Works through any command, including wipe bot memory.

  
#This just takes in the icon, its probably better to just manually write it into the backup csv file and then use Undo Last Command to force it in.

  if messagecontent == 'wipe bot memory' and str(message.author.id) in white_list:
     Update_Backups()
     await message.channel.send('wiping memory')
     shipnames = []
     up_down = []
     left_up_right_down = []
     right_up_left_down = []
     faction = []
     s = []
     r = []
     q = []
     x = []
     y  = []
     maxa = []
     destroyed = []
     shipnumber_creation = -1
     shipnumber_indentification = -1
     last_command = 0
  
  #This wipes the bot memory, except for the backup files.


client.run('')
