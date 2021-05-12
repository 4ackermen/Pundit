import logging
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import errors as discorderr
from discord.utils import get

from core.pundit.pundit import PUNDIT

class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_any_role(*(PUNDIT['adminroles']))
    async def serverstats(self, ctx):
        """
        Server Statistics
        """
        self.server = get(self.bot.guilds, name='bi0s Recruitment')
        # server = self.bot.get_guild(id=PUNDIT['server'])
        # members = await self.server.fetch_members(limit=150).flatten()
        embed = discord.Embed(title=f"{ctx.guild.name}", description="Stats of bi0s Recruitment Server", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        # embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
        # embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
        embed.add_field(name="Member Count", value=str(len(ctx.guild.members)))
        embed.add_field(name="Major Generals", value=str(len([member for member in self.server.members if (get(member.roles, name='Major General'))])))
        embed.add_field(name="Lieutenants", value=str(len([member for member in self.server.members if (get(member.roles, name='Lieutenant'))])))
        embed.add_field(name="Sanity Solves", value=str(len(set([member for member in self.server.members if get(member.roles, name='Private')])  |  set([member for member in self.server.members if get(member.roles, name='Private First Class')]))))
        embed.add_field(name="Recruits in S1", value=str(len([member for member in self.server.members if (get(member.roles, name='Private'))])))
        embed.add_field(name="Recruits in S3", value=str(len([member for member in self.server.members if (get(member.roles, name='Private First Class'))])))
        embed.add_field(name="Sergeant Count", value=str(len([member for member in self.server.members if get(member.roles, name='Sergeant')])))
        embed.add_field(name="Master Sergeant Count", value=str(len([member for member in self.server.members if get(member.roles, name='Master Sergant')])))
        embed.add_field(name="Sergeant Major Count", value=str(len([member for member in self.server.members if get(member.roles, name='Sergant Major')])))
        # embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
        # embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        # embed.set_thumbnail(url=f"{ctx.guild.icon}")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Statistics(bot))

