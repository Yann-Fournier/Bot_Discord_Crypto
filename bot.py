import discord
import os
from dotenv import load_dotenv , find_dotenv
from discord.ext import commands

intents = discord.Intents.all()

# Récuper le .env et stocker le token dans une variable
load_dotenv(find_dotenv())
bot_token = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix="!", intents = intents)

@client.command(name="Hello")
async def delete(ctx):
    messages = await ctx.channel.history(limit=10)

    for each_message in messages:
        await each_message.delete()

@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_typing(channel, user, when):
     await channel.send(user.name+" is typing")

@client.event
async def on_member_join(member):
    general_channel = client.get_channel(1044900412551073832)
    await general_channel.send("Bienvenue sur le serveur ! "+ member.name)

@client.event
async def on_message(message):
  # Permet au bo de ne pas ce parler à lui même
  if message.author == client.user:
    return

  # On gère les contenue des messages
  message.content = message.content.lower()

  if message.content.startswith("hello"):
    await message.channel.send("Hello")

  if "cochon" in message.content:
    await message.channel.send("Tu est ban.")

  if message.content == "azerty":
    await message.channel.send("qwerty")

  # permet de les touver si le message envoyer est une commande
  # permet de faire fonctionner les commande
  await client.process_commands(message)

# on lance le bot
client.run(bot_token)