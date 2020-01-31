# Lanturn Bot Public Source Code
A Pokemon Sword and Shield raid and seed
finding discord bot programmed and designed
by fishguy6564. Credits to algorithms used
and help received below. 

#Credit:
Used some algorithms publicly available by Admiral-Fish
Rafa10 for getting the get heap function to work
mdbell for noexes and KrankRival for the noexes .nsp port

#Prerequisites:
Please use by installing python3. 
Use pip commands to install the following:
pip install z3-solver

#Current Features:
$GetSeed - Gets a user's seed and next square/star shiny frame
by a user passing their encryption constant, pid, and IVs as arguments.

$GetFrameData - Gets a user's next square/star shiny frame by a
user passing their already generated seed as an argument.

$GetPoke - Requires a modded switch with noexes installed.
It obtains the Pokemon data from a player who offers their pokemon
for trade similar to dudu bot and reports it in the discord chat.

$logout - For the admin only. Will turn off the bot for testing

#Planned Features:
- Automation similar to dudu bot so users don't have to manually initiate trades
- Dump .pk8 file from offered pokemon from trade and send it via discord.
- Check a offered Pokemon's IVs