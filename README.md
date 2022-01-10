
# Hey, I am Yuki. A Bot which works with both Slash and Prefixed Commands!

<p align="center">
  <img width="460" height="400" src="https://cdn.discordapp.com/attachments/920354515142733825/920517232554024990/VIWztfa.png">
</p>

## Prerequisites

Python 3.8+
Java LTS 11+
Check out. the `requirements.txt` and install all the pakages. Use `pip install -r requirements.txt`
Make sure you have the [Lavalink.jar](https://github.com/freyacodes/Lavalink/releases) file and the [application.yml](https://github.com/freyacodes/Lavalink/blob/master/LavalinkServer/application.yml.example) file too

## Installing

You can either fork this repo or just download the zip
You will need Python 3.

## Getting Started!

Change the following:
`guild_ids`: I have added ... instead of the `guild_ids`. Why guild_ids and not global? Many people might have raised this question. Slash Commands may take an hour to register whereas adding selected guilds, it registers in an instant⚡.

Make sure you have the `main.db` file in the `utils/databases` directory and a `config.py` in the main directory with your [TENOR](https://tenor.com/developer/keyregistration) api key

> 

First use `java -jar Lavalink.jar` to run the Lavalink Node!
Then use `python bot.py`
and you are good to go!

## Built With

[Pycord](https://github.com/Pycord-Development/pycord) - The main API I used to connect to Discord.