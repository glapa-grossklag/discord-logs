import os
import argparse
from datetime import datetime
import discord


os.chdir(os.path.dirname(os.path.abspath(__file__)))

parser = argparse.ArgumentParser()
parser.add_argument("email", help = "email associated with Discord account")
parser.add_argument("password", help = "Discord password to login with")
parser.add_argument("--flushlogs", help = "clear all previously stored chat logs", action = "store_true")
args = parser.parse_args()

def write_to_log(message, text):
    # Select ID to use in logfile name
    filename = message.channel.recipients[0].id if (message.author == client.user) else message.author.id
    with open("./logs/" + filename + ".log", "a") as file:
        file.write(message.author.name+ "#" + message.author.discriminator + " at " + datetime.now().isoformat() + "\n")
        file.write(text + "\n" * 2)

# Create logs folder if it doesn't exist
if not os.path.exists("./logs/"):
    print("Creating log folder...")
    os.makedirs("./logs/")

# Wipe all log files
if args.flushlogs:
    for log in os.listdir("./logs/"):
        os.unlink("./logs/" + log)
    print("Cleared all chat logs")

client = discord.Client()
print("Connecing to Discord...")

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

@client.event
async def on_message(message):
    if not message.channel.is_private: return
    write_to_log(message, message.content)

@client.event
async def on_message_edit(before, after):
    if not before.channel.is_private: return
    write_to_log(before, before.content +  "\n  EDITED TO\n" + after.content)

client.run(args.email, args.password)
