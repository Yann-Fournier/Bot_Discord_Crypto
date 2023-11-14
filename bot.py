import discord
from discord.ext import commands
import os
from dotenv import load_dotenv , find_dotenv
from tvDatafeed import TvDatafeed, Interval

# Récuper le .env et stocker le token dans une variable
load_dotenv(find_dotenv())
bot_token = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()
client = commands.Bot(command_prefix="$", intents = intents)

# Commandes -------------------------------------------------------------------------------------------------------------------------
@client.command(name="commandes")
async def commandes(message):
    await message.channel.send("""
```markdown
# Liste des commandes:

  - $commandes: renvoie la liste des commandes
  - $valeurs: renvoie la liste des valeurs principales.
  
  
  - $test arg1: renvoie "test" et l'argument placer en paramètre
  - $img: renvoie une image
  - $plot crypto indicateur: renvoie "Voici un graphique de "crypto" avec l'"indicateur"."
  
```
""")
    
@client.command(name="valeurs")
async def crypto(message):
    await message.channel.send("""
```markdown
# Liste des principals valeurs:

  - SPX: S&P500, 500 entreprise coté en bourse au Etats-Unis
  - CAC: CAC40, les 40 plus grandes entreprises françaises
  - NDQ: NASDAQ, 100 entreprise coté en bourse au Etats-Unis

  - BTCUSD: Bitcoin / Dollard
  - ETHUSD: Etherum / Dollard
  - BNBUSD: Binance coin / Dollard

  - AAPL: Apple
  - TSLA: Tesla
  - NFLX: Netflix
  - MSFT: Microsoft corp
  - GOOG: Google
  - AMZN: Amazon
  - META: Meta
  
  - USOIL: le Pétrole
  - GOLD: l'Or
  - SILVER: l'Argent
  
```
""")

@client.command(name="test")
async def test(message, *arg1):
  await message.channel.send("test")
  await message.channel.send(arg1)


@client.command(name="img")
async def test(message):
  await message.channel.send(file=discord.File('img.png'))

@client.command(name="plot")
async def plot(message, crypto, indicateur):
  await message.channel.send(f"Voici un graphique de {crypto} avec le {indicateur}.")

# Events ---------------------------------------------------------------------------------------------------------------------------------
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
  # print(message.content)
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

# Lancement du bot ------------------------------------------------------------------------------------------------------------------------
client.run(bot_token)