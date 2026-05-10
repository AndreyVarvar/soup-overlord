import json
from discord.ext import commands as cmds


def get_name(bot: cmds.Bot, user_id: str):
    """
    1) They are on the server and their name matched the one in cache
    2) They are on the server but they changed their name
    3) They are not on the server so their old name is used
    """
    with open("username_cache.json", "r") as file:
        cache = json.load(file)

    if bot.get_user(int(user_id)) is None:
        if user_id not in cache:
            return "Deleted User"  # I will probably need to manualy set their nickname
        else:
            pass
    elif bot.get_user(int(user_id)) not in cache:
        cache[user_id] = bot.get_user(int(user_id)).display_name  # update/set their nickname on the server

        with open("username_cache.json", "w") as file:
            json.dump(cache, file, indent=4)
    
    return cache[user_id]