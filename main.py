import discord
from discord.ext import commands
import asyncio
import os
import json
import random
import requests
import robloxpy
from mastodon import Mastodon
from io import BytesIO
from pathlib import Path

path = Path(__file__).with_name("config.json")
with open(path) as f:
	config = json.load(f)

robloxpy.User.Internal.SetCookie(config.get("roblo"),True)
tokenio = config.get('tokenio')
prefix = "!"
mastodon = Mastodon(
    access_token = config.get('masto'),
    api_base_url = 'https://101010.pl'
)
#intents = discord.Intents.default()
#intents.members = True
req = requests.Session()
client = discord.Bot()

k3x10 = discord.SlashCommandGroup("3x10", "Commands for 101010.pl users")
mod = discord.SlashCommandGroup("mod", "Moderator commands")
roblox = discord.SlashCommandGroup("roblox", "Roblox commands")

@client.event
async def on_ready():
        os.system("clear")
        guild = client.guilds[0]
        print('===============================')
        print('Loaded')
        print('Logged in as {0} ({0.id})'.format(client.user))
        print('===============================')
        await status_changer()

@client.event
async def status_changer():
        while True:
                statusgamelist = ['xbox 360',
                        'Playstation',
                        'Playstation 3',
                        'Playstation 4',
                        'Playstation 5',
                        'Nintendo Wii',
                        'NES',
                        'SNES',
                        'Wii',
                        'Wii U',
                        'Gamecube',
                        'Steamdeck',
                        'Gameboy',
                        'Gameboy Advanced',
                        'Gameboy Color',
                        'xbox one',
                        'Playstation 2']
                statuswatchlist = ['Netflix',
                        'HBO',
                        'Twitch',
                        'Amazon Prime',
                        'Youtube',
                        'Peertube',
                        'CDA']
                statuslistenlist = ["Spotify",
                       'Soundcloud',
                       'Youtube Music',
                       'Tidal',
                       'Apple Music']
                await client.change_presence(status=discord.Status.online, activity=discord.Activity(name=random.choice(statusgamelist), type=discord.ActivityType.playing))
                await asyncio.sleep(15)
                await client.change_presence(status=discord.Status.online, activity=discord.Activity(name=random.choice(statuswatchlist), type=discord.ActivityType.watching))
                await asyncio.sleep(15)
                await client.change_presence(status=discord.Status.online, activity=discord.Activity(name=random.choice(statuslistenlist), type=discord.ActivityType.listening))
                await asyncio.sleep(15)

@mod.command(description="Bans user")
@commands.has_permissions(administrator = True)
async def ban(ctx, *, member : discord.Member, reason = "no provided reason"):
#async def ban(ctx, *, member: discord.Option(str), reason: discord.Option(str)):
    await member.ban(reason=reason)
    await ctx.respond(f'Banned {member} for {reason}')

@mod.command(description="Kicks user")
@commands.has_permissions(administrator = True)
async def kick(ctx, *, member : discord.Member, reason = "no provided reason"):
    await member.kick(reason=reason)
    await ctx.respond(f'Kicked {member} for {reason}')

@mod.command(description="Nukes channel")
@commands.has_permissions(administrator = True)
async def nuke(ctx, channel_name):
    guild = client.guilds[0]
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel is not None:
        await existing_channel.clone(reason="Has been nuked")
        await existing_channel.delete()
    else:
        await ctx.respond(f'No channel named **{channel_name}** was found')

@roblox.command(description="Get game details")
async def getgame(ctx, universeid : discord.Option(int)):
#    currentplayers = robloxpy.Game.Internal.GetCurrentPlayers(query)
#    visits = robloxpy.Game.Internal.GetGameVisits(query)
#    likes = robloxpy.Game.Internal.GetGameLikes(query)
#    dislikes = robloxpy.Game.Internal.GetGameDislikes(query)
#    universeid = robloxpy.Game.Internal.GetUniverseID(query)
    #robloxpy.Game.External.GetUniverseData(query)
    #query = robloxpy.Game.Internal.GetUniverseID(query)
    await ctx.respond("Sending request")
    unidata = robloxpy.Game.External.GetUniverseData(universeid)
    print(unidata)
    name = unidata.get("name")
    placeid = unidata.get("rootPlaceId")
    currentplayers = unidata.get('playing')
    visits = unidata.get('visits')
    createdat = unidata.get("created")
    maxplayers = unidata.get("maxPlayers")
    #likes = robloxpy.Game.Internal.GetGameLikes(placeid)
    #dislikes = robloxpy.Game.Internal.GetGameDislikes(placeid)
    favorites = unidata.get("favouritedCount")
    #name = robloxpy.Game.Internal.MyGame.name
    await ctx.send("Game name: " + name + "\nUniverse ID: " + str(universeid) + "\nRoot Place ID: " + str(placeid) + "\nCreated at: " + createdat + "\nFavourites: " + str(favorites) + "\nCurrent Players: " + str(currentplayers) + "\nVisits: " + str(visits) + "\nMax Players: " + str(maxplayers))

