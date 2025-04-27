import os
import discord
from discord.ext import commands


import ollama 
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="@", intents=intents)




@bot.event
async def on_ready():
    print(f"bot is ready as {bot.user.name}")


@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("hello, I am a bot!")
    


@bot.command(name="ask")
async def ask(ctx, *, message):
    print(message)
    print("========")
    response = ollama.chat(model='llama3', messages=[       
        {
            'role': 'system',
            'content': 'you are a helpful assistant who provides answers to the questions concisely in no more than 800 words. ',
        },
        {
            'role': 'user',
            'content': message,
        },
    ])
    print(response['message']['content'])
    await ctx.send(response['message']['content'])   


       # Send in chunks if reply is too long
    if len(reply) <= 2000:
        await ctx.send(reply)
    else:
        for i in range(0, len(reply), 2000):
            await ctx.send(reply[i:i+2000]) 
    




@bot.command(name="summarise")
async def summarise(ctx):
    msgs = [ message.content async for message in ctx.channel.history(limit=10)]


    summarise_prompt = f"""
        summarise the following messages delimited by 3 backticks;
        ```
        {msgs}
        ```
        """
    


    response = ollama.chat(model='llama3', messages=[       
        {
            'role': 'system',
            'content': 'you are a helpful assistant who summarises the provided messages concisely .',
        },
        {
            'role': 'user',
            'content': summarise_prompt,
        },
    ])
    print(response['message']['content'])
    await ctx.send(response['message']['content'])    
    



bot.run(os.getenv("DISCORD_BOT_TOKEN"))














