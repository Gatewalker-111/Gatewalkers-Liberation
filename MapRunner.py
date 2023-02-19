# -*- coding: utf-8 -*-
"""
Created on 18.04.2022

@author: DarkMatter1
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

###############################################################################
#---Image-Functions-----------------------------------------------------------#
###############################################################################

def add_image_over(pil_background,pil_foreground,pos):
    #Takes an image and places it over the background (centered)
    sz=pil_background.size
    szSmall=pil_foreground.size
    left=pos[1]-int(np.floor(szSmall[0]/2))
    top=pos[0]-int(np.floor(szSmall[1]/2))
    bottom=sz[1]-pos[0]-int(np.ceil(szSmall[1]/2))
    right=sz[0]-pos[1]-int(np.ceil(szSmall[0]/2))
    pil_foreground=add_margin(pil_foreground, top, right, bottom, left)
    pil_background=Image.alpha_composite(pil_background, pil_foreground)
    return pil_background

def add_margin(pil_img, top, right, bottom, left):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height))
    result.paste(pil_img, (left, top))
    return result

###############################################################################
#---Data-Functions------------------------------------------------------------#
###############################################################################

def str2img(image,string,yval,mode="w"):
    #Takes an image and a string and converts the string into image pixels via
    #ASCII code. yval is the position of the pixels
    #Writemode
    if mode=="w":
        #integer array for storage
        ch=np.zeros(len(string),dtype="int")
        for i in range(len(string)):
            #transforms each character into int (ASCII)
            ch[i]=ord(string[i])
        
        k=len(string)%4
        for i in range(0,len(string)-k,4):
            #Always puts the Characters into the 4 channels RGBA
            image.putpixel((i//4,yval-1), (ch[i], ch[i+1], ch[i+2],ch[i+3]))
        
        i=i+4
        if k==3: #Remaining strings that get filled to RGB, RG or R
            image.putpixel((i//4,yval-1), (ch[i], ch[i+1], ch[i+2],255))
        elif k==2:
            image.putpixel((i//4,yval-1), (ch[i], ch[i+1], 255,255))
        elif k==1:
            image.putpixel((i//4,yval-1), (ch[i], 255, 255,255))
    #Readmode
    else:
        i=0
        ch=""
        while i>=0:
            #Get the Pixel values
            pixvals=image.getpixel((i,yval-1))
            for j in range(4):
                #If the value==255 end of String
                if pixvals[j]==255:
                    i=-1
                    return ch
                #Append the Character to the string
                ch=ch + chr(pixvals[j])
            i=i+1

def normData(data):
    #Important function for the "add" command - this way the data is reliable
    #If no faction is given it defaults to "u"
    if len(data[1])!=1:
        data.insert(1, "u")
    k=len(data)
    #If no facing value is given, it defaults to up
    if k > 5:
        Facing=int(data[5])%6
    else:
        data.append(0)
    #If no acceleration value is given, it defaults to 0
    if k < 8:
        data.extend([0,0,0])
    return data

def clean(data):
    #Clean the string from '
    data=data.replace(" '","")
    data=data.replace("'","")
    data=data.replace('"',"")
    return data

###############################################################################
#---Coordinate-System-Converters----------------------------------------------#
###############################################################################

def xy2qrs(coords):
    #Converts the xy Coordinates (starting from the bottom left) into qrs Coords
    x=coords[0]
    y=coords[1]
    q=int(x)
    s=int(y-np.floor(x/2))
    r=int(q+s)
    return q,r,s

def qrs2xy(coords):
    #Converts the qrs Coordinates (starting from the bottom left) into xy Coords
    q=coords[0]
    s=coords[2]
    x=int(q)
    y=int(s+np.floor(q/2))
    return x,y

def xy2uv(GridDim,hexSize,pos):
    #Converts the parametric xy Coordinates in Pixels
    
    #Size of an individual Hexagon
    hexLen=4*np.floor(hexSize/2)-1
    hexHeight=2*np.round(np.sqrt(3)*np.floor(hexSize/2))-1
    #Size of the Canvas
    #x=GridDim[0]
    y=GridDim[1]
    
    #Step between middles
    stepX=(hexLen+hexSize-2)
    stepY=(hexHeight-1)
    
    #stepX/2 due to the shifting nature of the hexagons
    v=pos[0]*stepX/2
    #If x is odd shift up the y by half a hexagon
    u=abs(pos[1]-y)*stepY-1
    if np.mod(pos[0],2)==1:
        u=u-np.floor(hexHeight/2)
        
    u=int(u)
    v=int(v)
    return u,v

###############################################################################
#---Ship-Movement-------------------------------------------------------------#
###############################################################################

def adder(pos,add):
    #CAUTION, NOT COMMUTATIVE
    pos=xy2qrs(pos)
    q=pos[0]
    r=pos[1]
    s=pos[2]
    
    #Adds the q-component to the position
    firstpos=add[0]
    r=r+firstpos
    s=s+firstpos
    
    #Adds the r-component to the position
    secondpos=add[1]
    q=q+secondpos
    r=r+secondpos
    
    #Adds the s-component to the position
    thirdpos=add[2]
    q=q+thirdpos
    s=s-thirdpos
    
    newpos=qrs2xy((q,r,s))
    
    return newpos

###############################################################################
#---Map-aid-------------------------------------------------------------------#
###############################################################################

def standardMap(BorderSize,Minor,Grayval,Round,LogoText,Title, Map):
    #Start of the process that collects the correct Data, generates the Border,
    #puts the Logo in the correct Spot, adds the coordinates Markers and
    #saves the Metadata once again
    Map=Map.convert('RGBA')
    sz=Map.size
    data=Map.getpixel((0,0))
    GridSize=(data[0],data[1])
    Resolution=data[2]

    #Load the Font
    StrikeHeader = ImageFont.truetype("Resources/Standards/StrikeFighter.otf",18)
    StrikeFighter = ImageFont.truetype("Resources/Standards/StrikeFighter.otf",13)

    #Make a blank Border around the Map
    Border=Image.new('RGBA', (sz[0]+BorderSize,sz[1]+Minor), (Grayval, Grayval, Grayval, 255))
    image_editable = ImageDraw.Draw(Border)
    
    #Title
    w, h = image_editable.textsize(Title, font=StrikeHeader)
    image_editable.text((Border.size[0]/2-w/2,5), Title, (0, 0, 0), font=ImageFont.truetype("Resources/Standards/StrikeFighter.otf",40))
    
    #Coordinate Labels on x-Axis
    for i in range(1,GridSize[0]):
        pos=xy2uv(GridSize, Resolution, (i,GridSize[1]))
        w, h = image_editable.textsize(str(i), font=StrikeFighter)
        pos=(pos[1]+BorderSize-w/2,Minor-5-h)
        image_editable.text(pos, str(i), (Grayval-100, Grayval-100, Grayval-100), font=StrikeFighter)
    #Coordinate Labels on y-Axis
    for i in range(GridSize[1]):
        pos=xy2uv(GridSize, Resolution, (0,i))
        w, h = image_editable.textsize(str(i), font=StrikeFighter)
        pos=(BorderSize-5-w,pos[0]+Minor-h/2)
        image_editable.text(pos, str(i), (Grayval-100, Grayval-100, Grayval-100), font=StrikeFighter)
    
    #Logo in the top left corner
    Logo = Image.open("Resources/" + LogoText).convert('RGBA')
    Logo = Logo.resize((BorderSize,BorderSize))
    Logo=add_margin(Logo, 0, Border.size[0]-BorderSize, Border.size[1]-BorderSize, 0)
    Border=Image.alpha_composite(Border, Logo)
    
    #Save the metadata in the LowerLeft
    str2img(Border,str((BorderSize,Minor,Grayval,Round,LogoText,Title)),Border.size[1])
    
    return Map,Border,GridSize,Resolution

def placeShips(Border,Map,shipData,BorderSize,GridSize,Resolution):
    #Goes through every ship and places it on the map, as well as the descriptive
    #Text on the side
    
    image_editable = ImageDraw.Draw(Border)
    StrikeFighter = ImageFont.truetype("Resources/Standards/StrikeFighter.otf",13)
    #Load the Ship Icons
    ShipPlayer = Image.open("Resources/Standards/ShipPlayer.png").convert('RGBA')
    ShipEnemy = Image.open("Resources/Standards/ShipEnemy.png").convert('RGBA')
    ShipAlly = Image.open("Resources/Standards/ShipAlly.png").convert('RGBA')
    ShipUnknown = Image.open("Resources/Standards/ShipUnknown.png").convert('RGBA')
    
    #For every ship in the list
    for i in range(len(shipData)):
        Name=shipData[i][1]
        pos=(int(shipData[i][2]),int(shipData[i][3]))
        Facing=int(shipData[i][4])
            
        offset=BorderSize + 50+13*i
        #Icon choosing depended on faction/Text on the side
        if shipData[i][0]=="p":
            Icon=ShipPlayer
            image_editable.text((20,offset), Name + " " + str(pos), (0, 0, 0), font=StrikeFighter)
        elif shipData[i][0]=="e":
            Icon=ShipEnemy
            image_editable.text((20,offset), Name + " " + str(pos), (200, 0, 0), font=StrikeFighter)
        elif shipData[i][0]=="a":
            Icon=ShipAlly
            image_editable.text((20,offset), Name + " " + str(pos), (0, 200, 0), font=StrikeFighter)
        else:
            Icon=ShipUnknown
            image_editable.text((20,offset), Name + " " + str(pos), (200, 200, 200), font=StrikeFighter)
        
        #Rotate the ship accordingly
        IconRot = Icon.rotate(-60*Facing, resample=Image.BICUBIC)
        
        #Place the marker on the map
        PosUV=xy2uv(GridSize, Resolution, pos)
        Map=add_image_over(Map, IconRot, PosUV)
        Map_editable = ImageDraw.Draw(Map)
        Map_editable.text((PosUV[1]+5,PosUV[0]-Resolution/2), Name, (200, 200, 200), font=StrikeFighter)
        
        #Add the metadata on the bottom left
        str2img(Border,str(shipData[i]),Border.size[1]-i-1)
        
    return Border,Map,offset

def finishing(Border,Map,BorderSize,Minor,offset,Round):
    #Adds the remaining Headers, and combines the Border with the map
    
    image_editable = ImageDraw.Draw(Border)
    StrikeHeader = ImageFont.truetype("Resources/Standards/StrikeFighter.otf",18)
    
    #Ship Locations header
    w, h = image_editable.textsize("Ship Locations", font=StrikeHeader)
    image_editable.text((BorderSize/2-w/2,BorderSize + 25), "Ship Locations", (0, 0, 0), font=StrikeHeader)
    
    #Round Counter
    w, h = image_editable.textsize("Round " + str(Round), font=StrikeHeader)
    image_editable.text((BorderSize/2-w/2,offset + 25), "Round " + str(Round), (0, 0, 0), font=StrikeHeader)
    
    #Combine the Map and the Border together
    MapShift=add_margin(Map, Minor, 0, 0, BorderSize)
    BattleMap=Image.alpha_composite(Border, MapShift)
    return BattleMap

###############################################################################
#---MAIN----------------------------------------------------------------------#
###############################################################################

def updateMap(Previous,Filename,BaseMap):
    #Takes the Previous map and updates it. It collects the data, as well as
    #the new instructions and saves it again.
    #Extract the Metadata - Image related
    data=str2img(Previous,"",Previous.size[1],"r")
    data=data.replace("(", "")
    data=data.replace(")", "")
    data=data.split(",")
    
    BorderSize=int(data[0])
    Minor=int(data[1])
    Grayval=int(data[2])
    Round=int(data[3])+1
    Logo=clean(data[4])
    Title=clean(data[5])
    Blank = BaseMap.crop((BorderSize, Minor, Previous.size[0], Previous.size[1]))
    #Generate the fitting Border, Logo, Coordinates...
    Map,Border,GridSize,Resolution=standardMap(BorderSize, Minor, Grayval, Round, Logo, Title, Blank)
    
    #Extract the Shipdata from the Lowerleft corner
    i=1
    shipData=[]
    while i>=0:
        newdata=clean(str2img(Previous,"",Previous.size[1]-i,"r"))
        newdata=newdata.replace("[", "")
        newdata=newdata.replace("]", "")
        newdata=newdata.split(",")
        if len(newdata)!=1:
            shipData.append(newdata)
            i=i+1
        else:
            i=-1
            
    #Open new instructions and split them into lines
    f = open(Filename, "r")
    f=f.read()
    f=f.splitlines()
    #Walk through for every instruction
    for i in range(len(f)):
        new=f[i]
        new=new.split(",")
        mode=new[0]
        #Add a new ship to the map
        if mode=="add":
            new=normData(new)
            NameAdd=new[2]
            #Check if the ship already exists, then do not add it
            valid=True
            for j in range(len(shipData)):
                Name=shipData[j][1]
                if NameAdd==Name:
                    valid=False
            if valid==True:
                shipData.append(new[1:])
        
        #Move an existing ship on the map (with Newtonian Physics)
        elif mode=="mov":
            NameMov=new[1]
            for j in range(len(shipData)):
                Name=shipData[j][1]
                if NameMov==Name:
                    #Takes the Position, Acceleration, as well as previous Acceleration
                    #and calculates the next position and heading
                    pos=(int(shipData[j][2]),int(shipData[j][3]))
                    previousAccel=np.array((int(shipData[j][5]),int(shipData[j][6]),int(shipData[j][7])))
                    accel=np.array((int(new[2]),int(new[3]),int(new[4])))
                    accel=accel+previousAccel
                    newpos=adder(pos,accel)
                    shipData[j][2]=newpos[0]
                    shipData[j][3]=newpos[1]
                    shipData[j][5]=accel[0]
                    shipData[j][6]=accel[1]
                    shipData[j][7]=accel[2]
                    
                    #Heading being determined by the direction of the maximum
                    #acceleration
                    if abs(accel[0])>=max(abs(accel[1]),abs(accel[2])):
                        if accel[0]>0:
                            shipData[j][4]=0
                        else:
                            shipData[j][4]=3
                            
                    if abs(accel[1])>=max(abs(accel[0]),abs(accel[2])):
                        if accel[1]>0:
                            shipData[j][4]=1
                        else:
                            shipData[j][4]=4
                            
                    if abs(accel[2])>=max(abs(accel[0]),abs(accel[1])):
                        if accel[2]>0:
                            shipData[j][4]=2
                        else:
                            shipData[j][4]=5
                    break
        
        #Delete a ship from the Map
        elif mode=="del":
            NameDel=new[1]
            for j in range(len(shipData)):
                Name=shipData[j][1]
                if NameDel==Name:
                    shipData.pop(j)
                    break
    #With the new ships added, old ones moved or deleted, place the Ships at their correct locations
    Border,Map,offset=placeShips(Border,Map,shipData,BorderSize,GridSize,Resolution)
    #Pull everything together
    BattleMap=finishing(Border,Map,BorderSize,Minor,offset,Round)
    return BattleMap

def Map_Runner(round,map_name):
    Filename = "creation/data/commands.txt"
    try:
        string='creation/maps/' + str(map_name) + str(round-1) + '.png'
        zerostring='creation/maps/' + str(map_name) + '0.png'
        BaseMap = Image.open(zerostring).convert('RGBA')
        BattleMap = Image.open(string).convert('RGBA')

        BattleMap = updateMap(BattleMap,Filename,BaseMap)
        print("Map ready for next round")
        BattleMap.save('creation/maps/' + str(map_name) + str(round) + '.png')
        return BattleMap
    except:
        print("Please first initialize the Map first")