@roblox.command(description="Get user details")
async def getuser(ctx, username : discord.Option(str)):
    await ctx.respond("Sending request")
    userid = robloxpy.User.External.GetID(username)
    isonline = robloxpy.User.External.IsOnline(userid)
    isbanned = robloxpy.User.External.Isbanned(userid)
    agedays = robloxpy.User.External.GetAge(userid)
    getrap = robloxpy.User.External.GetRAP(userid)
    image = robloxpy.User.External.GetBust(userid)
    await ctx.send("Username: " + username + "\nUser ID: " + str(userid) + "\nAccount age in days: " + str(agedays) + "\nIs online?: " + str(isonline) + "\nIs banned?: " + str(isbanned) + "\nRAP: " + str(getrap) + "\nBust: " + image)

@k3x10.command(description="Checks atoms from users")
async def atomcheck(ctx, query: discord.Option(str)):
    userlist = mastodon.account_search(query, limit = None, following = False)
    try:
        if userlist[0].get("display_name") == '':
            await ctx.respond("No user found")
        else:
            userid = userlist[0].get("id")
            acct = userlist[0].get("acct")
            userid = str(userid)
            try:
                mastodon.account_follow(userid)
                mastodon.account_unfollow(userid)
                await ctx.respond(f"{acct} is the ally of 101010.pl :white_check_mark:")
            except:
                await ctx.respond(f"{acct} has activated the Atomic Bomb :boom: ")
    except:
        await ctx.respond(f"Command failed")

@k3x10.command(description="Atom List!")
async def atomlist(ctx):
    messagecontent = ""
    aa0 = mastodon.account_search("circumstances.run@circumstances.run", limit = None, following = False)
    aa1 = mastodon.account_search("robsewell@tech.lgbt", limit = None, following = False) 
    aa2 = mastodon.account_search("unicornriot@kolektiva.social", limit = None, following = False) 
    aa3 = mastodon.account_search("majakstasko_bot@lewacki.space", limit = None, following = False) 
    ab0 = aa0[0].get("id")
    ab1 = aa1[0].get("id")
    ab2 = aa2[0].get("id")
    ab3 = aa3[0].get("id")
    try:
        fuf(ab0)
    except:
        messagecontent += "Atom :boom: - circumstances.run\n"
    else:
        messagecontent += "Clear :white_check_mark: - circumstances.run\n"
    finally:
        try:
            fuf(ab1)
        except:
            messagecontent += "Atom :boom: - tech.lgbt\n"
        else:
            messagecontent += "Clear :white_check_mark: - tech.lgbt\n"
        finally:
            try:
                fuf(ab2)
            except:
                messagecontent += "Atom :boom: - kolektiva.social\n"
            else:
                messagecontent += "Clear :white_check_mark: - kolektiva.social\n"
            finally:
                try:
                    fuf(ab3)
                except:
                    messagecontent += "Atom :boom: - lewacki.space\n"
                else:
                    messagecontent += "Clear :white_check_mark: - lewacki.space\n"
        await ctx.respond(messagecontent)
@k3x10.command(description="checks rate limit")
async def ratelimitcheck(ctx):
    await ctx.respond("Amount of avaibale: " + str(mastodon.ratelimit_remaining) + "\nReset: " + str(mastodon.ratelimit_reset) + "\nLimit: " + str(mastodon.ratelimit_limit))

@k3x10.command(description="Search for a Mastodon user")
async def search(ctx, query: discord.Option(str)):
    userlist = mastodon.account_search(query, limit = None, following = False)
    acct = userlist[0].get("acct")
    displayname = userlist[0].get("display_name")
    followers = userlist[0].get("followers_count")
    followers = str(followers)
    messagecontent = "Account name: " + acct + "\nDisplay name: " + displayname + "\nFollowers: " + followers
    await ctx.respond(messagecontent)
    
client.add_application_command(k3x10)
client.add_application_command(mod)
client.add_application_command(roblox)
client.run(tokenio)
