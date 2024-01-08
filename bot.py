import discord
from discord.ext import commands
import os
from dotenv import load_dotenv , find_dotenv
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import hashlib
from outils import arbre, graph, hashmap, liste # mes propres fichiers

# Initialisation des objets ----------------------------------------------------------------------------------------------------------------------
historique = liste.ChainedList() # historique générale du bot
hist_users = hashmap.HashMap(10) # Hashmap contenant les historiques personnel des utilisateurs. [[('username', liste.ChainedList()]] 
# Je ne pense pas avoir plus d'une dizaine personnes sur mon server.
hash_key = {} # indice de l'historique personnel. 'username': indice(int). 
hashage = hashlib.sha256() # hash utiliser pour recupérer l'indice de la hashmap ou mettre l'historique personnel  
tv = TvDatafeed() # création de la connection à Tradingview.

# Récuper le .env et stocker le token dans une variable
load_dotenv(find_dotenv())
bot_token = os.getenv('BOT_TOKEN')

# Création du lien avec discord
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents = intents)

# Permet d'ajouter les commandes au historiques
def ajout_historiques(auteur, commande):
  # historique générale
  historique.append(commande) # ajout de la commande à l'historique générale
  
  # historique perso
  hist_perso = hist_users.get(auteur, hash_key[auteur]) # récupération de l'historique personnel
  # ajout de la commande:
  if hist_perso is None: 
    hist_perso = liste.ChainedList()
    hist_perso.append(commande)
  else:
    hist_perso.append(commande)
  
# Commandes -------------------------------------------------------------------------------------------------------------------------

# cf readmme.md pour l'explication des fonctions

@client.command(name="cmd")
async def commandes(message):
  ajout_historiques(str(message.author), "!cmd") # ajout de la commandes aux historiques
  await message.channel.send("""
```markdown
# Liste des commandes:

  - !last: renvoie la dernière commande entrée
  - !empty: vide entièrement l'historique des commandes du bot
  - !empty_user: vide entièrement l'historique de vos commandes
  
  - !cmd: renvoie la liste des commandes
  - !cmd_user: renvoie l'historique de vos propre commande. Vous n'avez pas accès à l'historique des autres.
  
  - !val: renvoie la liste des valeurs principales.
  - !ind: renvoie la liste des indicateurs disponible dans le bot.
  - !tf: renvoie la liste des unitées de temps disponibles dans le bot.
  
  - !plot: renvoie un graphique (val, tf).
  - !plot_ind: renvoie un graphique avec un indicateur technique (val, ind, tf).
```
""")
  
@client.command(name="cmd_user")
async def commandes_utilisateur(message):
  hist_perso = hist_users.get(str(message.author), hash_key[str(message.author)]) # récupération de l'historique personnel
  str_hist = hist_perso.to_str() # transformation en chaine de caractère
  # Envoie de l'historique
  if str_hist == "Vide":
    await message.channel.send("Vous n'avez pas encore entrez de commande")
  else:
    await message.channel.send("Voici l'historique de vos commandes:")
    await message.channel.send(str_hist)
  ajout_historiques(str(message.author), "!cmd_user") # ajout de la commandes aux historiques
    
@client.command(name="val")
async def crypto(message):
  ajout_historiques(str(message.author), "!val") # ajout de la commandes aux historiques
  await message.channel.send("""
```markdown
# Liste des principals valeurs:

Indices:
  - SPX: S&P500, 500 entreprise coté en bourse au Etats-Unis
  - CAC: CAC40, les 40 plus grandes entreprises françaises
  - NDQ: NASDAQ, 100 entreprise coté en bourse au Etats-Unis

Cryptomonnaies:
  - BTCUSD: Bitcoin / U.S Dollard
  - BTCEUR: Bitcoin / Euro
  - ETHUSD: Etherum / U.S Dollard
  - BNBUSD: Binance coin / U.S Dollard

Actions:
  - AAPL: Apple
  - TSLA: Tesla
  - NFLX: Netflix
  - MSFT: Microsoft corp
  - GOOG: Google
  - AMZN: Amazon
  - META: Meta
  
Forex:
  - USOIL: le Pétrole
  - GOLD: l'Or
  - SILVER: l'Argent
  
```
""")
    
@client.command(name="ind")
async def indicateurs(message):
  ajout_historiques(str(message.author), "!ind") # ajout de la commandes aux historiques
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
  ajout_historiques(str(message.author), "!tf") # ajout de la commandes aux historiques
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
  if historique.length == 0: # On vérifie si l'historique est vide
    await message.channel.send(f"Aucune commande n'a encore été entrée")
  else: # sinon on l'envoie dans le canal de discution
    await message.channel.send(f"Voici la dernière commande entrée par un utilisateur: {historique.get(historique.length - 1)}")
  ajout_historiques(str(message.author), "!last") # ajout de la commandes aux historiques

@client.command(name="empty")
async def vider(message):
  ajout_historiques(str(message.author), "!empty") # ajout de la commandes aux historiques
  historique.empty() # Puis on vide l'historique du bot (historique générale)
  await message.channel.send("L'historique générale du bot à été vider!")

