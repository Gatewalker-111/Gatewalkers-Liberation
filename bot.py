# -*- coding: utf-8 -*-
"""
Created on 17.02.2023

@author: DarkMatter1
"""
import discord
import MapInitialiser
import responses
import io
from MapInitialiser import Map_Initialiser
from MapRunner import Map_Runner
from PIL import Image
import os
import shutil


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


async def send_image_message(image, message):
    """
    Sends an image as a file attachment in a Discord message.
    :param image: The image to send.
    :param message: The message(channel) to send the image in.
    """
    # convert image data to bytes-like object
    with io.BytesIO() as image_bytes:
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        # create a discord.File object from the image bytes
        image_file = discord.File(fp=image_bytes, filename='image.png')
        # send the file as an attachment in the message
        await message.channel.send(file=image_file)


def run_discord_bot():
    #default stuff
    TOKEN = 
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    #activation confirmation
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    active_game = False
    active_round = False
    commands = []
    round_number = 0
    game_name = "BattleMap"

    folders_to_create = [
        'Resources',
        'Resources/Standards',
        'creation',
        'creation/maps',
        'creation/data'
    ]
    for folder in folders_to_create:
        if not os.path.exists(folder):
            os.makedirs(folder)

    #message listening
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        nonlocal active_game
        nonlocal active_round
        nonlocal commands
        nonlocal round_number
        nonlocal game_name
        #debug
        print(f'{username} said: "{user_message}" ({channel})')
        if user_message[0:10] == '!generate ':
            if len(message.attachments) == 1:
                attachment = message.attachments[0]
                if attachment.filename.endswith('.xlsx'):
                    map_name=user_message[10:]
                    #read the excel and run the map initialiser program
                    Excel = io.BytesIO(await attachment.read())
                    await message.channel.send('`Creating...`')
                    image = Map_Initialiser(Excel,map_name)
                    await send_image_message(image,message)
                else:
                    await message.channel.send('Error: Please attach an Excel file.')
            else:
                try:
                    map_name = user_message[9:]
                    image = Image.open(str(map_name) + '.png').convert('RGBA')
                    await send_image_message(image, message)
                except Exception as e:
                    print(e)

        elif message.content[0:11] == '!startgame ' and not active_game:
            active_game = True
            game_name = message.content[11:]
            try:
                string = 'creation/maps/' + str(game_name) + '0.png'
                Image.open(string).convert('RGBA')
                await message.channel.send('Game started!')
            except:
                active_game=False
                await message.channel.send('Invalid Game Name!')

        elif message.content == '!stopgame' and active_game:
            round_number = 0
            active_game = False

            # Delete everything inside creation/data
            data_folder = "creation/data"
            for filename in os.listdir(data_folder):
                file_path = os.path.join(data_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

            # Delete images in creation/maps that do not end with 0.png
            maps_folder = "creation/maps"
            for filename in os.listdir(maps_folder):
                if not filename.endswith("0.png"):
                    file_path = os.path.join(maps_folder, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Reason: {e}")

            await message.channel.send('Game ended!')

        elif message.content == '!round' and active_game:
            if not active_round:
                round_number += 1
                active_round = True
                commands = ["del,x","add,u,x,-1,-1"]
                await message.channel.send(f'Round {round_number} started! Enter your commands:')
            else:
                await message.channel.send('There is already an active round in progress!')

        elif message.content == '!finish' and active_game:
            if active_round:
                active_round = False
                filename = f'creation/data/commands.txt'
                with open(filename, 'w') as file:
                    commands = MapInitialiser.format_text(commands)
                    file.writelines(commands)
                await message.channel.send(f'Round {round_number} ended! Commands saved to file {filename}.')
                image = Map_Runner(round_number,game_name)
                await send_image_message(image, message)
            else:
                await message.channel.send('There is no active round in progress!')

        elif active_round:
            commands.append(message.content + '\n')


        elif user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message,user_message,is_private=True)
        elif user_message[0] == '!':
            user_message = user_message[1:]
            await send_message(message,user_message,is_private=False)
        else:
            return

    client.run(TOKEN)