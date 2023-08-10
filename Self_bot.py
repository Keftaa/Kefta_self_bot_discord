# ------------------------------------------------------------------------
# Filename   : self_bot.py
# Description: Self bot développé par Kefta.
# Author     : Kefta
# Website    : https://github.com/Keftaa/Kefta_self_bot_discord
# Version    : 1.2
# Date       : 10/08/2023
# ------------------------------------------------------------------------
import discord
from discord.ext import commands
import asyncio
import os
import datetime
import random
import fade
import datetime
from babel.dates import format_date
from googletrans import Translator

bot = commands.Bot(command_prefix='-',self_bot=True, help_command=None)
snipe_message_author = {}
snipe_message_content = {}
snipe_message_deletion_time = {}
start_time = datetime.datetime.utcnow()
KEFTA_GIF_URL = "https://cdn.discordapp.com/attachments/1137948255653728367/1137948351564890112/replace.gif"

categorized_commands = {
    'Utilitaire': ['ping', 'snipe', 'clear','avatar', 'banner','arabe','anglais','uptime'],
    'Admin commande': ['stealallpdp','savegrp','savedm'],
    'Troll': ['dicksize', 'gay', 'coinflip', 'iq', 'datemort', 'lgbt', 'sexcall', 'tamerelapute','hack','fakeaudio'], 
    'NFSW': ['cum'],
    'Paramétres': ['setprefix','cls']
}

def get_token():
    with open('token.txt') as f:
        return f.read().strip()
TOKEN = get_token()

def Dump(ctx):
    if ctx.guild is None:
        ctx.send("Cette commande ne peut être exécutée que dans un serveur.")
        return
    
    with open(f'Images/{ctx.guild.id}-Dump.txt', 'a+') as f:
        for member in ctx.guild.members:
            avatar_url= member.avatar
            f.write(str(avatar_url) + '\n')
            


@bot.event
async def on_ready():
    os.system('cls')
    print(fade.purpleblue(f"""
                 __  __     ______     ______   ______   ______    
                /\ \/ /    /\  ___\   /\  ___\ /\__  _\ /\  __ \   
                \ \  _"-.  \ \  __\   \ \  __\ \/_/\ \/ \ \  __ \  
                 \ \_\ \_\  \ \_____\  \ \_\      \ \_\  \ \_\ \_\ 
                  \/_/\/_/   \/_____/   \/_/       \/_/   \/_/\/_/ """))
    print(fade.purpleblue(f"""┌────────────────────────────────────────────────────────────────────────────────────────┐"""))
    print(fade.purpleblue(f"                                Kefte Self bot - by Kefta"))
    print(fade.purpleblue(f"                         Connected: {bot.user.name}#{bot.user.discriminator} | Servers: {len(bot.guilds)}"))
    print(fade.purpleblue(f"""└────────────────────────────────────────────────────────────────────────────────────────┘"""))

async def send_kefta_gif(ctx, delete_after=5):
    await ctx.send(KEFTA_GIF_URL, delete_after=delete_after)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.HTTPException):
        if error.code == 429:  # Erreur de rate limit
            retry_after = error.retry_after
            await ctx.send(f"Erreur de rate limit. Réessayer après {retry_after:.2f} secondes.")
            await asyncio.sleep(retry_after)
            await ctx.reinvoke()
    else:
        raise error
    
@bot.event
async def on_message_delete(message):
    channel_id = message.channel.id
    snipe_message_author.pop(channel_id, None)
    snipe_message_content.pop(channel_id, None)
    snipe_message_deletion_time.pop(channel_id, None)

    snipe_message_author[channel_id] = message.author
    snipe_message_content[channel_id] = message.content
    snipe_message_deletion_time[channel_id] = message.created_at

    await asyncio.sleep(30)

    snipe_message_author.pop(message.channel.id, None)
    snipe_message_content.pop(message.channel.id, None)

