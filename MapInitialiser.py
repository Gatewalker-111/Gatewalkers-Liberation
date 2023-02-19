# -*- coding: utf-8 -*-
"""
Created on 18.04.2022

@author: DarkMatter1
"""
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

###############################################################################
#---BATTLE-MAP DRAWING--------------------------------------------------------#
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

def standardMap(BorderSize,Minor,Grayval,Round,LogoText,Title,Map):
    #Start of the process that collects the correct Data, generates the Border,
    #puts the Logo in the correct Spot, adds the coordinates Markers and
    #saves the Metadata once again
    
    #Load the Map and fetch the metadata
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

def initBattleMap(Map):
    #First main for initialising the Map. It only takes the ini command
    List = pd.read_excel (r'creation/data/Parameters.xlsx', sheet_name='Commands')
    List=List.set_index('Map Dimensions')
    
    Logo=List.loc["Logo"].at["Value"] + ".png"
    Title=List.loc["Title"].at["Value"]
    Grayval=List.loc["Grayval"].at["Value"]
    BorderSize=List.loc["BorderSize"].at["Value"]
    Minor=List.loc["Minor"].at["Value"]
    
    if type(Grayval)!=int:
        if np.isnan(Grayval):
            Grayval=255
    Grayval=int(Grayval)
    if type(BorderSize)!=int:
        if np.isnan(BorderSize):
            BorderSize=200
    BorderSize=int(BorderSize)
    if type(Minor)!=int:
        if np.isnan(Minor):
            Minor=100
    Minor=int(Minor)
    
    Round=-1
    #Generate the fitting Border, Logo, Coordinates...
    Map,Border,GridSize,Resolution=standardMap(BorderSize, Minor, Grayval, Round, Logo,Title,Map)
    #Pull everything together
    BattleMap=finishing(Border,Map,BorderSize,Minor,BorderSize + 50,Round)
    print("Finished Initalising the Battlemap")
    return BattleMap

###############################################################################
#---MAP DRAWING---------------------------------------------------------------#
###############################################################################

def initMap():
    
    #Read the Execl for the Map Parameters
    List = pd.read_excel(r'creation/data/Parameters.xlsx', sheet_name='Commands')
    List=List.set_index('Map Dimensions')
    xDim=int(List.loc["x"].at["Value"])
    yDim=int(List.loc["y"].at["Value"])
    Resolution=List.loc["Resolution"].at["Value"]
    BgImg=List.loc["Background Image"].at["Value"]
    #Get the GridSize
    GridSize=(xDim,yDim)
    
    if type(Resolution)!=int:
        if np.isnan(Resolution):
            Resolution=31
    Resolution=int(Resolution)
    if type(BgImg)!=str:
        if np.isnan(BgImg):
            BgImg=1
    
    #Check if the Values are correct
    if np.mod(Resolution,2)==0:
        Resolution=Resolution+1
    if np.mod(GridSize[0],2)==1:
        GridSize=(GridSize[0]+1,GridSize[1])
    
    
    
    tile, marker=hextile(Resolution)
    #tile=tile+marker
    Grid=gridMaker(tile,GridSize)
    
    #Get the Grid Sizes
    a=len(Grid)
    b=int(Grid.size/a)
    
    #The rgb gets filled with white the a is controlled by the Grid
    White=np.ones((a,b,3))
    Grid=np.dstack((White,Grid))
    HexIm=Image.fromarray(np.uint8(Grid*100)).convert("RGBA")
    
    #Blurring the Grid for visual effect
    blurImage = HexIm.filter(ImageFilter.GaussianBlur(1.5))
    HexIm=Image.alpha_composite(HexIm,blurImage)
    
    if BgImg==1:
        #Black Background
        Black=np.zeros((a,b))
        Black=Image.fromarray(np.uint8(Black)).convert("RGBA")
        HexIm=Image.alpha_composite(Black,HexIm)
    if type(BgImg) == str:
        imageName="Resources/"+BgImg+".png"
        Picture = Image.open(imageName).convert('RGBA')
        Picture = Picture.resize((b,a))
        Picture = ImageEnhance.Brightness(Picture).enhance(0.3)
        HexIm=Image.alpha_composite(Picture,HexIm)
    print("Finished Initalising the Background")
    return HexIm, GridSize, Resolution

