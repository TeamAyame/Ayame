import os
from flask import Flask
from flask_discord_interactions import DiscordInteractions
import importlib
app = Flask(__name__)
discord = DiscordInteractions(app)

app.config["DISCORD_CLIENT_ID"] = ""
app.config["DISCORD_PUBLIC_KEY"] = ""
app.config["DISCORD_CLIENT_SECRET"] = ""

discord.set_route("/interactions")

for file in os.listdir(f"command"):
    if not file.endswith(".py"):
        continue

    command_filename = file[:-3]
    command = importlib.import_module(f"command.{command_filename}").bot
    discord.register_blueprint(command)

    print(f"\033[32m Command \033[0m {file} was successfully initialized")

discord.update_commands()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
