<h1>Opskins-Searching Telegram Bot</h1>
Script to create a Telegram-Search-Bot for Opskins.com
With the bot, you can search for different virtual items in different games including images from the items and get their prices in USD and WAX (calculated with
the value from coinmarketcap.com)<br><br>



<b>Dependencies:</b>
 - Python 3 and the different modules (install via pip: ```pip install python-telegram-bot```)
 - OPSkinskey (How to get one: You need an account at opskins.com - there you can generate your key at Account->Advanced Options)
 - Your telegram bot with token (How to get one: https://core.telegram.org/bots#6-botfather )
 - Coinmarketcap API-Key (How to get one: https://coinmarketcap.com/api/)
 - Coinmarketcap Sandbox-API-Key (How to get one: https://sandbox.coinmarketcap.com/)
<b>Installation:</b>
 - copy the script into the desired location
 - Rename or copy sample-credentials.py to credentials.py and add your OPSkinskey, coinmarketcap-api/coinmarketcap-sandbox-api and your Telegram-Bot-Token
 - make sure, your dependencies are installed
 - activate or deactivate the coinmarketcap-sandbox in credentials.py

<b>Start the script (depending on your python installation):</b>
 - ```python opskins-searchbot.py``` or ```python3 opskins-searchbot.py```


<b>Usage:</b>
 - send <b>/games</b> to get a list of supported games and choose one
 - search for an item (just type the name of the item)
 - use the buttons to get the current market price

 <b>Comment:</b>
 Still in Alpha-state and a very messy code - but I'm going to work on that the next days. But the WAX-Bounty-Program (for what this project was coded) ends in a short time, so I was in a little hurry ;).

<b>Latest updates:</b>
- Coinmarketcap API v2 (API-key needed, since v1 is deprecated and will shut down soon)
- changed the authorization method
- integrated an individual file for authorization
- gamelist is now generated in a better way
- pictures!
