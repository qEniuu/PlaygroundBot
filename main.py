import discord
from discord.ext import commands
import asyncio
import os
import json
import random
import requests
from mastodon import Mastodon
from io import BytesIO
from pathlib import Path

path = Path(__file__).with_name("config.json")
with open(path) as f:
	config = json.load(f)

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

k3x10 = discord.SlashCommandGroup("3x10", "Komendy dla użyszkodników głównie 101010.pl.")

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



@client.command(description="Nukes channel")
@commands.has_permissions(administrator = True)
async def nuke(ctx, channel_name):
    guild = client.guilds[0]
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel is not None:
        await existing_channel.clone(reason="Has been nuked")
        await existing_channel.delete()
    else:
        await ctx.respond(f'No channel named **{channel_name}** was found')

@k3x10.command(description="Search for a Mastodon user")
async def search(ctx, query: discord.Option(str)):
    userlist = mastodon.account_search(query, limit = None, following = False)
    acct = userlist[0].get("acct")
    displayname = userlist[0].get("display_name")
    followers = userlist[0].get("followers_count")
    followers = str(followers)
    messagecontent = "Account name: " + acct + "\nDisplay name: " + displayname + "\nFollowers: " + followers
    await ctx.respond(messagecontent)

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

@k3x10.command(description="checks rate limit")
async def ratelimitcheck(ctx):
    await ctx.respond("Amount of avaibale: " + str(mastodon.ratelimit_remaining) + "\nReset: " + str(mastodon.ratelimit_reset) + "\nLimit: " + str(mastodon.ratelimit_limit))

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
client.add_application_command(k3x10)

client.run(tokenio)