@bot.command(name='ping', help='Affiche la latence du bot',category='Utilitaire')
async def ping(ctx):
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    latency = (end_time - start_time).microseconds / 1000
    bot_latency = round(bot.latency * 1000, 2)
    await ctx.send(content=f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Pong_**:star:\n\nPong! Latence du bot : {bot_latency} ms, Latence du message : {latency} ms",delete_after=5)
    await ctx.message.delete()

@bot.command(name='stealallpdp',help='Permet de récuperer toute les pp d\'un server')
async def steal_all_pdp(ctx):
    await ctx.message.delete()
    Dump(ctx)
    await ctx.send('Finis !')


@bot.command(name='clearimages', help='Efface tous les fichiers du dossier Images')
async def clear_images(ctx):
    await ctx.send("Êtes-vous sûr de vouloir supprimer tous les fichiers du dossier Images ? Répondez avec 'oui' ou 'non'.",delete_after=5)

    def check(response):
        return response.author == ctx.author and response.channel == ctx.channel

    try:
        response = await bot.wait_for('message', timeout=15, check=check)

        if response.content.lower() == 'oui':
            folder = 'Images'
            file_list = [f for f in os.listdir(folder)]
            
            if file_list:
                for file_name in file_list:
                    file_path = os.path.join(folder, file_name)
                    os.remove(file_path)
                await ctx.send("Tous les fichiers ont été supprimés avec succès.",delete_after=5)
            else:
                await ctx.send("Le dossier Images est déjà vide.",delete_after=5)
        else:
            await ctx.send("Opération annulée.",delete_after=5)
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé. Opération annulée.",delete_after=5)

@bot.command(name='uptime',help='Permet de savoir depuis quand le bot est en ligne')
async def uptime(ctx):
    await ctx.message.delete()
    uptime = datetime.datetime.utcnow() - start_time
    uptime = str(uptime).split('.')[0]
    await ctx.send(f'`'+uptime+'`')


@bot.command(name= 'snipe', help='Permet de voir le dernier message supprimé du salon',category='Utilitaire')
async def snipe(ctx):
    channel_id = ctx.channel.id
    author = snipe_message_author.get(channel_id)
    content = snipe_message_content.get(channel_id)
    deletion_time = snipe_message_deletion_time.get(channel_id)

    if author and content and deletion_time:
        if isinstance(ctx.channel, discord.TextChannel):
            channel_name = f"#{ctx.channel.name}"
        else:
            channel_name = "a DM"
        
        message = (
            f"**Kefta Snipe**:\n\n"
            f"Dernier message envoyé dans {channel_name} est :\n"
            f"Contenu: {content}\n"
            f"Envoyé par **{author}**\n"
            f"Supprimé le: {deletion_time}"
        )
        await ctx.send(message, delete_after=10)
    else:
        await ctx.send("Pas de message récent supprimé ici.")
    await ctx.message.delete()

@bot.command(name='cls',help='Clear la console')
async def cls(ctx):
    await ctx.message.delete()
    os.system('cls')
    await ctx.send('Console clear !',delete_after=3)

@bot.command(name='arabe',help='Traduit un texte en arabe',category='Utilitaire')
async def arabe(ctx, *, texte):
    translator = Translator()
    translation = translator.translate(texte, src='fr', dest='ar')
    translated_text = translation.text
    await ctx.send(f'{translated_text}')
    await ctx.message.delete()

@bot.command(name='anglais',help='Traduit un texte en arabe',category='Utilitaire')
async def anglais(ctx, *, texte):
    translator = Translator()
    translation = translator.translate(texte, src='fr', dest='en')
    translated_text = translation.text
    await ctx.send(f'{translated_text}')
    await ctx.message.delete()


#######################################Troll commands################################################

@bot.command(name='fakeaudio',help='Envoie un faux message vocal',category='Troll')
async def fakeaudio(ctx):
    await ctx.message.delete()
    audio= "https://cdn.discordapp.com/attachments/1137948255653728367/1139185795371106406/ED6EFBC5-A68E-48C6-9103-B123B1ECC22D.gif"
    try:
        await ctx.send(f'{audio}',delete_after=10)
    except discord.HTTPException as e:
        await ctx.send('Les images sont lock ici',delete_after=5)


@bot.command(name='dicksize', help='Affiche aléatoirement la taille d\'un pénis.',category='Troll')
async def dicksize(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    size = '=' * random.randint(1, 20)
    message = f"```ini\n{member.display_name} taille de son zgeg\n\n8{size}D```"
    await ctx.send(message,delete_after=10)
    await ctx.message.delete()


@bot.command(name='gay',help='Permet de calculer l\'homosexualité d\'une personne.',category='Troll')
async def gay(ctx, *, member: discord.Member = None):
    if member is None:
        member = ctx.author
    homosexuality_percentage = random.randint(0, 100)
    message = f"{member.mention} est `{homosexuality_percentage}%` gay :rainbow_flag:"
    await ctx.send(message,delete_after=10)
    await ctx.message.delete()

@bot.command(name='coinflip', help='Effectue un lancer de pièce (pile ou face)',category='Troll')
async def coinflip(ctx):
    result = random.choice(['Pile', 'Face'])
    await ctx.send(f"{ctx.author.mention} a lancé une pièce et obtenu : `{result}`",delete_after=10)
    await ctx.message.delete()

@bot.command(name="tamerelapute",help="Pour savoir si la mère d'une personne est une pute ou non",category='Troll')
async def tamerelapute(ctx,*, member: discord.Member = None):
    if member is None:
        member = ctx.author
    result = random.choice(['pute !', 'mère charitable !'])
    await ctx.send(f"La mère de {member.mention} une **{result}**",delete_after=10)
    await ctx.message.delete()


@bot.command(name='iq', help='Donne un QI aléatoire à une personne',category='Troll')
async def iq(ctx, *, member: discord.Member = None):
    if member is None:
        member = ctx.author
    iq_score = random.randint(3, 200)
    await ctx.send(f"{member.mention} a un QI de `{iq_score}`",delete_after=10)
    await ctx.message.delete()
    
@bot.command(name='datemort',help='Prédit la date de mort d\'une personne.',category='Troll')
async def datemort(ctx, *, member: discord.Member):
    if member != ctx.author:
        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        max_years = 70
        random_days = random.randint(2, max_years * 365)
        death_date = today + random_days * one_day

        if death_date == today:
            death_date += one_day
        elif death_date == today - one_day:
            death_date += 2 * one_day

        formatted_death_date = format_date(death_date, format='full', locale='fr_FR')
        prediction_message = f"La date de la mort de {member.mention} est le: `{formatted_death_date}`"
        await ctx.send(prediction_message,delete_after=10)
    else:
        await ctx.send("Tu peux pas prédire ta propre mort débile.",delete_after=10)
    await ctx.message.delete()

@bot.command(name='lgbt', help='Rajoute des drapeau LGBT partout',category='Troll')
async def lgbt(ctx, *, message: str):
    kefta = ':rainbow_flag:'.join(message)
    await ctx.send(kefta)
    await ctx.message.delete()

@bot.command(help="Permet de trouver une sexcalleuse",name="sexcall",category='Troll')
async def sexcall(ctx,user_id: int):
    await ctx.message.delete()
    await ctx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Sexcalleuse_**:star:\n\nEn recherche d'une sexcalleuse dans les environs...", delete_after=5)
    await asyncio.sleep(5)
    message = await ctx.send("Recherche en cours...")
    await asyncio.sleep(1)
    await message.edit(content="Recherche en cours..")
    await asyncio.sleep(1)
    await message.edit(content="Recherche en cours.")
    await asyncio.sleep(1)
    await message.edit(content="Recherche en cours..")
    await asyncio.sleep(1)
    await message.edit(content="Recherche en cours...")
    await message.delete()
    await ctx.send(f"Sexcalleuse trouvé son profil <@{user_id}>",delete_after=10)

@bot.command(help="Permet d'éjaculer",name='cum')
async def cum(ctx):
    await ctx.message.delete()
    message = await ctx.send('''
            :ok_hand:            :smile:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant:''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :smiley:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:  
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :grimacing:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant:  
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :persevere:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:   
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :confounded:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant: 
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :tired_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:    
             ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :weary:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:= D:sweat_drops:
             :trumpet:      :eggplant:        
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :dizzy_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :drooling_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''',delete_after=10)

@bot.command(help='Hack un compte',name='hack')
async def hack(ctx, user: discord.Member=None):
    await ctx.message.delete()
    gender = ["Homme", "Femme", "Trans", "Autre", "Retard"]
    age = str(random.randrange(10, 25))
    height = ['4\'6"', '4\'7"', '4\'8"', '4\'9"', '4\'10"', '4\'11"', '5\'0"', '5\'1"', '5\'2"', '5\'3"',
            '5\'4"', '5\'5"',
            '5\'6"', '5\'7"', '5\'8"', '5\'9"', '5\'10"', '5\'11"', '6\'0"', '6\'1"', '6\'2"', '6\'3"',
            '6\'4"', '6\'5"',
            '6\'6"', '6\'7"', '6\'8"', '6\'9"', '6\'10"', '6\'11"']
    weight = str(random.randrange(60, 300))
    hair_color = ["Noir", "Brun", "Blond", "Blanc", "Gris", "Rouge"]
    skin_color = ["Blanc", "Pâle", "Brun", "Noir", "Peau claire"]
    religion = ["Chrétien", "Musulman", "Athée", "Hindou", "Bouddhiste", "Juif"]
    sexuality = ["Hétérosexuel", "Gay", "Homo", "Bi", "Bi-Sexuel", "Lesbienne", "Pansexuel"]
    education = ["École secondaire", "Collège", "École intermédiaire", "École primaire", "École maternelle",
                "Retard n'est jamais allé à l'école LOL"]
    ethnicity = ["Blanc", "Afro-Américain", "Asiatique", "Latino", "Latina", "Américain", "Mexicain", "Coréen", "Chinois",
                "Arabe", "Italien", "Porto-Ricain", "Non hispanique", "Russe", "Canadien", "Européen", "Indien"]
    occupation = ["Retard n'a pas d'emploi LOL", "Retard certifié de Discord", "Agent d'entretien", "Agent de police", "Enseignant",
                "Caissier", "Commis", "Serveur", "Serveuse", "Emballeur d'épicerie", "Détailleur", "Vendeur", "Artiste",
                "Chanteur", "Rappeur", "Trappeur", "Voyou de Discord", "Gangster", "Empaqueteur de Discord", "Mécanicien", "Menuisier",
                "Électricien", "Avocat", "Docteur", "Programmeur", "Ingénieur en logiciel", "Scientifique"]
    salary = ["Retard ne gagne pas d'argent LOL", "$" + str(random.randrange(0, 1000)), '<50 000€', '<75 000€', "100 000€",
            "€125 000", "150 000€", "175 000€",
            "200 000€+"]
    location = ["Retard vit dans le sous-sol de sa mère LOL", "France", "Paris", "Marseille", "Lyon", "Toulouse", "Bordeaux",
            "Lille", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lyon", "Nantes", "Toulouse",
            "Lille", "Rennes", "Le Havre", "Reims", "Cergy-Pontoise", "Saint-Étienne", "Toulon", "Angers", "Grenoble",
            "Dijon", "Nîmes", "Aix-en-Provence", "Saint-Quentin-en-Yvelines", "Brest", "Le Mans", "Amiens", "Limoges",
            "Tours", "Clermont-Ferrand", "Villeurbanne", "Besançon", "Orléans", "Mulhouse", "Caen", "Nancy",
            "Saint-Denis", "Rouen", "Avignon", "Nanterre", "Poitiers", "Vitry-sur-Seine", "Créteil", "Aulnay-sous-Bois",
            "Versailles", "Pau", "Colombes", "La Rochelle"]
    email = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com", "@protonmail.com", "@disposablemail.com",
            "@aol.com", "@edu.com", "@icloud.com", "@gmx.net", "@yandex.com"]
    dob = f'{random.randrange(1, 32)}/{random.randrange(1, 13)}/{random.randrange(1950, 2021)}'
    name = ['Alexis Fontaine', 'Pierre Dupont', 'Antoine Durand', 'Louis Pollet', 'Johan Picard', 'Léonard Caudron', 'Gabriel Brunet', 'Hugo Vincent', 'Léon Boé', 'Arsène Royer',
        'Côme Pollet', 'Achille Boyer', 'Hector Morel', 'Félix Bourhis', 'Alexis Clavel', 'Charles Moulin', 'Auguste Mercier', 'Léandre Boé', 'Nathan Roussel', 'Noé Duval',
        'Zoé Derambure', 'Salomé Derambure', 'Célestine Roux', 'Ambre Fortin', 'Aurore Roy', 'Sophie Jean', 'Suzanne Lenne', 'Mathilde Mercier', 'Mélina Coolen', 'Céleste Boé',
        'Florian Durand', 'Manon da Silva', 'Ninon Fretigny', 'Olivia Brun', 'Célestine Huart', 'Augustine Lenne', 'Maeva Mauvieux', 'Augustine Bertrand', 'Charline Baron', 'Manon Garnier']
    phone = f'07.{"%02d.%02d.%02d.%02d" % (random.randint(0, 99), random.randint(0, 99), random.randint(0, 99), random.randint(0, 99))}'
    if user is None:
        user = ctx.author
        password = ['motdepasse', '123', 'monmotdepasseestmotdepasse', user.name + "estcool123", user.name + "estpapa",
                    "papa" + user.name, "jaimediscord", "j<3discord", "furryporn456", "secret", "123456789", "pomme49",
                    "redskins32", "princesse", "dragon", "motdepasse1", "1q2w3e4r", "jaimelesfurries"]
        message = await ctx.send(f"`Piratage de {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Piratage de {user}...\nPiratage dans le réseau principal...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Piratage de {user}...\nPiratage dans le réseau principal...\nMise en cache des données...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Piratage de {user}...\nPiratage dans le réseau principal...\nMise en cache des données...\nDécodage des informations du SSN...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Piratage de {user}...\nPiratage dans le réseau principal...\nMise en cache des données...\nDécodage des informations du SSN...\nForçage des détails de la vie amoureuse...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Piratage de {user}...\nPiratage dans le réseau principal...\nMise en cache des données...\nDécodage des informations du SSN...\nForçage des détails de la vie amoureuse...\nFinalisation des détails de la vie du dossier sur la durée de vie\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"```Piratage réussi de {user}\nNom : {random.choice(name)}\nGenre : {random.choice(gender)}\nÂge : {age}\nTaille : {random.choice(height)}\nPoids : {weight}\nCouleur des cheveux : {random.choice(hair_color)}\nCouleur de la peau : {random.choice(skin_color)}\nDate de naissance : {dob}\nEmplacement : {random.choice(location)}\nTéléphone : {phone}\nE-mail : {user.name + random.choice(email)}\nMots de passe : {random.choices(password, k=3)}\nProfession : {random.choice(occupation)}\nSalaire annuel : {random.choice(salary)}\nEthnicité : {random.choice(ethnicity)}\nReligion : {random.choice(religion)}\nSexualité : {random.choice(sexuality)}\nÉducation : {random.choice(education)}```")
    else:
        password = ['motdepasse', '123', 'monmotdepasseestmotdepasse', user.name + "estcool123", user.name + "estpapa",
                    "papa" + user.name, "jaimediscord", "j<3discord", "furryporn456", "secret", "123456789", "pomme49",
                    "redskins32", "princesse", "dragon", "motdepasse1", "1q2w3e4r", "jaimelesfurries"]
        message = await ctx.send(f"`Piratage de {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Piratage de {user}...\nPiratage dans le réseau principal...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Piratage de {user}...\nPiratage dans le réseau principal...\nMise en cache des données...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Piratage de {user}...\nPiratage dans le réseau principal...\nMise en cache des données...\nDécodage des informations du SSN...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Piratage de {user}...\nPiratage dans le réseau principal...\nMise en cache des données...\nDécodage des informations du SSN...\nForçage des détails de la vie amoureuse...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Piratage de {user}...\nPiratage dans le réseau principal...\nMise en cache des données...\nDécodage des informations du SSN...\nForçage des détails de la vie amoureuse...\nFinalisation des détails de la vie du dossier sur la durée de vie\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"```Piratage réussi de {user}\nNom : {random.choice(name)}\nGenre : {random.choice(gender)}\nÂge : {age}\nTaille : {random.choice(height)}\nPoids : {weight}\nCouleur des cheveux : {random.choice(hair_color)}\nCouleur de la peau : {random.choice(skin_color)}\nDate de naissance : {dob}\nEmplacement : {random.choice(location)}\nTéléphone : {phone}\nE-mail : {user.name + random.choice(email)}\nMots de passe : {random.choices(password, k=3)}\nProfession : {random.choice(occupation)}\nSalaire annuel : {random.choice(salary)}\nEthnicité : {random.choice(ethnicity)}\nReligion : {random.choice(religion)}\nSexualité : {random.choice(sexuality)}\nÉducation : {random.choice(education)}```",delete_after=60)

###################################################################################################

@bot.command(pass_context=True,help="Permet de clear un certains nombre de message",name='clear',usage='-clear [nb]',category='Utilitaire')
async def clear(ctx, amount=100):
    amount = int(amount)
    is_dm_or_group = isinstance(ctx.channel, (discord.DMChannel, discord.GroupChannel))
    if is_dm_or_group or isinstance(ctx.channel, discord.TextChannel):
        is_me = ctx.message.author.id == bot.user.id
        deleted_count = -1
        kefta= f'https://cdn.discordapp.com/attachments/1137948255653728367/1137948351564890112/replace.gif'
        async for message in ctx.channel.history(limit=500):
            if not message.type == discord.MessageType.default:  # Vérifier si le message n'est pas un message système
                continue
            try:
                if is_me and message.author.id == bot.user.id:
                    await message.delete()
                    await asyncio.sleep(0.5)
                    deleted_count += 1
            except discord.NotFound:
                pass

            if deleted_count >= amount:
                break
        #await send_kefta_gif(ctx, delete_after=5)
        await ctx.send(f'᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Clear_**:star:\n\n{deleted_count} messages supprimé gg well played', delete_after=5)
        #await send_kefta_gif(ctx, delete_after=5)
    else:
        #await send_kefta_gif(ctx, delete_after=5)
        await ctx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Clear_**:star:\n\na commande fonctionne que dans les dm",deleted_after=5)
        #await send_kefta_gif(ctx, delete_after=5)
    await ctx.message.delete()


@bot.command(help="Permet de changer le préfix",name='setprefix',usage='-setprefix [prefix]',category='Paramétres')
async def setprefix(ctx, prefix: str):
    kefta= f'https://cdn.discordapp.com/attachments/1137948255653728367/1137948351564890112/replace.gif'
    global current_prefix
    current_prefix = prefix
    bot.command_prefix = prefix
    #await send_kefta_gif(ctx, delete_after=5)
    await ctx.send(f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SetPrefix_**:star:\n\nLe préfixe a été changé en `{prefix}`.", delete_after=5)
    #await send_kefta_gif(ctx, delete_after=5)

@bot.command(help="Permet de récupérer tout les messages de la conversation dans les DM",name='savedm',category='Utilitaire')
async def savedm(ctx):
    # Vérifier si le contexte est un DM (Direct Message) ou un groupe privé
    if isinstance(ctx.channel, discord.DMChannel):
        # Récupérer tous les messages du DM (jusqu'à 1000 messages)
        messages = []
        async for message in ctx.channel.history(limit=None):
            messages.append(message)

        # Filtrer les messages pour ne conserver que ceux de l'auteur de la commande et de l'autre personne
        relevant_messages = [message for message in messages if message.author == ctx.author or message.author == ctx.channel.recipient]

        if len(relevant_messages) >= 2:
            # Spécifier le nom du dossier pour enregistrer le fichier
            folder_name = "SaveDM"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            filename = f"{ctx.author.name}_{ctx.channel.recipient.name}.txt"
            file_path = os.path.join(folder_name, filename)

            with open(file_path, 'w', encoding='utf-8') as file:
                for message in relevant_messages:
                    timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    file.write(f"[{timestamp}] {message.author.name}: {message.content}\n")
            #await send_kefta_gif(ctx, delete_after=5)
            await ctx.send(f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nMessages enregistrés dans le fichier {filename}.",delete_after= 5)
            #await send_kefta_gif(ctx, delete_after=5)
        else:
            #await send_kefta_gif(ctx, delete_after=5)
            await ctx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nIl n'y a pas suffisamment de messages pour enregistrer la conversation.",delete_after= 5)
            #await send_kefta_gif(ctx, delete_after=5)
    else:
        #await send_kefta_gif(ctx, delete_after=5)
        await ctx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nCette commande ne peut être utilisée que dans un DM.",delete_after= 5)
        #await send_kefta_gif(ctx, delete_after=5)
    await ctx.message.delete()


@bot.command(name='savegrp', help='Permet de récupérer tout les messages de la conversation d\'un groupe !',category='Utilitaire')
async def savegrp(ctx):
    # Vérifier si le contexte est un DM (Direct Message) ou un groupe privé
    if isinstance(ctx.channel, (discord.DMChannel, discord.GroupChannel)):
        # Récupérer tous les messages du DM ou du groupe privé (jusqu'à 1000 messages)
        messages = []
        async for message in ctx.channel.history(limit=None):
            messages.append(message)

        # Filtrer les messages pour ne conserver que ceux de l'auteur de la commande et des autres participants
        relevant_messages = [message for message in messages if message.author == ctx.author or (isinstance(ctx.channel, discord.GroupChannel) and not message.author.bot)]

        if len(relevant_messages) >= 2:
            # Spécifier le nom du dossier pour enregistrer le fichier
            folder_name = "SaveDM"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            filename = f"{ctx.author.name}_{'_'.join([member.name for member in ctx.channel.recipients])}.txt" if isinstance(ctx.channel, discord.DMChannel) else f"{ctx.channel.name}.txt"
            file_path = os.path.join(folder_name, filename)

            with open(file_path, 'w', encoding='utf-8') as file:
                for message in relevant_messages:
                    timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    file.write(f"[{timestamp}] {message.author.name}: {message.content}\n")
            
            #await send_kefta_gif(ctx, delete_after=5)
            await ctx.send(f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nMessages enregistrés dans le fichier {filename}.",delete_after= 5)
            #await send_kefta_gif(ctx, delete_after=5)
        else:
            #await send_kefta_gif(ctx, delete_after=5)
            await ctx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nIl n'y a pas suffisamment de messages pour enregistrer la conversation.",delete_after= 5)
            #await send_kefta_gif(ctx, delete_after=5)
    else:
        #await send_kefta_gif(ctx, delete_after=5)
        await ctx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nCette commande ne peut être utilisée que dans les groupes.",delete_after= 5)
        #await send_kefta_gif(ctx, delete_after=5)
    await ctx.message.delete()

@bot.command(help='Affiche l\'avatar d\'un membre',name="avatar",category='Utilitaire')
async def avatar(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author

    userAvatar = member.avatar
    #await send_kefta_gif(ctx, delete_after=5)
    await ctx.send(f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Avatar_**:star:\n\n{userAvatar}",delete_after= 10)
    #await send_kefta_gif(ctx, delete_after=5)


@bot.command(help='Affiche la bannière d\'un membre',name="banner",category='Utilitaire')
async def banner(ctx, user :discord.Member = None):
    if user == None:
        user = ctx.author
    try:
        req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
        banner_id = req["banner"]
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
        await ctx.send(f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Banner_**:star:\n\n{banner_url}", delete_after=5)
    except KeyError:
        await ctx.send("Cet utilisateur n'a pas de bannière.", delete_after=5)
    except Exception as e:
        await ctx.send("Une erreur s'est produite lors de la récupération de la bannière.", delete_after=5)
        print(f"Erreur lors de l'exécution de la commande 'banner': {e}")

    await ctx.message.delete()


@bot.command(name='help', help='Affiche la liste des commandes et leur description par catégorie')
async def help(ctx):
    help_message = "```md\n"

    for category, commands_list in categorized_commands.items():
        help_message += f"\n{category}:\n"

        for cmd_name in commands_list:
            help_message += f"[-{cmd_name}]: {bot.get_command(cmd_name).help}\n"

    help_message += "```"

    await ctx.send(f"{help_message}", delete_after=60)
    await ctx.message.delete()

bot.run(TOKEN)
