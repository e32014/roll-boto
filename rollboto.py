import discord
import asyncio
import re
import random
from collections import deque

client = discord.Client()

def commandStructure( commandStack ):
    if len(commandStack) > 0:
        command = commandStack.popleft()   
        if command == "test":
            return "This is a test alert of the emergency system", 0        
        elif command == "roll":
            return rollCommand( commandStack, 0 )
        elif re.match("^\d+d\d+$", command):
            message, tot = roll(command)
            if tot == -1:
                return message, -1
            contMess, error = rollCommand( commandStack, tot )
            if error == -1:
                return contMess, -1
            return message + contMess, 0
        else:
            return "Not a valid command", -1
    else:
        return "Hello, I am " + client.user.name + " and I roll dice. Enter a roll using either `#d#` or `roll #d#`", 0

def rollCommand( commandStack, currTotal ):
    if len( commandStack ) > 0:
        command = commandStack.popleft()
        if re.match("^\d+d\d+$", command):
            message, tot = roll(command)
            if tot == -1:
                return message, -1
            contMess, error = rollCommand(commandStack, currTotal + tot)
            if error == -1:
                return contMess, -1
            return message + contMess, 0 
        else:
            return "Not a valid roll command", -1
    else:
        return "You rolled a grand total of **" + str(currTotal) + "**", 0


def roll(command):
    message = ""
    if not re.match("^\d+d\d+$", command):
        message = "Invalid input"
        return message, -1
    comm = command.split("d");
    howMany = int(comm[0])
    howLarge = int(comm[1])
    if howMany == 0:
        return "Invalid Input, cannot have zero dice", -1
    elif howMany > 50:
        return "Invalid Input, cannot roll more than 50 dice at once", -1
    if howLarge == 0:
        return "Invalid Input, cannot have a zero sided die", -1
    elif howLarge == 1:
        return "Invalid Input, cannot have a one sided die", -1
    elif howLarge > 200:
        return "Invalid Input, dice with more than 200 sides might as well be spheres", -1
    
    total = 0;
    message += "With **" + command + "**, you rolled a "
    for i in range(0, howMany):
        output = random.randint(1, howLarge)
        total += output
        message += "**" + str(output) + "**"
        if howMany - i > 2:
            message += ", "
        elif howMany - i == 2 and howMany == 2:
            message += " and "
        elif howMany - i == 2 and howMany > 2:
            message += ", and "
            
    message += " for a total of **" + str(total) + "**\n"
    return message, total

@client.event
async def on_ready():
    print("I'm in...")
    print(client.user.name)
    print(client.user.id)
    print("------")

@client.event
async def on_message(message):
    command = deque(message.content.split(" "));
    if len(command) > 0 and command[0] == "<@"+client.user.id+">":
        command.popleft()
        await client.send_message(message.channel, commandStructure(command)[0] );

f = open('api.key', 'r')
client.run(f.readline().strip())
