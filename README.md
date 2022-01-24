# cocobot
a Discord retard bot, originally created for r/okbuddyhololive.

the code is already like 6 months old, so it's clumsy, sorry if it's too messed up

## running
1. make sure you are running Python 3.8+
2. make an application on the [Discord Developer Portal](https://discordapp.com/developers/applications/)
3. install all modules from `requirements.txt` using `python -m pip install -r requirements.txt`
4. download & install `averaged_perceptron_tagger` for NLTK using `python -c "import nltk; nltk.download('averaged_perceptron_tagger')"`
5. rename `credentials.example.py` to `credentials.py` & copy your bot token in `discord_token`
    - a DigitalOcean API token is not required, it's only used for `pd billing`
6. configure `assets/config.py` to your liking
    - some settings are not configurable, but you can change them in the code (i don't know why was i doing that lol), ex. `pd impregnate` working everytime on your own account
7. gather messages for the Markov chain in a [MessagePack](https://msgpack.org/) format & save it as `assets/memory.msgpack`
    - you can use a script in [this](https://gist.github.com/bemxio/97b786fc9328c8ecfb1ada2dfe84e852) gist to generate a MessagePack from a text file split by newlines
8. run `python bot.py`

if you have any problems with running cocobot, feel free to make an issue on this repository

## contributions
while i don't plan to make any new features, if you see a bug or something you want to add, feel free to make a pull request on this repository. i'll be happy to review your pull request and make it live :D