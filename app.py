import os
from flask import Flask
from flask_discord_interactions import DiscordInteractions
import importlib
app = Flask(__name__)
discord = DiscordInteractions(app)

app.config["DISCORD_CLIENT_ID"] = "1114130290516959263"
app.config["DISCORD_PUBLIC_KEY"] = "cfce12e1a56c319a72daa606eb9199ab13766870e2b96cec97ae370cf21dfa28"
app.config["DISCORD_CLIENT_SECRET"] = "hW8hZtD4Wln0-uGrlS-1JsXajOgB7rVV"

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
