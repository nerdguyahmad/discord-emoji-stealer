from discord.ext import commands
import requests
import discord

class Makeemoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def makeemoji(self, ctx, name, url=None):
        if url:
            file_request = requests.get(url)
            try:
                emoji = await ctx.guild.create_custom_emoji(image=file_request.content, name=name)
                await ctx.send(f"Emoji <:{emoji.name}:{emoji.id}> was created!")
            except discord.InvalidArgument:
                await ctx.send("You must attach an **image** or a **gif** for the emoji, not a different type of the file.")
            return
        try:
            attachment_url = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send("You must attach an image or a gif for the emoji.")
            return
        file_request = requests.get(attachment_url)
        try:
            emoji = await ctx.guild.create_custom_emoji(image=file_request.content, name=name)
        except discord.InvalidArgument:
            await ctx.send("You must attach an **image** or a **gif** for the emoji, not a different type of the file.")
            return
        await ctx.send(f"Emoji <:{emoji.name}:{emoji.id}> was created!")

    @makeemoji.error
    async def makeemoji_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Specify a name for the emoji. Example: `makeemoji emoji1`")
            return
        raise error

def setup(bot):
    bot.add_cog(Makeemoji(bot))
