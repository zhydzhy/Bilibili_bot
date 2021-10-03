import discord
from discord.ext import commands
import youtube_dl
import os
import json


SONG_LIST = []
TOKEN = 'Put your token here'

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Logged on as {}'.format(client))


@client.command()
async def info(ctx):
    await ctx.send('Bilibili Bot, trying to play music off of bilibili.com.\rAuthor: CyberWh1t3zZ')

#stream plays the audio from any supported link by youtube-dl
@client.command()
async def play(ctx, url):
    try:
        if not ctx.message.author.voice:
            await ctx.send("You have to be in a voice channel to use play")
            return
        ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    }],
                'outtmpl':'%(title)s.%(etx)s',
                'quiet':False
            }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            song_info = ydl.extract_info(url, download=False)

        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice_client == None:
            await voice.connect()
            voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        else:
            await voice_client.move_to(channel)
        voice_client.play(discord.FFmpegPCMAudio(song_info["formats"][0]["url"]))
    except:
        SONG_LIST.append(url)
        return

#connect to the voice channel where the user that sends the command
async def connect(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await voice.connect()
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    else:
        await voice_client.move_to(channel)

    

#disconnect from voice channel
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice != None:
        await voice.disconnect()
    else:
        await ctx.send("not in a voice channel")

#pause the audio currently playing
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

#resume if audio is paused
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

#stop the music, leaves voice channel
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await voice.disconnect()




client.run(TOKEN)
