from utils.database import *
from flask_discord_interactions import DiscordInteractionsBlueprint, Member, Message, Embed, embed, Context
bot = DiscordInteractionsBlueprint()
import random

@bot.command()
def set_currency(ctx: Context, currency:str):
    get_guild(ctx.guild_id)
    settings.update_one({'gid': ctx.guild_id}, {'$set': {'currency': currency}})
    return Message(embed=Embed(
        description=f'<:success:1082768543923310694> Вы успешно изменили значок валюты на {currency}'))

@bot.command()
def info(ctx: Context):
    return Message(
        f"""
GID: {ctx.guild_id}
ID: {ctx.author.id}
NAME: {ctx.author.display_name}
        """
    )

@bot.command()
def balance(ctx: Context):
    get_guild(ctx.guild_id)
    currency = get_currency(ctx.guild_id)
    user = get_user(ctx.author.id, ctx.guild_id)
    return Message(embed=Embed(
        fields=[
            embed.Field(
            name="Баланс:",
            value=f"{task(user['balance'])} {currency}"
            ),
            embed.Field(
                name="Банк:",
                value=f"{task(user['bank'])} {currency}"
            )
        ]
    ))
