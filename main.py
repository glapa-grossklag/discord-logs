import os
import shutil
import discord
import argparse
from datetime import datetime


os.chdir(os.path.dirname(os.path.abspath(__file__)))

parser = argparse.ArgumentParser()
parser.add_argument("email", help = "email associated with Discord account")
parser.add_argument("password", help = "Discord password to login with")
parser.add_argument("--flushlogs", help = "clear all previously stored chat logs", action = "store_true")
args = parser.parse_args()

# Wipe all log files
if args.flushlogs:
    for log in os.listdir("./logs/"):
        os.unlink("./logs/" + log)
    print("Cleared all chat logs")

# Discord listeners
client = discord.Client()

@client.event
async def on_ready():
    print(f"Connected as {client.user.name}")

@client.event
async def on_message(message):
    user = message.author
    if message.channel.is_private:
        id_to_use = ""
        if user == client.user:
            id_to_use = message.channel.recipients[0].id
        else:
            id_to_use = message.author.id

        with open("./logs/" + id_to_use + ".log", "a") as file:
            file.write(user.name+ "#" + user.discriminator + " at " + datetime.now().isoformat() + "\n")
            file.write(message.content + "\n" * 2)

client.run(args.email, args.password)
