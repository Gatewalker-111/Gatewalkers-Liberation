
import json
import math
import os
from turtle import update
import discord
import csv
Intents = discord.Intents(messages=True, guilds=True,message_content=True,)
client = discord.Client(intents=Intents)
white_list = ['539596142002962442', '245387424748929024', '137267493776392194' , '246015579880685568', '498682085951930388' ,'183007580824666112', '244201502967595010','260254296795381760','258189519956738048']
#base discord setup stuff. Whitelist == all the mods and sierra's discord ID things, to govern who can edit the bot's memory and wipe it.



@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))
#tells me the bot loads.
#C:/Users/hyl10/Desktop/Gatewalkers - Liberation/Combat Maps/Map Generation/ShipPos.csv


shipnumber_creation = -1
shipnumber_indentification = -1
#shipnumber_creation == used to put each ships information in the correct array position during creation.
#shipnumber_indentification == used to indentify which ship the command == calling on.
#Use Indentification for everything but adding new ships
shipnames = []
up_down = []
left_up_right_down = []
right_up_left_down = []
secondary_up_down = []
secondary_left_up_right_down = []
secondary_right_up_left_down = []
faction = []
s = []
r = []
q = []
x = []
y  = []
maxa = []
destroyed = []
#Each of these stores a ships information in the same row. So if the ship Phoenix == in 1, its data are all stored in spot one of the every array.
# S,R, and Q are the coordinates of the ship tshis program handles. X and Y are the human-readable part, ARE ONLY GENERATED FOR SECONDARY BURN AND QUERY POSITION.ß
#Destroyed asks if the ship has been destroyedor rendered inoperable. 0 == no, 1 == yes.
#Secondaries are for the secondary burn
update_message = 'Acceleration applied, momentum is: '
messagecontent = 'placeholder'
#update_message == where I construct the messages to be put in discord, messagecontent == just the content of the message its looking at,
# because ToLowerCase doesn't work with message.content
#csv_string houses the string of commands that are passed to dark
arrow_array_list = ['⇑', '⇗', '⇘', '⇓', '⇙', '⇖']
#List of arrows to be yoinked in some places
csv_string = ''
#Tells me how I should update the CSV file for Dark

