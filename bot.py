import discord
from discord.ext import commands
import os
from dotenv import load_dotenv , find_dotenv
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import ta
import utils
import mplfinance as mpf
import matplotlib.pyplot as plt

tv = TvDatafeed() # création de la connection à Tradingview.

# Récuper le .env et stocker le token dans une variable
load_dotenv(find_dotenv())
bot_token = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()
client = commands.Bot(command_prefix="$", intents = intents)

# Commandes -------------------------------------------------------------------------------------------------------------------------
@client.command(name="cmd")
async def commandes(message):
    await message.channel.send("""
```markdown
# Liste des commandes:

  - $cmd: renvoie la liste des commandes
  - $val: renvoie la liste des valeurs principales.
  - $ind: renvoie la liste des principaux indicateurs:
  
  
  - $test arg1: renvoie "test" et l'argument placer en paramètre
  - $img: renvoie une image
  - $plot crypto indicateur: renvoie "Voici un graphique de "crypto" avec l'"indicateur"."
  
```
""")
    
@client.command(name="val")
async def crypto(message):
    await message.channel.send("""
```markdown
# Liste des principals valeurs:

  - SPX: S&P500, 500 entreprise coté en bourse au Etats-Unis
  - CAC: CAC40, les 40 plus grandes entreprises françaises
  - NDQ: NASDAQ, 100 entreprise coté en bourse au Etats-Unis

  - BTCUSD: Bitcoin / U.S Dollard
  - BTCEUR: Bitcoin / Euro
  - ETHUSD: Etherum / U.S Dollard
  - BNBUSD: Binance coin / U.S Dollard

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
    
@client.command(name="ind")
async def indicateurs(message):
    await message.channel.send("""
```markdown
# Liste des principaux indicateurs:

  - rsi: Relative Strength Index
  - stoch: Stochastique %K
  - macd: Convergence Divergence Moyenne Mobile (macd, macd_signal, macd_diff(bar-plot))
  - boll: Bollinger Bands
  - mm: moyenne mobile
  
```
""")
    
@client.command(name="tf")
async def time_frame(message):
    await message.channel.send("""
```markdown
# Liste des unitées de temps:

  - 1m: 1 minute
  - 3m: 3 minutes
  - 5m: 5 minutes
  - 15m: 15 minutes
  - 30m: 30 minutes
  - 45m: 45 minutes
  - 1h: 1 heure
  - 2h: 2 heures
  - 3h: 3 heures
  - 4h: 4 heures
  - 1d: 1 journée
  - 1w: 1 semaine
  - 1M: 1 mois
  
```
""")
  
  



@client.command(name="plot")
async def plot(message, val, ind, tf):
  # Creation d'un channel perso pour envoyer les graphiques.
  guild = message.guild
  name = str(message.author) + "_plots"
  is_already_create = False
  
  # On regarde si l'auteur du message possède déja un channel privé pour ces graphiques.
  # pour ne pas polluer le channel général.
  for channel in guild.channels:
    if channel.name == name:
      is_already_create = True

  # Sinon on lui en créer un
  if is_already_create == False:
    overwrites = { # définition des permissions. faire en sort que ce channel soit privé.
      guild.default_role: discord.PermissionOverwrite(read_messages=False),
      guild.me: discord.PermissionOverwrite(read_messages=True),
      message.author: discord.PermissionOverwrite(read_messages=True)
    }
    await guild.create_text_channel(name, overwrites=overwrites)
    await message.send(f"Vous pouvez retrouver vos graphiques dans le salon textuel {name[0].upper() + name[1:]}")
  
  channel = discord.utils.get(guild.channels, name=name) # Récupération du channel lié à l'auteur du message
  await channel.send(f"Je suis en train de créer votre graphique")
  
  # récupération de l'echange
  data = tv.search_symbol(text=val)
  # Recupération de l'unité de temps
  time_frame = utils.get_time_frame(tf=tf, Interval=Interval)
  # Récupération des données et mise en forme.
  crypto = tv.get_hist(symbol=val.upper(), exchange=data[0]["exchange"].upper(), interval=Interval.in_daily, n_bars=10_000)
  df = pd.DataFrame(crypto)
  del df['symbol']
  df = utils.get_indicator(df=df, ind=ind.lower())
  
  # Création du graphique
  utils.create_plot(df, ind.lower(), str(message.author) + "_plot.png")

  # Envoie du graphique fini dans le channel correspondant.
  await channel.send(f"Voici un graphique de {val} avec le {ind} sur {tf}.")
  await channel.send(file=discord.File(str(message.author) + "_plot.png"))
  os.remove(str(message.author) + "_plot.png")

  

# Test de commande -----------------------------------------------------------------------------------
@client.command(name="delete")
async def delete(message):
  # await message.send(message.guild.me)
  for channel in message.guild.channels:
    if isinstance(channel, discord.TextChannel):
      await message.send(f"The channel {channel} is instance")
      # if channel.permissions_for(message.author).send_messages:
      #   channel_used = channel
      #   break

@client.command(name="test")
async def test(message, *args):
  await message.channel.send("test")
  arguments = ', '.join(args)
  await message.channel.send(f'{len(args)} arguments: {arguments}')
  await message.channel.send(args)
  try:
    await message.channel.send(args[0].upper())
  except:
    await message.channel.send("Aucun argument donné")


@client.command(name="img")
async def test(message):
  await message.channel.send(file=discord.File('img.png'))
  
  
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

  # # On gère les contenue des messages
  # message.content = message.content.lower()

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