from datetime import datetime as dt, timedelta
import pymongo
from flask_discord_interactions import Member
db = pymongo.MongoClient('').main

users = db["users"]
settings = db["settings"]

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

def get_currency(guild_id):
    guild_id = int(guild_id)
    guild = settings.find_one({"gid": guild_id})
    return guild["currency"] if guild else "🪙"
