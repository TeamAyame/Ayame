from datetime import datetime as dt, timedelta
import pymongo
from flask_discord_interactions import Member
db = pymongo.MongoClient('mongodb+srv://admin0001:llWW6Pw4FjmRtzNA@bot.ggs2v.mongodb.net/main?retryWrites=true&w=majority').main

users = db["users"]
settings = db["settings"]
shop = db["shop"]
promocodes = db["promocodes"]
cooldown = db["cooldown"]
work_stats = db["work_stats"]

def task(value):
    return f'{value:,}'

def get_guild(guild_id):
    guild_id = int(guild_id)
    guild_obj = settings.find_one({"gid": guild_id})
    if not guild_obj:
        guild_obj = {
            'gid': guild_id,
            'currency': '🪙',
            'premium': False,
            "timeout_work": 2,
            "timeout_crime": 3,
            "timeout_collect": 2
        }
        settings.insert_one(guild_obj)
    return guild_obj

def get_user(member_id, guild_id):
    condition = {
        'uid': int(member_id),
        'gid': int(guild_id)}

    user = users.find_one(condition)
    if not user:
        user = {
            'gid': int(guild_id),
            'uid': int(member_id),
            'balance': 0,
            'bank': 0
        }
        users.insert_one(user)
    return user

def get_timeout(user: Member, cmd: str) -> tuple[bool, int] | tuple[bool, dt]:
    now = dt.now()
    c = cooldown.find_one({"gid": user.guild.id, "uid": user.id, "cmd": cmd})
    if not c:
        cooldown.insert_one({"gid": user.guild.id, "uid": user.id, "cmd": cmd, "c": now})
        return True, 0
    g = get_guild(user.guild)
    to = g[f"timeout_{cmd}"] * 60 * 60
    if (now - c["c"]).total_seconds() < to:
        return False, dt.now() + timedelta(seconds=to - (now - c["c"]).total_seconds())
    cooldown.update_one({"gid": user.guild.id, "uid": user.id, "cmd": cmd}, {"$set": {"c": now}})
    return True, 0

def check_stats(name: str):
    stat = work_stats.find_one({"name": name})
    if not stat:
        object = {
            "name": name,
            "amount": 0
            }
        work_stats.insert_one(object)
        return 0
    updatedamount = stat["amount"] + 1
    work_stats.update_one({"name": name}, {"$set": {"amount": updatedamount}})
    return updatedamount

def get_currency(guild_id):
    guild_id = int(guild_id)
    guild = settings.find_one({"gid": guild_id})
    return guild["currency"] if guild else "🪙"