import discord
from discord.ext import commands
import time
import asyncio
import random
import os


def get_token():
    with open('token.txt') as f:
        return f.read().strip()

bot = commands.Bot(command_prefix='-',self_bot=True)
snipe_message_author = {}
snipe_message_content = {}
TOKEN = get_token()

@bot.event
async def on_ready():
    print(f'Connecté à {bot.user}  (ID: {bot.user.id})')


@bot.command(hidden=True)
async def kids(ctx):
    await ctx.send('<@537309367129604096> depuis aujourdhui\n https://cdn.discordapp.com/attachments/1134270242147807336/1137827196153626633/macaco_triste.jpg')

@bot.command(hidden=True)
async def kids_clown(ctx):
    for i in range(100):
        await ctx.send('<@537309367129604096> tu es un clown !\n https://media.discordapp.net/attachments/1133840588924538880/1137828275331268711/Sans_titre.jpg', delete_after = 5)
        await asyncio.sleep(5)

@bot.command(name='ping', help='Répond pong')
async def ping(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/1137948255653728367/1137948351564890112/replace.gif', delete_after=5)
    await ctx.send('᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Pong_**:star:\n\npong', delete_after=5)
    await ctx.send('https://cdn.discordapp.com/attachments/1137948255653728367/1137948351564890112/replace.gif', delete_after=5)
    await ctx.message.delete()

@bot.event
async def on_message_delete(message):
    snipe_message_author.pop(message.channel.id, None)
    snipe_message_content.pop(message.channel.id, None)

    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content

    await asyncio.sleep(30)

    snipe_message_author.pop(message.channel.id, None)
    snipe_message_content.pop(message.channel.id, None)

@bot.command(name= 'snipe', help='Permet de voir le dernier message supprimé du salon')
async def snipe(ctx):
    channel = ctx.channel
    try:
        author = snipe_message_author[channel.id]
        content = snipe_message_content[channel.id]
        if isinstance(channel, discord.TextChannel):
            channel_name = f"#{channel.name}"
        else:
            channel_name = "a DM"
        
        message = f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Snipe_**:star:\n\nDernier message envoyé est: {content}\nenvoyé par **{author}**"
        kefta= f'https://cdn.discordapp.com/attachments/1137948255653728367/1137948351564890112/replace.gif'
        await ctx.send(kefta, delete_after=10)
        await ctx.send(message, delete_after=10)
        await ctx.send(kefta, delete_after=10)
    except KeyError:
        await ctx.send(f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Snipe_**:star:\n\nPas de message récent supprimé ici !")
    await ctx.message.delete()



@bot.command(pass_context=True,help="Permet de clear un certains nombre de message",name='clear',usage='-clear [nb]')
async def clear(ctx, amount=100):
    amount = int(amount)
    is_dm_or_group = isinstance(ctx.channel, (discord.DMChannel, discord.GroupChannel))
    if is_dm_or_group or isinstance(ctx.channel, discord.TextChannel):
        is_me = ctx.message.author.id == bot.user.id
        deleted_count = 0
        kefta= f'https://cdn.discordapp.com/attachments/1137948255653728367/1137948351564890112/replace.gif'
        async for message in ctx.channel.history(limit=500):
            if is_me and message.author.id == bot.user.id:
                await message.delete()
                await asyncio.sleep(1)
                deleted_count += 1
                

            if deleted_count >= amount:
                break
        await ctx.send(kefta, delete_after=5)
        await ctx.send(f'᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Clear_**:star:\n\n{deleted_count} messages supprimé gg well played', delete_after=5)
        await ctx.send(kefta, delete_after=5)
    else:
        await ctx.send(kefta, delete_after=5)
        await ctx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Clear_**:star:\n\na commande fonctionne que dans les dm",deleted_after=5)
        await ctx.send(kefta, delete_after=5)
    await ctx.message.delete()


@bot.command(help="Permet de changer le préfix",name='setprefix',usage='-setprefix [prefix]')
async def setprefix(ctx, prefix: str):
    kefta= f'https://cdn.discordapp.com/attachments/1137948255653728367/1137948351564890112/replace.gif'
    global current_prefix
    current_prefix = prefix
    bot.command_prefix = prefix
    await ctx.send(kefta, delete_after=5)
    await ctx.send(f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SetPrefix_**:star:\n\nLe préfixe a été changé en `{prefix}`.", delete_after=5)
    await ctx.send(kefta, delete_after=5)

@bot.command(help="Permet de récupérer tout les messages de la conversation dans les DM",name='savedm')
async def savedm(ctx):
    kefta= f'https://cdn.discordapp.com/attachments/1137948255653728367/1137948351564890112/replace.gif'
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
            await ctx.send(kefta, delete_after=5)
            await ctx.send(f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nMessages enregistrés dans le fichier {filename}.",delete_after= 5)
            await ctx.send(kefta, delete_after=5)
        else:
            await ctx.send(kefta, delete_after=5)
            await ctx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nIl n'y a pas suffisamment de messages pour enregistrer la conversation.",delete_after= 5)
            await ctx.send(kefta, delete_after=5)
    else:
        await ctx.send(kefta, delete_after=5)
        await ctx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nCette commande ne peut être utilisée que dans un DM.",delete_after= 5)
        await ctx.send(kefta, delete_after=5)
    await ctx.message.delete()


@bot.command(name='savegrp', help='Permet de récupérer tout les messages de la conversation d\'un groupe !')
async def savegrp(ctx):
    kefta= f'https://cdn.discordapp.com/attachments/1137948255653728367/1137948351564890112/replace.gif'
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
            
            await ctx.send(kefta, delete_after=5)
            await ctx.send(f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nMessages enregistrés dans le fichier {filename}.",delete_after= 5)
            await ctx.send(kefta, delete_after=5)
        else:
            await ctx.send(kefta, delete_after=5)
            await ctx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nIl n'y a pas suffisamment de messages pour enregistrer la conversation.",delete_after= 5)
            await ctx.send(kefta, delete_after=5)
    else:
        await ctx.send(kefta, delete_after=5)
        await ctx.send("᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta SaveDM_**:star:\n\nCette commande ne peut être utilisée que dans les groupes.",delete_after= 5)
        await ctx.send(kefta, delete_after=5)
    await ctx.message.delete()


@bot.command(help="T'es con t'es dedans", name='aide')
async def aide(ctx):
    kefta= f'https://cdn.discordapp.com/attachments/1137948255653728367/1137948351564890112/replace.gif'
    # Afficher une description globale du bot
    help_message = f"᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼:star:**_Kefta Aide_**:star:\n\n"

    # Liste des commandes disponibles
    command_list = bot.commands

    for command in command_list:
        # Vérifier si la commande est cachée (non affichée dans la liste d'aide)
        if not command.hidden:
            # Ajouter le nom de la commande et sa description dans le message d'aide
            help_message += f"**{command.name}**: {command.help}\n"
    await ctx.send(kefta, delete_after=60)
    await ctx.send(help_message,delete_after= 60)
    await ctx.send(kefta, delete_after=60)
    await ctx.message.delete()

bot.run(TOKEN)