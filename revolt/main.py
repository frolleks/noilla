import asyncio
import aiohttp
import requests
import revolt
from revolt.ext import commands
import config as cfg
import json


class Client(commands.CommandsClient):
    async def get_prefix(self, message: revolt.Message):
        return "."

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("pong")

    @commands.command()
    async def imagine(self, ctx: commands.Context):
        msg = ctx.message.content
        msg = msg.split(".imagine ")
        msg = msg[1]
        prompt = msg.split(" --negative ")
        res = requests.post("http://127.0.0.1:8000/txt2img", json.dumps({
            "prompt": prompt[0],
            "negative_prompt": prompt[1] if len(prompt) > 1 else None
        }))
        await ctx.send(content=f"**{prompt[0]}** by <@{ctx.author.id}>", attachments=[
            res.content
        ])


async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(session, cfg.config["token"])
        print("Successfully logged on!")
        await client.start()

asyncio.run(main())
