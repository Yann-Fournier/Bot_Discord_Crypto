# Bot Discord Trading Plot

Ce bot à été créer dans le cadre d'un projet pour mon école.\
\
Il vous permet de créer des graphiques en bougie japonnaise retraçant l'historique d'une action, d'une cryptomonnaie ou autre. Vous avez également la possibilité d'ajouter au graphique un indicateur technique. Ce graphique sera envoyer dans un salon textuel privé avec votre nom d'utilisateur suivi de "_plots". 

> Le bot récupère les données sur TradingView. N'hésitez pas à vous renseigner sur le nom d'une cryptomonnaie ou d'une action sur [TradingView](https://fr.tradingview.com/). Sinon, vous trouverez des exemples d'actions et autre et d'indicateur avec les commandes du bot.

## Configuration
Changer ``.env.exemple`` en ``.env`` et insérer le token de votre bot discord entre les apostrophes.

## Documentation

Toutes les commandes doivent être précédée du signe `!` pour fonctionner.

```
Exemple:
    - !last
    - !plot val tf
    - !cmd_user
    - !plot_ind val ind tf
```

### Commnades :
- [cmd](#cmd)
- [last](#last)
- [empty](#empty)
- [empty_user](#empty_user)
- [cmd_user](#cmd_user)
- [val](#val)
- [ind](#ind)
- [tf](#tf)
- [plot](#plot)
- [plot_ind](#plot_ind)

#### cmd
    Permet de voir la liste des commandes disponibles.

#### last
    Permet de voir la dernière commande entrée dans le bot.

#### empty
    Permet de vider enitèrement l'historique du bot (historique général).

#### empty_user
    Permet de vider entièrement l'historique de vos commandes (historique personnel).

#### cmd_user
    Permet de voir l'histoique de vos commandes (historique personnel).

#### val
    Permet de voir une liste non exhaustive d'action ou de cryptomonnaie et autre utilisable dans le bot.  

#### ind
    Permet de voir la liste des indicateurs pris en compte par le bot. 

#### tf
    Permet de voir la liste des périodes de temps pris en compte par le bot (tf = timeframe).

#### plot
    Permet de créer le graphique qui vous intéresse.
    Cette commande prend deux paramètre: l'action ou autre (val) puis la période de temps (tf).

#### plot_ind
    Permet de créer le graphique qui vous intéresse avec un indicateur.
    Cette commande prend trois paramètre: l'action ou autre (val), l'indicateur (ind) puis la période de temps (tf).