def Easter_Egg_Manager ():
  egg_name = ['chocolate chip cookie', 'sugar cookie', 'snickerdoodle']
  egg_lines = ['*Epsilone takes one of the chocolate chip cookies, staring down the Arch Admiral on screen while munching.* "As I was saying, we will not surrender to you. Raise your shields!"',
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

    
  

def Assemble_burn_message (relevant_momentum,relevant_arrow_1,relevant_arrow_2):
  global update_message
  print('use relevant momentum has activated')
  if(relevant_momentum == left_up_right_down or up_down or right_up_left_down):
   if(int(relevant_momentum[shipnumber_indentification]) > 0) :
     update_message = update_message + ' ' + relevant_arrow_1 + str(relevant_momentum[shipnumber_indentification])

   if((relevant_momentum[shipnumber_indentification]) < 0) :
     update_message = update_message + " " + relevant_arrow_2 + str(abs(int(relevant_momentum[shipnumber_indentification])))

  else: 
    Determine_XY_Position()


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
    applied_speed +=  int((messagecontent[messagecontent.find('⇙'): messagecontent.find('⇙') + 3])[1])

  if('⇖' in messagecontent):
    applied_speed +=  int((messagecontent[messagecontent.find('⇖'): messagecontent.find('⇖') + 3])[1])

  #This adds up all the ordered acceleration and checks if its over the max acceleration of the ship
  print(applied_speed)
  if(int(applied_speed) > int(maxa[shipnumber_indentification])) :
    update_message = 'Error: Too much acceleration applied, engine strain outside of acceptable parameters.'
  
  else :
    Update_Undo_Backup()
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
#The way the string mess works is that the first string looks through the entire message for where the arrow is then takes that and the next 2 characters.
#That is then run through a string that takes the numbers and ignores the arrow.


  #The above part runs through every direction, and if its > 0 it adds it to the message.

#Constructs a discord message with all the non-zero and non-negative velocities.

def Extract_Warp_momentum():
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
    applied_speed +=  int((messagecontent[messagecontent.find('⇙'): messagecontent.find('⇙') + 3])[1])

  if('⇖' in messagecontent):
    applied_speed +=  int((messagecontent[messagecontent.find('⇖'): messagecontent.find('⇖') + 3])[1])

  #This adds up all the ordered acceleration and checks if its over the max acceleration of the ship
  print(applied_speed)
  if(int(applied_speed) > int(maxa[shipnumber_indentification])) :
    update_message = 'Error: Too much acceleration applied, engine strain outside of acceptable parameters.'
  
  else :
    Update_Undo_Backup()
    print('max a check has suceeded')
    if '⇑' in messagecontent:
      (secondary_up_down[shipnumber_indentification]) = int((messagecontent[messagecontent.find('⇑'):messagecontent.find('⇑') + 3])[1])

    if '⇓' in messagecontent:
      secondary_up_down[shipnumber_indentification] = int(secondary_up_down[shipnumber_indentification]) - int(((messagecontent[messagecontent.find('⇓'):
         messagecontent.find('⇓') + 3]))[1])

    if '⇖' in messagecontent:
      secondary_left_up_right_down[shipnumber_indentification] =  int(((messagecontent[messagecontent.find('⇖'):
        messagecontent.find('⇖') + 3])[1]))

    if '⇘' in messagecontent:
      secondary_left_up_right_down[shipnumber_indentification] = int(secondary_left_up_right_down[shipnumber_indentification]) - int(((messagecontent[messagecontent.find('⇘'):
        messagecontent.find('⇘') + 3])[1]))

    if '⇗' in messagecontent:
      secondary_right_up_left_down[shipnumber_indentification] =  int(((messagecontent[messagecontent.find('⇗'):
        messagecontent.find('⇗') + 3])[1]))

    if '⇙' in messagecontent:
      secondary_right_up_left_down[shipnumber_indentification] = int(secondary_right_up_left_down[shipnumber_indentification]) - int(((messagecontent[messagecontent.find('⇙'):
        messagecontent.find('⇙') + 3])[1]))
#A version of extract relevant but for secondary burn

def Update_Position():
  q[shipnumber_indentification] = int(q[shipnumber_indentification]) + int(right_up_left_down[shipnumber_indentification]) - int(left_up_right_down[shipnumber_indentification])
  print('Q is ' + str(q[shipnumber_indentification]))
  s[shipnumber_indentification] = int(s[shipnumber_indentification]) + int(up_down[shipnumber_indentification]) + int(left_up_right_down[shipnumber_indentification])
  r[shipnumber_indentification] = int(r[shipnumber_indentification]) + int(up_down[shipnumber_indentification]) + int(right_up_left_down[shipnumber_indentification])
#This updates a ship position in qrs based on an accel order.

def Warp_Update_Position():
  q[shipnumber_indentification] = int(q[shipnumber_indentification]) + int(secondary_right_up_left_down[shipnumber_indentification]) - int(secondary_left_up_right_down[shipnumber_indentification])
  print('Q is ' + str(q[shipnumber_indentification]))
  s[shipnumber_indentification] = int(s[shipnumber_indentification]) + int(secondary_up_down[shipnumber_indentification]) + int(secondary_left_up_right_down[shipnumber_indentification])
  r[shipnumber_indentification] = int(r[shipnumber_indentification]) + int(secondary_up_down[shipnumber_indentification]) + int(secondary_right_up_left_down[shipnumber_indentification])
#This updates a ship position in qrs based on an accel order. Secondary burn version


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
  length = len(shipnames)
  while(shipfound == 0 and shipnumber_indentification <= length ) :
    if shipnames[shipnumber_indentification] in messagecontent:
      shipfound = 1
      print('ship found! Ship is ' + shipnames[shipnumber_indentification])
    
    else :
      shipnumber_indentification += 1
      print('still searching for ship')
      print(length)
    
def Determine_XY_Position ():
    global update_message
    global shipnumber_indentification
    print('x is ' + str(x[shipnumber_indentification]))
    print('q is ' + str(q[shipnumber_indentification]))
    x[shipnumber_indentification] = q[shipnumber_indentification]
    print('S is ' + str(s[shipnumber_indentification]))
    print('Q is ' + str(q[shipnumber_indentification]))
    print('Half of Q is ' + str(math.floor(q[shipnumber_indentification]/2)))
    y[shipnumber_indentification] = (s[shipnumber_indentification]) + (math.floor(+q[shipnumber_indentification]/2))
    print ('query position: X is '+ str(x[shipnumber_indentification]) + ', y is ' + str(y[shipnumber_indentification]))
    update_message = update_message + 'x:'+ str(x[shipnumber_indentification]) + ' y:' + str(y[shipnumber_indentification])
#Determine XY is used by secondary Burn and Query Position to turn the QRS position tracker the code uses into human-readable XY
  
def Update_Undo_Backup ():
  backup_string = [shipnames,left_up_right_down,up_down,right_up_left_down,q,r,s,maxa,destroyed,faction,secondary_left_up_right_down,secondary_right_up_left_down,secondary_up_down,x,y]
  with open('GatewalkerBackupStats.JSON', 'w') as json_file:
    json.dump(backup_string, json_file)
  with open('csv_backup.csv', 'w', encoding='UTF8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([csv_string])
  #Update undo backup triggers at the start of any action command (add ship, primary burn, sec. burn, swap faction, destroy, disable) plus wipe bot memory. 
  #It works by writing to a Json file for its data and a csv file for the commands sent to Dark' bot. 


def Update_Crash_Backup ():
  backup_string = [shipnames,left_up_right_down,up_down,right_up_left_down,q,r,s,maxa,destroyed,faction,secondary_left_up_right_down,secondary_right_up_left_down,secondary_up_down,x,y]
  with open('GatewalkerCrashBackup.JSON', 'w') as json_file:
    json.dump(backup_string, json_file)
  with open('csv_backup.csv', 'w', encoding='UTF8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([csv_string])
#Update Crash Backup is slightly different than Undo backup. It triggers at the start of any command, not just the action ones,
#This ensures that if that command crashes the bot, nothing is lost. 

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
  global csv_string


  if message.author == client.user:
    return
  global messagecontent
  messagecontent = (message.content).lower()
  print('message content is' + message.content)
  print('test') 

#######################
######/Action Commands#########
#######################

  if 'add ship' in messagecontent:
   Update_Crash_Backup()
   Update_Undo_Backup()
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
   global secondary_up_down
   global secondary_left_up_right_down 
   global secondary_right_up_left_down 

   print('ship added')
   shipnumber_creation = shipnumber_creation + 1
   shipnames.insert(shipnumber_creation,messagecontent[9:(messagecontent.find(':') - 2)])
   up_down.insert(shipnumber_creation, 0)
   left_up_right_down.insert(shipnumber_creation, 0)
   right_up_left_down.insert(shipnumber_creation, 0)
   secondary_up_down.insert(shipnumber_creation, 0)
   secondary_left_up_right_down.insert(shipnumber_creation, 0)
   secondary_right_up_left_down.insert(shipnumber_creation, 0)
   destroyed.insert(shipnumber_creation, 0)
   extract_starting_position(shipnumber_creation)
   print(shipnumber_creation)
   maxa.insert(shipnumber_creation, int(messagecontent[messagecontent.find(':') + 1 :][(messagecontent[messagecontent.find(':') + 1 :]).find(':') + 1: (messagecontent[messagecontent.find(':') + 1 :]).find(':') + 3]))
   print('Maxa is ' + str(maxa[shipnumber_creation]))
   faction.insert(shipnumber_creation,(messagecontent[messagecontent.rfind(':') + 1 : messagecontent.rfind(':') + 2]))
   #Easter_Egg_Manager()
   update_message = 'The ' + shipnames[shipnumber_creation] + ' has joined the fleet!'
   print(update_message)
   await message.channel.send(update_message)
   csv_string += 'add,' + faction[shipnumber_creation] + ',' + shipnames[shipnumber_creation] + ',' + str(x[shipnumber_creation]) + ',' + str(y[shipnumber_creation]) + '\n'
   with open('ShipPos.csv', 'w', encoding='UTF8', newline= '\n') as csv_file:
     writer = csv.writer(csv_file)
     writer.writerow([csv_string])
   #exec(open("MapRunner.py").read())
     #This is the add ship command. It replaces all the data in that row with baseline, then checks if an easter egg == applicable, sends the message, and updates the CSV and the bot.
  

  if 'primary burn' in messagecontent:
    Update_Crash_Backup()
    global shipnumber_indentification
    print('Primary acceleration has been passed')
    update_message = 'Acceleration applied, momentum is '
    Find_Called_Ship()
    if destroyed[shipnumber_indentification] == 0:
      print('destroyed check has been passed')
      Extract_relevant_momentum()
      print('Extract Momentum has ended')
      if update_message != 'Error: Too much acceleration applied, engine strain outside of acceptable parameters.':
        Assemble_burn_message(up_down,'⇑','⇓')
        Assemble_burn_message(left_up_right_down,'⇖','⇘')
        Assemble_burn_message(right_up_left_down,'⇗','⇙')
        print('Update position has been reached')
        Update_Position()
        if(update_message == "Acceleration applied, momentum is ") : update_message = 'Acceleration applied, ship is stationary.'
        else:
           csv_string += 'mov,' + str(shipnames[shipnumber_indentification]) + ',' + str(q[shipnumber_creation]) + ',' + str(r[shipnumber_creation]) + ',' + str(s[shipnumber_creation]) + '\n'
           with open('ShipPos.csv', 'w', encoding='UTF8', newline= '\n') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([csv_string])
    #exec(open("MapRunner.py").read())
    #This first finds the called ship, runs extraxt momentum, and if it hasn not exceeded
    else: update_message = 'Error: ship is inoperable.'
    await message.channel.send(update_message)  

        
  if 'secondary burn' in messagecontent: 
   Update_Crash_Backup()
   print('secondary acceleration has been passed')
   update_message = 'Secondary Burn applied, position is now '
   Find_Called_Ship()
   secondary_right_up_left_down[shipnumber_indentification] = 0
   secondary_left_up_right_down[shipnumber_indentification] = 0
   secondary_up_down[shipnumber_indentification] = 0
   if destroyed[shipnumber_indentification] == 0:
    print('destroyed check has been passed')
    Extract_Warp_momentum()
    print('Extract Momentum has ended')
    if update_message != 'Error: Too much acceleration applied, engine strain outside of acceptable parameters.':
      Warp_Update_Position()
      Determine_XY_Position()
      print('Update position has been reached')
      if(update_message == "Acceleration applied, momentum is ") : update_message = 'Acceleration applied, ship is stationary.'
      #else:
       #csv_string += 'mov,' + str(shipnames[shipnumber_indentification]) + ',' + str(q[shipnumber_creation]) + ',' + str(r[shipnumber_creation]) + ',' + str(s[shipnumber_creation]) + '\n'
       #with open('ShipPos.csv', 'w', encoding='UTF8', newline= '\n') as csv_file:
         #writer = csv.writer(csv_file)
         #writer.writerow([csv_string])
    else: update_message = 'Error: ship is inoperable.'
    await message.channel.send(update_message)  

  if 'swap faction' in messagecontent :
    Update_Crash_Backup()
    Update_Undo_Backup()
    Find_Called_Ship()
    faction[shipnumber_indentification] = messagecontent[messagecontent.find(':') + 1:messagecontent.find(':') + 2]
    if(faction[shipnumber_indentification] == 'a') : update_message = 'The ' + shipnames[shipnumber_indentification] + ' has begun broadcasting fleet IFF codes. Updating maps.'
    if(faction[shipnumber_indentification] == 'e') : update_message = 'The ' + shipnames[shipnumber_indentification] + ' has warmed up weapons. The ship is now classified as hostile.'
    if(faction[shipnumber_indentification] == 'u') : update_message = 'The ' + shipnames[shipnumber_indentification] + ' has defied previous allegiance assumptions. Reclassified.'
    if(faction[shipnumber_indentification] == 'p') : update_message = 'Good news: the ' + shipnames[shipnumber_indentification] + ' is now in control of fleet crew.'
    await message.channel.send(update_message)

  if 'destroy' in messagecontent :
    Update_Crash_Backup()
    Update_Undo_Backup()
    Find_Called_Ship()
    destroyed[shipnumber_indentification] = 1
    print(destroyed[shipnumber_indentification])
    update_message = shipnames[shipnumber_indentification] + ' has been destroyed. Prepare for a long meeting with Epsilone.'
    await message.channel.send(update_message)
    csv_string += "del," + shipnames[shipnumber_indentification] + '\n'
    with open('ShipPos.csv', 'w', encoding='UTF8', newline= '\n') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow([csv_string])
    #exec(open("MapRunner.py").read())

  if 'disable' in messagecontent :
    Update_Crash_Backup()
    Update_Undo_Backup()
    Find_Called_Ship()
    destroyed[shipnumber_indentification] = 2
    print(destroyed[shipnumber_indentification])
    update_message = shipnames[shipnumber_indentification] + ' has been disabled. Damage reports indicate the ship is still repairable.'
    await message.channel.send(update_message)
    #csv_string += "del," + shipnames[shipnumber_indentification] + '\n'
    #with open('ShipPos.csv', 'w', encoding='UTF8', newline= '\n') as csv_file:
      #writer = csv.writer(csv_file)
     # writer.writerow([csv_string])
    #exec(open("MapRunner.py").read())


#Just destroys/disables the ship listed. Pretty simple.

#######################
######/QOL Commands##########/
#######################
  if 'query momentum' in messagecontent :
    Update_Crash_Backup()
    Find_Called_Ship()
    update_message = 'Momentum of ' + shipnames[shipnumber_indentification] + ' is '
    Assemble_burn_message(up_down,'⇑','⇓')
    Assemble_burn_message(left_up_right_down,'⇖','⇘')
    Assemble_burn_message(right_up_left_down,'⇗','⇙')
    if update_message == 'Momentum of ' + shipnames[shipnumber_indentification] + ' is ' :
      update_message = 'The ' + shipnames[shipnumber_indentification] + ' is stationary.'   
    await message.channel.send(update_message)

  if 'query position' in messagecontent :
    Update_Crash_Backup()
    Find_Called_Ship()
    print(shipnames[shipnumber_indentification])
    update_message = 'Position of ' + shipnames[shipnumber_indentification] + ' is '
    Determine_XY_Position()
    await message.channel.send(update_message)

  if 'query ships' in messagecontent :
    Update_Crash_Backup()
    update_message = 'The ships are: ' + str([shipnames])
    await message.channel.send(update_message)

  if 'query faction' in messagecontent :
    Update_Crash_Backup()
    Find_Called_Ship()
    update_message = 'The ' + shipnames[shipnumber_indentification] + 'is a '
    await message.channel.send(update_message)

  if 'command list' == messagecontent :
    Update_Crash_Backup()
    update_message = 'Add ship: adds ship to combat engagement. \n Format: "add ship [shipname] P:([starting x],[starting y]) A:[maximum acceleration]" F:[factiion of ship. Player, Ally, Enemy, or Unknown]. \n'
    update_message = update_message + '\n Primary Burn: applies stated acceleration to called ship. \n format: primary burn: [ship name] [arrow followed by number without space] [repeat for all called directions] \n'
    update_message = update_message + '\n Secondary Burn: moves ship based on arrows given, does not leave residual momentum. \n format: secondary burn: [ship name] [arrow followed by number without space] [repeat for all called directions] \n'
    update_message = update_message + '\n Destroy: destroys target ship. \nformat: destroy [shipname] \n'
    update_message = update_message + '\n Disable: disables target ship. \nformat: disable [shipname] \n'
    update_message = update_message + '\n Swap Faction: swaps the faction of chosen ship. \nformat: swap faction [shipname]:[Ally/Player/Enemy/Unknown] \n'
    update_message = update_message + '\n Query momentum: gives the momentum of the called ship. \n format: Query momentum [shipname] \n'
    update_message = update_message + '\n Query position: gives the position of the called ship in xy coords. \n format: Query position [shipname]\n'
    update_message = update_message + '\n Query ships: lists the ships.\n format: Query ships \n'
    update_message = update_message + '\n Query faction: gives the faction of the called ship.\n format: Query faction \n'
    update_message = update_message + '\n command list: lists all commands. \n format:command list \n'
    update_message = update_message + '\n wipe bot memory: resets bot. Note: only jimbo, the mods, and sierra can use this command. \n format: wipe bot memory \n'
    update_message = update_message + '\n undo last command: undos the last command. Can undo wipe bot memory. \n Format: undo last command \n'
    update_message = update_message + '\n crash reload: Reloads crash. Will never loose a command if reloading from crash, unlike undo last command \n Format: crash reload \n'
    update_message = update_message + '\n Note: all commands are not case sensitive.'
    await message.channel.send(update_message)
  

            #########################
            ##########/CONSOLE COMMANDS######/
            #########################


  if messagecontent == 'undo last command' and str(message.author.id) in white_list :
    Update_Crash_Backup()
    await message.channel.send('Undoing last command.')
    backup_string = 'placeholder'
    with open('GatewalkerBackupStats.JSON', 'r') as GateFile:
      backup_string = json.load(GateFile)
    print('Undo Last Command Has Fired')
    print(backup_string)
    print('Update is happening')
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
    secondary_left_up_right_down = backup_string[10]
    secondary_right_up_left_down = backup_string[11]
    secondary_up_down = backup_string[12]
    x = backup_string[13]
    y = backup_string[14]
    with open('csv_backup.csv', 'r', encoding='UTF8') as csv_file:
      reader = csv.reader(csv_file)
      csv_string = ''
      for row in reader:
       csv_string += str(row)
    Update_Undo_Backup()
    with open('ShipPos.csv', 'w', encoding='UTF8', newline= '\n') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow([csv_string])
    #exec(open("MapRunner.py").read())
#The two csv things above me take the backup of the csv and aplly it to the current csv

#This takes the backup files and replaces the existing data from them. Works through any command, including wipe bot memory.
  if messagecontent == 'crash reload' and str(message.author.id) in white_list :
    await message.channel.send('Reloading from crash.')
    backup_string = 'placeholder'
    with open('GatewalkerCrashBackup.JSON', 'r') as GateFile:
      backup_string = json.load(GateFile)
    print('Undo Last Command Has Fired')
    print(backup_string)
    print('Update is happening')
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
    secondary_left_up_right_down = backup_string[10]
    secondary_right_up_left_down = backup_string[11]
    secondary_up_down = backup_string[12]
    x = backup_string[13]
    y = backup_string[14]
    with open('csv_backup.csv', 'r', encoding='UTF8') as csv_file:
      reader = csv.reader(csv_file)
      csv_string = ''
      for row in reader:
       csv_string += str(row)
    Update_Undo_Backup()
    with open('ShipPos.csv', 'w', encoding='UTF8', newline= '\n') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow([csv_string])
  #The two csv things above me take the backup of the csv and apply it to the current csv


  if messagecontent == 'wipe bot memory' and str(message.author.id) in white_list:
     Update_Crash_Backup()
     Update_Undo_Backup()
     await message.channel.send('wiping memory')
     shipnames = []
     up_down = []
     left_up_right_down = []
     right_up_left_down = []
     secondary_left_up_right_down = []
     secondary_right_up_left_down = []
     secondary_up_down = []
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
     with open('ShipPos.csv', 'w', encoding='UTF8', newline= '\n') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow([''])
     #exec(open("MapRunner.py").read())
  #This wipes the bot memory, except for the backup files.



client.run('')