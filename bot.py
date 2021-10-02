import discord
from discord.ext import commands
import youtube_dl
import os
import json


SONG_LIST = []
TOKEN = 'ODE3MjgzMDEwMzA3MTYyMTEy.YEHQHg.mCx2HtddDWsZ1WDDnf2tnisn-7k'

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Logged on as {}'.format(client))


@client.command()
async def info(ctx):
    await ctx.send('Bilibili Bot, trying to play music off of bilibili.com.\rAuthor: CyberWh1t3zZ')

@client.command()
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send("得在语音频道里才能听歌啊 你猪笔吧!")
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
        await ctx.send("没在语音里面 leave尼玛")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await voice.disconnect()




client.run(TOKEN)
