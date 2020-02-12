# Dudu Bot

A Pokemon SWSH bot that performs seed checking for max raid dens.

## Credit

This project has been forked from https://gitlab.com/fishguy6564/lanturn-bot-public-source-code.

Thanks to https://gitlab.com/fishguy6564 for the initial work.

## Installation

This project requires that you have python 3.6 or later installed on your system.

To install the project dependencies run:

.. code-block:: bash

   pip install -r requirements.txt


## Run The Bot

You may be wondering how to run this. As for the switch side of things, you
must already have a cfw installed, preferrably atmosphere. Olliz0r has 
instructions on how to setup sys-botbase in the readme of his github page.
Please check DuduClient.py, bot.py, and RaidCommands.py for comments on what
needs to be filled in. Once all of that is done, double click run.bat and if
all goes well, DuduClient should shoot out a message saying "Awaiting... Inputs" 
if successfully connected to your switch. bot.py should show a message that 
prints out your basic discord info.

Want to see it in action? Check out the demo video [here](https://www.youtube.com/watch?v=yDIYqYmnV3Y)

## Bot Commands

- `$GetSeed` - Gets a user's seed and next square/star shiny frame
by a user passing their encryption constant, pid, and IVs as arguments.
- `$GetFrameData` - Gets a user's next square/star shiny frame by a
user passing their already generated seed as an argument.
- `$CheckMySeed` - Queues up the invoker and initiates the Dudu Clone modules.
It communicates to the DuduClient script via the communicate.bin file. Please
do not trash any files when downloading them.
- `$greet` - Sends a cute message depending on what the developer sets it to.
- `$CheckQueueSize` - Reports the amount of people currently in the queue
- `$CheckMyPlace` - Reports the current position of the sender in the queue system
- `$logout` - For the admin only. Will turn off the bot for testing.

## Important Things To Note

- This is calibrated for Pokemon Sword and Shield in English. Other languages
may have more dialogue in certain parts and will need to be recalibrated.
- Text speed must be set to the fastest setting in order to keep the timing of
the button inputs from the dudu client.
- Using a modded switch online CAN get you banned. I am not responsible if you
somehow do get banned. You use this at your own risk.
