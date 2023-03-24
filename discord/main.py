import json
import discord
import requests
import config as cfg
import io
from discord import option

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)


@bot.slash_command(name="imagine")
@option("prompt", description="Enter a prompt for the image")
@option("negative_prompt", description="Enter a prompt of stuff you don't want in the image", required=False)
async def imagine(ctx: discord.ApplicationContext, prompt: str, negative_prompt: str):
    res = requests.post("http://127.0.0.1:8000/txt2img", json.dumps({
        "prompt": prompt,
        "negative_prompt": negative_prompt
    }))

    file = io.BytesIO(res.content)

    await ctx.respond(f"**{prompt}** by <@{ctx.author.id}>", file=discord.File(file, "image.png"))

bot.run(cfg.config["token"])
