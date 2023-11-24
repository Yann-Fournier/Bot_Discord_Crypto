import sys
sys.path.append('./')
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv , find_dotenv
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
from outils import arbre, graph, hashmap, liste # mes propres fichiers

# Initialisation ----------------------------------------------------------------------------------------------------------------------
# Objets
historique = liste.ChainedList()
hist_users = hashmap.HashMap(10) # Je ne pense pas avoir plus d'une dizaine personnes sur mon server.
# discussion = arbre.

hist_users.add_key_value("ryulgc", liste.ChainedList())
hist_users.add_key_value("patchouf", liste.ChainedList())
hist_users.add_key_value("koliwki", liste.ChainedList())


tv = TvDatafeed() # création de la connection à Tradingview.

# Récuper le .env et stocker le token dans une variable
load_dotenv(find_dotenv())
bot_token = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()
client = commands.Bot(command_prefix="$", intents = intents)

# Commandes -------------------------------------------------------------------------------------------------------------------------
@client.command(name="cmd")
async def commandes(message):
  historique.append("$cmd")
  print(str(message.author))
  perso = hist_users.get(str(message.author))
  perso.append("$cmd")
  hist_users.add_key_value(str(message.author), perso)
  print(hist_users)
  # print(historique)
  await message.channel.send("""
```markdown
# Liste des commandes:

  - $last: renvoie la dernière commande entrée
  - $vider: vide entièrement l'historique des commandes
  
  - $cmd: renvoie la liste des commandes
  - $cmd_user: renvoie l'historique des commandes d'un utilisateur $$$$$$$$$
  
  - $val: renvoie la liste des valeurs principales.
  - $ind: renvoie la liste des principaux indicateurs:
  - $tf: renvoie la liste des périodes disponibles
```
""")
    
@client.command(name="val")
async def crypto(message):
  historique.append("$val")
  print(hist_users.get(str(message.author)))
  # print(historique)
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
  historique.append("$ind")
  # print(historique)
  await message.channel.send("""
```markdown
# Liste des principaux indicateurs:

  - rsi: Relative Strength Index
  - stoch: Stochastique %K
  - macd: Convergence Divergence Moyenne Mobile (macd, macd_signal, macd_diff(bar-plot))
  - boll: Bollinger Bands
  - mm: moyenne mobile (moving average)
  
```
""")
    
@client.command(name="tf")
async def time_frame(message):
  historique.append("$tf")
  # print(historique)
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

@client.command(name="last")
async def last(message):
  if historique.length == 0:
    await message.channel.send(f"Aucune commande n'a encore été entrée")
  else:
    await message.channel.send(f"Voici la dernière commande entrée par un utilisateur: {historique.get(historique.length - 1)}")
  historique.append("$last")
  # print(historique)
  
@client.command(name="vider")
async def vider(message):
  historique.empty()
  # print(historique)

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
  
  try:
    # récupération de l'echange
    data = tv.search_symbol(text=val)
    # Recupération de l'unité de temps
    time_frame = graph.get_time_frame(tf=tf, Interval=Interval)
    # Récupération des données et mise en forme.
    crypto = tv.get_hist(symbol=val.upper(), exchange=data[0]["exchange"].upper(), interval=time_frame, n_bars=10_000)
    df = pd.DataFrame(crypto)
    del df['symbol']
    df = graph.get_indicator(df=df, ind=ind.lower())
  except:
    await channel.send("L'un des paramètres entrer n'est pas correct!")
  
  try:
    # Création du graphique
    graph.create_plot(df, ind.lower(), str(message.author) + "_plot.png", val=val.upper())

    # Envoie du graphique fini dans le channel correspondant.
    await channel.send(f"Voici un graphique de {val} avec le {ind} sur {tf}.")
    await channel.send(file=discord.File(str(message.author) + "_plot.png"))
    os.remove(str(message.author) + "_plot.png")
    
    # On ajout la commande seulement si elle fonctionne.
    historique.append("$plot" + " " + val + " " +  ind + " " +  tf)
    # print(historique)
  except:
    print("problème avec le graphique")

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
  hist_users.add_key_value(str(member.name), liste.ChainedList()) # création d'un historique perso pour chaque nouvel arrivant.
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