def drawHexagon(sidelen):
    
    #Diagonals
    sidelen=int(np.floor(sidelen/2))
    #Prepare a canvas with size s/2 and sqrt(3)*s/2
    zero=np.zeros((sidelen,round(np.sqrt(3)*sidelen)))
    height=int(np.size(zero)/sidelen)
    
    #implicit formula 0=sqrt(3)*x-y
    for i in range(height):
        for j in range(sidelen):
            if abs(np.sqrt(3)*j-i)<1:
                zero[j,i]=1
    
    #Building up the Hexagonsides
    zero=np.transpose(zero)
    dzero=np.flip(zero,0)
    dzero=dzero[1:,:]
    dzero=np.vstack((zero,dzero))
    
    #Building up the middle
    middleline=np.ones(sidelen*2-1)
    middle=np.zeros((len(dzero)-2,sidelen*2-1))
    
    #Building the whole Hexagon
    middle=np.vstack((middleline,middle,middleline))
    
    hexagon=np.hstack((np.flip(dzero,1),middle,dzero))
    #HexIm=Image.fromarray(np.uint8(hexagon*255))
    #HexIm.show()
    return hexagon
    
def hextile(HexRes):
    #  /   \
    #--|   |--
    #  \___/
    
    #Draws the middle Hexagon
    hexagon=drawHexagon(HexRes)
    height=len(hexagon)
    side=int(np.size(hexagon)/height)
    halfs=int(np.floor(side/2))+2
    halfh=int(np.floor(height/2))
    
    #Prepare the lines on the sides
    filler=np.zeros((halfh,int(np.floor(halfs/2))))
    line=np.ones(int(np.floor(halfs/2)))
    side=np.vstack((filler,line,filler))
    
    #Stick the Lines onto the Hexagon
    tile=np.hstack((side,hexagon,side))
    
    #Rmove the outer edges to avoid doubling at the edges
    tile=tile[1:,:-1]
    
    #Marker for the Middle
    height=len(tile)
    side=int(np.size(tile)/height)
    middlemark=tile*0
    middlemark[height-1,0]=1
    middlemark[int(np.floor(height/2)-1),int(side/2)]=1 
    return tile, middlemark

def gridMaker(tile,CanvasDim):
    #due to the shape of the base tile x will always be even
    x=CanvasDim[0]
    y=CanvasDim[1]
    x=int(x/2);
    xcanvas=tile
    #Stacks the Hex-Tiles sideways then on top to create the grid
    for i in range(x-1):
        xcanvas=np.hstack((xcanvas,tile))
    ycanvas=xcanvas
    for i in range(y-1):
        ycanvas=np.vstack((ycanvas,xcanvas))
    return ycanvas

###############################################################################
#---OBJECT DRAWING------------------------------------------------------------#
###############################################################################

def initObjects(GridSize, Resolution):
    #Reads the Objects from the Excel file
    List=pd.read_excel(r'creation/data/Parameters.xlsx', sheet_name='Mapper')
    List=List.set_index('Coords')
    
    #Generates an empty canvas to stack the Objects onot
    param=xy2uv(GridSize, Resolution, (GridSize[0],0))
    param=(param[1],param[0]+1)
    Foreground=Image.new('RGBA', (param))
    
    #For every Cell in the Map go through
    sz=List.shape
    for x in range(sz[1]):
        for y in range(sz[0]):
            Object=List.loc[y].at[x]
            #If not empty (NaN)=int then continue
            if type(Object)==str:
                #Search for the Scaling Factor in front
                try:
                    Scale=int(Object[0:2])
                    Object=Object[2:]
                except:
                    try:
                        Scale=int(Object[0])
                        Object=Object[1:]
                    except:
                        Scale=1
                #Get the Name
                Name=Object[0:2]
                Object=Object[2:]
                #Get the (random) Variant
                if Object=="":
                    #Try anything from 0 to 10
                    Variant=np.random.randint(10)
                    String="Resources/"+str(Name)+"_"+str(Variant)+".png"
                    try:
                        Picture = Image.open(String).convert('RGBA')
                    except:
                        #Try anything from 0 to 5
                        Variant=np.random.randint(5)
                        String="Resources/"+str(Name)+"_"+str(Variant)+".png"
                        try:
                            Picture = Image.open(String).convert('RGBA')
                        except:
                            #Choose Variant 0
                            Variant=0
                            String="Resources/"+str(Name)+"_"+str(Variant)+".png"
                            try:
                                Picture = Image.open(String).convert('RGBA')
                            except:
                                Picture = Image.open("Resources/Test.png").convert('RGBA')
                #Get the specified Variant
                else:
                    Variant=Object
                    String="Resources/"+str(Name)+"_"+str(Variant)+".png"
                    try:
                        Picture = Image.open(String).convert('RGBA')
                    except:
                        Picture = Image.open("Resources/Test.png").convert('RGBA')
                
                #With Object Scatter place the Object at the correct position and add it to the Foreground
                newForeground=ObjectScatter(Picture, Resolution, GridSize, (x,y),Scale)
                if Scale>4:
                    Foreground=Image.alpha_composite(newForeground,Foreground)
                else:
                    Foreground=Image.alpha_composite(Foreground,newForeground)
    
    Foreground.putpixel((0, 0), (GridSize[0], GridSize[1], Resolution,255))
    print("Finished Initalising the Foreground")
    return Foreground
    
