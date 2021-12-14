import re
from discord import Color, Embed
from discord.ext import commands
from discord.commands import slash_command, Option
from utils.functions import create_guest_paste_bin


class CodeRunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")

    @property
    def session(self):
        return self.bot.http._HTTPClient__session  # type: ignore

    async def _run_code(self, *, lang: str, code: str):
        res = await self.session.post(
            "https://emkc.org/api/v1/piston/execute",
            json={"language": lang, "source": code},
        )
        return await res.json()

    @commands.command()
    async def run(self, ctx: commands.Context, *, codeblock: str):
        matches = self.regex.findall(codeblock)
        if not matches:
            return await ctx.reply(
                embed=Embed(
                    title="Uh-oh", description="Couldn't quite see your codeblock"
                )
            )
        lang = matches[0][0] or matches[0][1]
        if not lang:
            return await ctx.reply(
                embed=Embed(
                    description="**<:error:897382665781669908> Oops, Couldn't find the language hinted in the codeblock or before it**",
                )
            )
        code = matches[0][2]
        result = await self._run_code(lang=lang, code=code)

        await self._send_result(ctx, result)

    @commands.command()
    async def runl(self, ctx: commands.Context, lang: str, *, code: str):
        result = await self._run_code(lang=lang, code=code)
        await self._send_result(ctx, result)

    async def _send_result(self, ctx: commands.Context, result: dict):
        if "message" in result:
            embed = Embed(description=f"<:error:897382665781669908> Oops!\n\n {result['message']}")
            return await ctx.reply(embed=embed)
        output = result["output"]
        #        if len(output) > 2000:
        #            url = await create_guest_paste_bin(self.session, output)
        #            return await ctx.reply("Your output was too long, so here's the pastebin link " + url)
        embed = Embed(description=f"**<:tick:897382645321850920> Successfully ran your {result['language']} code!**", color=Color.green())
        output = output[:500].strip()
        shortened = len(output) > 500
        lines = output.splitlines()
        shortened = shortened or (len(lines) > 15)
        output = "\n".join(lines[:15])
        output += shortened * "\n\n**Output shortened**"
        embed.add_field(name="Output", value=output or "**<No output>**")

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(CodeRunCog(bot))