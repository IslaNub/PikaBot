import discord
from discord.ext import commands
import datetime

class mod:
    '''Moderation commands!'''
    def __init__(self, bot):
        self.bot = bot
        
      
    now = datetime.datetime.utcnow()
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx ,user: discord.Member=None, *, reason: str=None):
        '''Kick a member from the server!'''
        if not user:
            await ctx.send("Please mention a member for this command to work")
        try:
            embed = discord.Embed(title=f"Kick | {ctx.guild.name}", color=0xff0000, inline=True)
            embed.add_field(name=f"Moderator:", value=f"{ctx.author.name}", inline=True) 
            embed.add_field(name=f"User:", value=f"{user.name}", inline=True)
            embed.add_field(name=f"Reason:", value=reason, inline=True)
            embed.add_field(name=f"Issued At:", value=now, inline=True)
            embed.set_thumbnail(url=user.avatar_url)
            channel = discord.utils.get(ctx.guild.channels, name='mod-log')
            if not channel:
                channel = await ctx.guild.create_text_channel(name="mod-log")
                await channel.send(embed=embed)
            else:
                await channel.send(embed=embed)
            await user.send(embed=embed)
            await ctx.guild.kick(user)
        except discord.Forbidden:
            await ctx.send("I could not kick the member, Please check my permissions")
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx ,user: discord.Member=None, *, reason: str=None):
        '''Ban a member from the server!'''
        if not user:
            await ctx.send("Please mention a member for this command to work")
        try:
            embed = discord.Embed(title=f"Ban | {ctx.guild.name}", color=0xff0000, inline=True)
            embed.add_field(name=f"Moderator:", value=f"{ctx.author.name}", inline=True) 
            embed.add_field(name=f"User:", value=f"{user.name}", inline=True)
            embed.add_field(name=f"Reason:", value=reason, inline=True)
            embed.add_field(name=f"Issued At:", value=now, inline=True)
            embed.set_thumbnail(url=user.avatar_url)
            if not channel:
                channel = await ctx.guild.create_text_channel(name="mod-log")
                await channel.send(embed=embed)
            else:
                await channel.send(embed=embed)
            await user.send(embed=embed)
            await ctx.guild.ban(user)
        except discord.Forbidden:
            await ctx.send("I could not ban the member, Please check my permissions")
        
def setup(bot):
    bot.add_cog(mod(bot))
