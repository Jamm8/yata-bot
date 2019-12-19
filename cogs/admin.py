# import standard modules
import json

# import discord modules
import discord
from discord.ext import commands
from discord.utils import get
from discord.utils import oauth_url


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def reload(self, ctx):
    #     """Admin tool for the bot owner"""
    #     from includes.yata_db import load_configurations
    #     from includes.yata_db import push_guild_name
    #     if ctx.author.id != 227470975317311488:
    #         await ctx.send("This command is not for you")
    #         return
    #     _, c = load_configurations(self.bot.bot_id)
    #     self.bot.config = c
    #     await ctx.author.send("**Configurations reloaded**")
    #     for k1, v1 in json.loads(self.bot.config).items():
    #         await ctx.author.send(f"`{k1}`")
    #         guild = get(self.bot.guilds, id=int(k1))
    #         await push_guild_name(guild)
    #         for k2, v2 in json.loads(self.bot.config)[k1].items():
    #             await ctx.author.send(f"`{k2} {v2}`")

    @commands.command()
    async def invite(self, ctx):
        """Admin tool for the bot owner"""
        if ctx.author.id != 227470975317311488:
            await ctx.send("This command is not for you")
            return
        # await ctx.send(oauth_url(self.bot.user.id, discord.Permissions(permissions=469837840)))
        await ctx.send(oauth_url(self.bot.user.id, discord.Permissions(permissions=8)))

    @commands.command()
    async def yataRole(self, ctx):
        """Admin tool for the bot owner"""
        if ctx.author.id != 227470975317311488:
            await ctx.send("This command is not for you")
            return

        # loop over member
        for member in ctx.guild.members:
            print(f"[YATA ROLE] {member} [{member.id}]")
            status, id, key = await self.bot.get_master_key(ctx.guild)
            if status == -1:
                return
            status, _, _, _ = await self.bot.get_user_key(ctx, member, needPerm=False)
            if status == 0:
                await member.add_roles(get(ctx.guild.roles, name="YATA user"))

    # helper functions

    async def role_exists(self, ctx, guild, name):
        r = get(guild.roles, name=f"{name}")
        s = f":white_check_mark: {name} role present" if r is not None else f":x: no {name} role"
        await ctx.send(s)

    async def channel_exists(self, ctx, guild, name):
        r = get(guild.channels, name=f"{name}")
        s = f":white_check_mark: {name} channel present" if r is not None else f":x: no {name} channel"
        await ctx.send(s)

    @commands.command()
    async def c(self, ctx):
        """Admin tool for the bot owner"""

        if ctx.author.id != 227470975317311488:
            await ctx.send("This command is not for you")
            return

        # loop over guilds
        for guild in self.bot.guilds:
            await ctx.send(f"**Guild {guild} owned by {guild.owner} aka {guild.owner.display_name}**")
            config = self.bot.get_config(guild)

            await ctx.send("*general*")
            # check 0.1: test if config
            s = ":white_check_mark: configuration files" if len(config) else ":x: no configurations"
            await ctx.send(s)

            # check 0.2: test system channel
            s = ":white_check_mark: system channel" if guild.system_channel else ":x: no system channel"
            await ctx.send(s)

            # check 0.3: test readme channel
            await self.channel_exists(ctx, guild, "readme")

            # check 1: loot module
            if self.bot.check_module(guild, "loot"):
                await ctx.send("*loot*")

                # check 1.1: Looter role
                await self.role_exists(ctx, guild, "Looter")

                # check 1.2: #loot and #start-looting
                await self.channel_exists(ctx, guild, "loot")
                await self.channel_exists(ctx, guild, "start-looting")

            # check 2: verify module
            if self.bot.check_module(guild, "verify"):
                await ctx.send("*verify*")

                # check 1.1: Verified role
                await self.role_exists(ctx, guild, "Verified")

                # check 1.2: #verified-id
                await self.channel_exists(ctx, guild, "verify-id")
                for k, v in config.get("factions", dict({})).items():
                    await self.role_exists(ctx, guild, f"{v} [{k}]")