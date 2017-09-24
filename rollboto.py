import discord
import asyncio
import re
import random

client = discord.Client()

def roll(command):
    message = ""
    if not re.match("\d+d\d+", command):
        message = "Invalid input"
        return message
    comm = command.split("d");
    howMany = int(comm[0])
    howLarge = int(comm[1])
    if howMany == 0:
        return "Invalid Input, cannot have zero dice"
    elif howMany > 50:
        return "Invalid Input, cannot roll more than 50 dice at once"
    if howLarge == 0:
        return "Invalid Input, cannot have a zero sided die"
    elif howLarge == 1:
        return "Invalid Input, cannot have a one sided die"
    elif howLarge > 200:
        return "Invalid Input, dice with more than 200 sides might as well be spheres"
    
    if howMany == 1:
        output = random.randint(1, howLarge)
        return "You rolled a " + str(output)
    else:
        total = 0;
        for i in range(0, howMany):
            output = random.randint(1, howLarge)
            total += output
            message += "You rolled a " + str(output) + "\n"
        message += "You rolled a total of " + str(total)
        return message

@client.event
async def on_ready():
    print("I'm in...")
    print(client.user.name)
    print(client.user.id)
    print("------")

@client.event
async def on_message(message):
    command = message.content.split(" ");
    if len(command) > 0 and command[0] == "<@"+client.user.id+">":
        if len(command) == 1:
            await client.send_message(message.channel, "Hello, I am " + client.user.name + " and I roll dice. Enter a roll using either `#d#` or `roll #d#`");
        elif len(command) > 1:
            if command[1] == "test":
                await client.send_message(message.channel, "This is a test alert of the emergency system")
            elif command[1] == "roll":
                if(len(command) == 2):
                    await client.send_message(message.channel, "Please give me a roll in d format")
                else:
                    await client.send_message(message.channel, roll(command[2]));
            elif re.match("\d+d\d+", command[1]):
                await client.send_message(message.channel, roll(command[1]));
f = open('api.key', 'r')
client.run(f.readline().strip())