def add_margin(pil_img, top, right, bottom, left):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height))
    result.paste(pil_img, (left, top))
    return result

def ObjectScatter(Picture,Resolution,GridSize,pos,ObjectSize=1):
    #Canvas Size
    param=xy2uv(GridSize, Resolution, (GridSize[0],0))
    param=(param[0]+1,param[1])
    
    #Hexagon Size
    hexLen=int(4*np.floor(Resolution/2)-1)
    hexHeight=int(2*np.round(np.sqrt(3)*np.floor(Resolution/2))-1)
    
    #Hexagon Size times the Size
    k=(2*ObjectSize-2)
    hexLen=(hexLen+Resolution)*ObjectSize-Resolution-k
    k=2*ObjectSize-1
    hexHeight=((hexHeight-1)*k)+1
    
    dim=np.min((hexLen,hexHeight))
    
    #Load Image
    Picture = Picture.resize((dim,dim))
    posNew=xy2uv(GridSize, Resolution, pos)
    
    #Add Margin
    Left=int(posNew[1]-np.floor(dim/2))
    Right=int(param[1]-(posNew[1]+np.ceil(dim/2)))
    Top=int(posNew[0]-np.floor(dim/2))
    Bottom=int(param[0]-(posNew[0]+np.ceil(dim/2)))
    
    Picture = add_margin(Picture, Top, Right, Bottom, Left)
    
    return Picture

def debugGrid(Canvas,Resolution,GridSize):
    #Inputs: Canvas(Image)
    #Adds labels to the Grid. In itself closed function, returns nothing, saves an image
    draw = ImageDraw.Draw(Canvas)
    xmax=GridSize[0]
    ymax=GridSize[1]
    for x in range(xmax+1):
        for y in range(ymax+1):
            Coords=xy2uv(GridSize,Resolution,(x,y))
            posx=Coords[1]
            posy=Coords[0]
            #Write the x and y Coordinates into the Grid
            draw.text((posx-Resolution/2,posy-Resolution/2),str(x) + "," + str(y),(int(255*x/xmax),int(255*y/ymax),255))
    Canvas.save('creation/maps/debug.png')
    return

###############################################################################
#---COORDINATE SYSTEM CONVERTERS----------------------------------------------#
###############################################################################

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
#---MAIN----------------------------------------------------------------------#
###############################################################################

def Map_Initialiser(file_data,map_name):

    if file_data != -1:
        # save the contents of the BytesIO object to a file
        with open('creation/data/Parameters.xlsx', 'wb') as f:
            f.write(file_data.getvalue())

    HexIm, GridSize, Resolution,=initMap()
    Foreground=initObjects(GridSize, Resolution)

    HexIm=Image.alpha_composite(HexIm, Foreground)
    # HexIm.save('creation/maps/' + str(map_name) + '.png')
    # debugGrid(HexIm,Resolution,GridSize)

    BattleMap=initBattleMap(HexIm)
    BattleMap.save('creation/maps/' + str(map_name) + '0.png')
    return BattleMap


def format_text(input_lines):
    output_text = ""
    for line in input_lines:
        if line.startswith("Add"):
            split_line = line.split(", ")
            faction = split_line[1][0].lower()
            name = split_line[2]
            pos_x = int(split_line[3])
            pos_y = int(split_line[4])
            rotation = 0
            acceleration = "0,0,0"
            if len(split_line) >= 4:
                rotation = int(split_line[5])
            if len(split_line) == 8:
                acceleration = split_line[6] + "," + split_line[7] + "," + split_line[8]
            output_text += f"add,{faction},{name},{pos_x},{pos_y},{rotation},{acceleration}\n"
        elif line.startswith("Mov"):
            split_line = line.split(", ")
            name = split_line[1]
            q, r, s = 0, 0, 0
            for move in split_line[2:]:
                if "⇑" in move:
                    q += int(move[1:])
                elif "⇓" in move:
                    q -= int(move[1:])
                elif "⇗" in move:
                    r += int(move[1:])
                elif "⇙" in move:
                    r -= int(move[1:])
                elif "⇘" in move:
                    s += int(move[1:])
                elif "⇖" in move:
                    s -= int(move[1:])
            output_text += f"mov,{name},{q},{r},{s}\n"
        elif line.startswith("Del"):
            name = line.split(", ")[1]
            output_text += f"del,{name}\n"
    return output_text.strip()