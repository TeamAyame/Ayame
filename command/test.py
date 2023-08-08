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

@bot.command()
def work(ctx: Context):
    t = get_timeout(ctx.author, "work")
    member = ctx.author
    currency = get_currency(ctx.guild)
    user = users.find_one({'gid': ctx.guild.id})
    work_stats = check_stats("work_stats")
    if t[0]:
        works = {
            1: 'Вы поработали программистом и зарабатывали',
            2: 'Вы поработали в SubWay и зарабатывали',
            3: 'Вы поработали строителем и заработали',
            4: 'Вы поработали парикмахером и заработали',
            5: 'Вы поработали водителем такси и заработали',
            6: 'Вы поработали сантехником и заработали'
        }
        work = random.randint(1, 6)
        amount = random.randint(500, 1000)
        if work <= 3:
            amount = random.randint(200, 600)
        users.update_one({'gid': member.guild.id, 'uid': member.id}, {'$set': {'balance': user['balance'] + amount}})
        return Message(embed=Embed(description=f'{works[work]} {task(amount)} {currency}'))
    else:
        return Message(embed=Embed(
            description=f"Вы сможете выйти на работу <t:{str(t[1].timestamp()).split('.')[0]}:R>"))