@client.command(name="empty_user")
async def vider(message):
  ajout_historiques(str(message.author), "!empty_user") # ajout de la commandes aux historiques
  # On vide l'historique personnel de l'utilisateur
  hist_users.empty(str(message.author), liste.ChainedList(), hash_key[str(message.author)]) 
  await message.channel.send("Votre historique personnel à bien été vider!")
  
@client.command(name="plot")
async def plot(message, val, tf):
  # Creation d'un channel perso pour envoyer les graphiques. Pour ne pas polluer les cannaux généraux.
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
      guild.default_role: discord.PermissionOverwrite(read_messages=False), # Les autre
      guild.me: discord.PermissionOverwrite(read_messages=True), # Le bot
      message.author: discord.PermissionOverwrite(read_messages=True) # l'auteur du message
    }
    await guild.create_text_channel(name, overwrites=overwrites) # création du canal
    await message.send(f"Vous pouvez retrouver vos graphiques dans le salon textuel {name[0].upper() + name[1:]}")
  
  channel = discord.utils.get(guild.channels, name=name) # Récupération du canal lié à l'auteur du message
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
  except:
    await channel.send("L'un des paramètres entrer n'est pas correct!")
    return # On arrête la fonction
  
  try:
    # Création du graphique
    graph.simple_plot(df, str(message.author) + "_plot.png", val=val.upper())
    
    # Envoie du graphique fini dans le channel correspondant.
    await channel.send(f"Voici un graphique de {val} sur {tf}.")
    await channel.send(file=discord.File(str(message.author) + "_plot.png"))
    os.remove(str(message.author) + "_plot.png") # on supprime la photo du graphique
    
    # On ajoute la commande aux historiques seulement si elle fonctionne.
    ajout_historiques(str(message.author), "!plot" + " " + val +  " " +  tf)
  except:
    return # on arrête la fonction
    print("problème avec le graphique")
  
@client.command(name="plot_ind")
async def plot_ind(message, val, ind, tf):
  # Creation d'un channel perso pour envoyer les graphiques. Pour ne pas polluer les cannaux généraux.
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
    overwrites = { # définition des permissions. faire en sort que ce canal soit privé.
      guild.default_role: discord.PermissionOverwrite(read_messages=False), # Les autres
      guild.me: discord.PermissionOverwrite(read_messages=True), # Le bot
      message.author: discord.PermissionOverwrite(read_messages=True) # L'auteur du message
    }
    await guild.create_text_channel(name, overwrites=overwrites) # création du canal
    await message.send(f"Vous pouvez retrouver vos graphiques dans le salon textuel {name[0].upper() + name[1:]}")
  
  channel = discord.utils.get(guild.channels, name=name) # Récupération du canal lié à l'auteur du message
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
    os.remove(str(message.author) + "_plot.png") # on supprime la photo du graphique
    
    # On ajout la commande aux historiques seulement si elle fonctionne.
    ajout_historiques(str(message.author), "!plot" + " " + val + " " +  ind + " " +  tf)
  except:
    print("problème avec le graphique")

# Events ---------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_ready(): # que faire quand le bot est près à l'emploi ?
  # Création des historiques personnels des membres déjà présents
  for guild in client.guilds: # Pour tous les servers ou le bot est présent 
    for member in guild.members: # Pour tous les membres
      hashage.update(str.encode(member.name)) # hashage du nom d'utilisateur
      index = int(hashage.hexdigest(), 16) % 10 # récupération de l'indice de ou sera stocker son historique personnel
      hash_key[member.name] = index # ajout de l'indice dans le dictionnaire.
      hist_users.add_key_value(member.name , liste.ChainedList(), index) # création de l'historique
  print("Le bot est prêt !") # Le démarrage du bot à bien été éfféctuer.

@client.event
async def on_member_join(member): # quand un nouveau membre rejoind le server
  general_channel = client.get_channel(1167398798469906434) # récupération du canal général
  hashage.update(str.encode(member.name)) # hashage du nom d'utilisateur
  index = int(hashage.hexdigest(), 16) % 10 # récupération de l'indice de ou sera stocker son historique personnel
  hash_key[str(member.name)] = index # ajout de l'indice dans le dictionnaire.
  hist_users.add_key_value(str(member.name), liste.ChainedList(), index) # création de l'historique personnel du nouvel arrivant
  await general_channel.send("Bienvenue sur le serveur "+ member.name  + " !") # petit message de bienvenue.
  
@client.event
async def on_message(message):
  
  # Permet au bot de ne pas ce parler à lui même
  # print(message.content)
  if message.author == client.user:
    return

  # On gère les contenue des messages
  message.content = message.content.lower()

  # permet de les touver si le message envoyer est une commande
  # permet de faire fonctionner les commande
  await client.process_commands(message)
     
# Lancement du bot ------------------------------------------------------------------------------------------------------------------------
client.run(bot_token)