import discord
from discord.ext import commands
import youtube_dl
import os
import json
import time


SONG_LIST = []
SOLO_LIST = []
SOLO_KING = "insert king here"
LAST_WON = SOLO_KING
GAME_COUNT = 1
TOKEN = "insert here"

client = commands.Bot(command_prefix='~')
def get_info(url):
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
        return ydl.extract_info(url, download=False)
    
@client.event
async def on_ready():
    print('Logged on as {}'.format(client))
    
@client.command() 
async def beingchilling(ctx):#plays john cena chinese beingchilling
    await play(ctx,'https://www.youtube.com/watch?v=AWOyEIuVzzQ')
    
@client.command()
async def lili(ctx):#plays lili houyougen
    await play(ctx,'https://www.youtube.com/watch?v=znrz0nfz6gA')

@client.command()
async def solo(ctx, *args):
    await soloreboot(ctx)
    for each in args:
        SOLO_LIST.append(each)
    await ctx.send(f"Solo roster received, current Solo King: {SOLO_KING}")
    await ctx.send(f"First round, {SOLO_KING} vs. {SOLO_LIST[GAME_COUNT]}")

@client.command()
async def won(ctx, winner):
    global LAST_WON
    global GAME_COUNT
    if GAME_COUNT == 8:
        await (f"Solo赛结束咯!")
    if LAST_WON == SOLO_KING and winner != SOLO_KING:
        await ctx.send(f"水鬼来咯!")
        LAST_WON = winner
        GAME_COUNT += 1
        await ctx.send(f"Next round, {LAST_WON} vs. {SOLO_LIST[GAME_COUNT]}")
    elif LAST_WON == winner and winner != SOLO_KING:
        await ctx.send(f"{winner} has won again, will he challenge {SOLO_KING}?")
        LAST_WON = winner
        GAME_COUNT += 1
        await ctx.send(f"Next round, {LAST_WON} vs. {SOLO_LIST[GAME_COUNT]}")
    elif LAST_WON == SOLO_KING:
        await ctx.send(f"还得是你solo king, 懂不懂solo king的含金量啊?!")
        GAME_COUNT += 1
        await ctx.send(f"Next round, {SOLO_KING} vs. {SOLO_LIST[GAME_COUNT]}")

    else:
        await ctx.send(f"擂主{LAST_WON}倒了! {winner}是新的擂主!")
        LAST_WON = winner
        GAME_COUNT += 1
        await ctx.send(f"Next round, {LAST_WON} vs. {SOLO_LIST[GAME_COUNT]}")

@client.command()
async def soloend(ctx):
    await ctx.send("不玩咯不玩咯 睡觉咯")
    SOLO_LIST = []
    await ctx.send("Player list has been cleared")
    
@client.command()
async def soloreboot(ctx):
    SOLO_LIST = []
    await ctx.send("Player list has been cleared")

@client.command()
async def soloking(ctx, newking):
    global SOLO_KING
    await ctx.send(f"新的SOLO KING 诞生啦!")
    SOLO_KING = newking
    
@client.command()
async def play(ctx, url):
    try:
        if not ctx.message.author.voice:
            await ctx.send("得在语音频道里才能听歌")
            return
        song_info = get_info(url)
            
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
        return

@client.command()
async def connect(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await voice.connect()
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    else:
        await voice_client.move_to(channel)
        
@client.command()
async def countdown(ctx, t):
    await ctx.send(f"Start counting down: {t} seconds")
    t = int(t)
    while t:
        time.sleep(1)
        t -= 1
    await ctx.send("Time is up!")
    await play(ctx, "https://www.youtube.com/watch?v=kcT-i9xzC-8")


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

@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await ctx.send("Song skipped")
    if voice.is_playing():
        voice.stop()
        if len(SONG_LIST) != 0:
            await play(ctx, SONG_LIST[0])
        else:
            return
        


client.run(TOKEN)
