from discord.ext import tasks, commands
import discord
from framecalc import *
from seedgen import *
from GetPokeInfo import *
from bot import *
from Person import *
from ArrayQueue import *
import time
import settings


BOT_NAME = settings.get_settings().bot_name
# 300 with the current queue and the reporting system
# will make sure everyone has a place and can see when they will be served
# q = ArrayQueue(300)

# until possible merge and improvement, setting it to 20 as from the previous commits
q = ArrayQueue(20)


class RaidCommands(commands.Cog):
    def __init__(self, client):
        self.checkDataReady.start()
        self.userChannel = None
        self.user = None
        self.id = None
        self.person = None
        self.idInt = None

    # Clears instance variables
    def clearData(self):
        self.userChannel = None
        self.user = None
        self.id = None
        self.idInt = None
        self.person = None

    # Generates the appropriate string based on your star and square frames
    def generateFrameString(self, starFrame, squareFrame):
        starFrameMessage = ""
        if starFrame != -1:
            starFrameMessage = str(starFrame + 1)
        else:
            starFrameMessage = "Shiny frame greater than 10000! Try again :("

        squareFrameMessage = ""
        if squareFrame != -1:
            squareFrameMessage = str(squareFrame + 1)
        else:
            squareFrameMessage = "Shiny frame greater than 10000! Try again :("

        return starFrameMessage, squareFrameMessage

    # Reports how many people are in the queue
    @commands.command(name="CheckQueueSize")
    async def checkQueueSize(self, ctx):
        await ctx.send("Current queue size is: " + str(q.size()))

    # Reports where the sender is in the queue
    @commands.command(name="CheckMyPlace")
    async def checkMyPlace(self, ctx):
        global q
        id = ctx.message.author.id
        p = Person(id, ctx.message.channel, ctx.message.author)
        place = q.indexOf(p) + 1

        if place > 0:
            await p.send(
                "```python\nHi there! You are currently at the place "
                + place
                + ".\n```"
            )
        else:
            await p.send("```python\nSorry but you're not in the queue right now.\n```")

    @commands.command(name="CheckMySeed")
    async def checkMySeed(self, ctx):
        global q

        if q.availableSpace():
            print(
                "Invoked by: "
                + str(ctx.message.author)
                + " in: "
                + str(ctx.message.guild)
            )
            if ctx.message.guild != None:

                # Constructs person object for queue
                id = ctx.message.author.id
                p = Person(id, ctx.message.channel, ctx.message.author)

                # Checks if queue already contains assets from the constructed person object
                if not q.contains(p) and self.idInt != id:

                    # Checks if anyone is currently being served
                    if self.person == None:
                        q.enqueue(p)
                        await ctx.send(
                            "<@"
                            + str(id)
                            + ">"
                            + f" {BOT_NAME} bot dispatched, I will ping you once I start searching! There are currently no people ahead of you"
                        )

                    # Checks if you are already being served
                    elif self.person.getID() != id:
                        q.enqueue(p)

                        # for correct grammar
                        prsn = ""
                        pre = ""
                        if q.size() == 1:
                            prsn = " person "
                            pre = " is "
                        else:
                            prsn = " people "
                            pre = " are "

                        await ctx.send(
                            "<@"
                            + str(id)
                            + ">"
                            + f" {BOT_NAME} bot dispatched, I will ping you once I start searching! There"
                            + pre
                            + "currently "
                            + str(q.size())
                            + prsn
                            + "waiting in front of you."
                        )
                    elif self.person.getID() == id:
                        await ctx.send("You are already being served, please wait!")
                else:
                    await ctx.send(
                        "You are already in line! Please wait until I ping you for your turn."
                    )
        else:
            await ctx.send(
                "The queue is already full! Please wait a while before trying to register."
            )

    # Main loop that is sending and receiving data from the dudu client
    @tasks.loop(seconds=0.1)
    async def checkDataReady(self):
        global q

        # If there is no person being served and the queue is not empty, get the next person in the queue
        # and start the dudu client
        if self.person == None and not q.isEmpty():
            self.person = q.dequeue()
            print("Current person being served: " + str(self.person.getUser()))
            initializeDuduClient()

        # Checks if lanturn is now searching and if there is a person being served
        if checkSearchStatus() and self.person != None:

            # assigns assets based on the person being served
            self.userChannel = self.person.getUserChannel()
            self.user = self.person.getUser()
            self.id = self.person.getIDString()
            self.idInt = self.person.getID()

            # Gets link code from text file
            code = getCodeString()

            await self.userChannel.send(
                self.id
                + f" I am now searching! I have sent your unique link code as a private message. My IGN is: {settings.get_settings().ign}."
            )
            await self.user.send(
                "```python\nHi there! Your private link code is: "
                + code
                + "\nPlease use it to match up with me in trade!```"
            )

        # Check if user has timed out and checks if a valid userChannel is present
        if checkTimeOut() and self.userChannel != None:
            await self.userChannel.send(
                self.id
                + " You have been timed out! You either took too long to respond or you lost connection. People remaining in line: "
                + str(q.size())
            )
            self.clearData()

        # Check if a valid user channel is present and if the dudu client is still running
        if self.userChannel != None and not checkDuduStatus():
            time.sleep(2.0)
            ec, pid, seed, ivs, iv = getPokeData()

            if seed != -1:
                calc = framecalc(seed)
                starFrame, squareFrame = calc.getShinyFrames()

                starFrameMessage, squareFrameMessage = self.generateFrameString(
                    starFrame, squareFrame
                )

                await self.userChannel.send(
                    self.id
                    + "```python\nEncryption Constant: "
                    + str(hex(ec))
                    + "\nPID: "
                    + str(hex(pid))
                    + "\nSeed: "
                    + seed
                    + "\nAmount of IVs: "
                    + str(ivs)
                    + "\nIVs: "
                    + str(iv[0])
                    + "/"
                    + str(iv[1])
                    + "/"
                    + str(iv[2])
                    + "/"
                    + str(iv[3])
                    + "/"
                    + str(iv[4])
                    + "/"
                    + str(iv[5])
                    + "\nStar Shiny at Frame: "
                    + starFrameMessage
                    + "\nSquare Shiny at Frame: "
                    + squareFrameMessage
                    + "```"
                )

                # outputs how many people remain in line
                time.sleep(1.0)
                await self.userChannel.send(
                    "People remaining in line: " + str(q.size())
                )
                self.clearData()
            else:
                await self.userChannel.send(
                    "Invalid seed. Please try a different Pokemon. People remaining in line: "
                    + str(q.size())
                )
                self.clearData()

        # await ctx.send("Invoked")

    @commands.command(name="GetSeed")
    async def obtainSeed(self, ctx, arg1=None, arg2=None, arg3=None):
        try:
            # Convert user strings to a usable format (int)
            ec = int(arg1, 16)
            pid = int(arg2, 16)
            ivs = [int(iv) for iv in arg3.split("/")]

            # Generate seed from user input
            gen = seedgen()
            seed, ivs = gen.search(ec, pid, ivs)

            # Calculate star and square shiny frames based on seed
            calc = framecalc(seed)
            starFrame, squareFrame = calc.getShinyFrames()

            # Format message based on result and output
            starFrameMessage, squareFrameMessage = self.generateFrameString(
                starFrame, squareFrame
            )

            await ctx.send(
                "```python\nRaid seed: "
                + str(seed)
                + "\nAmount of IVs: "
                + str(ivs)
                + "\nStar Shiny at Frame: "
                + starFrameMessage
                + "\nSquare Shiny at Frame: "
                + squareFrameMessage
                + "```"
            )
        except:
            await ctx.send(
                "Please format your input as: ```$GetSeed [Encryption Constant] [PID] [IVs as HP/Atk/Def/SpA/SpD/Spe]```"
            )

    @commands.command(name="GetFrameData")
    async def obtainFrameData(self, ctx, arg1=None):
        try:
            # Convert user strings to a usable format
            seed = hex(int(arg1, 16))

            # Calculate star and square shiny frames based on seed
            calc = framecalc(seed)
            starFrame, squareFrame = calc.getShinyFrames()

            # Format message based on result and output
            starFrameMessage, squareFrameMessage = self.generateFrameString(
                starFrame, squareFrame
            )

            await ctx.send(
                "```python\nFor Seed: "
                + str(seed)
                + "\nStar Shiny at Frame: "
                + starFrameMessage
                + "\nSquare Shiny at Frame: "
                + squareFrameMessage
                + "```"
            )
        except:
            await ctx.send("```$GetFrameData [Input your Seed]```")


def setup(client):
    client.add_cog(RaidCommands(client))
