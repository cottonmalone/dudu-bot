from discord.ext import commands
import discord
from framecalc import *
from SwitchClient import *
from seedgen import *

class RaidCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='GetPoke')
    async def getPoke(self, ctx):
        switch = SwitchClient()
        check, ec, pid, IV1, IV2, IV3, IV4, IV5, IV6 = switch.connectToSwitch()
        if check != -1:
            ivs = [IV1, IV2, IV3, IV4, IV5, IV6]
            gen = seedgen()
            seed, ivs = gen.search(ec, pid, ivs)
            if seed != -1:

                calc = framecalc(seed)
                starFrame = calc.getStarShinyFrame()
                squareFrame = calc.getSquareShinyFrame()


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

                await ctx.send("```python\nEncryption Constant: " + str(hex(ec)) +
                    "\nPID: " + str(hex(pid)) +
                    "\nSeed: " + seed +
                    "\nAmount of IVs: " + str(ivs) +  
                    "\nIVs: " + str(IV1) + "/" + str(IV2) + "/" + str(IV3) + "/" + str(IV4) + "/" + str(IV5) + "/" + str(IV6) + 
                    "\nStar Shiny at Frame: " + starFrameMessage +
                    "\nSquare Shiny at Frame: " + squareFrameMessage + "```")
            else:
                await ctx.send("Invalid seed. Please try a different Pokemon.")
        else:
            await ctx.send("Unable to connect to switch!")

    @commands.command(name='GetSeed')
    async def obtainSeed(self, ctx, arg1=None, arg2=None, arg3=None):
        try:
            #Convert user strings to a usable format (int)
            ec = int(arg1, 16)
            pid = int(arg2, 16)
            ivs = [ int(iv) for iv in arg3.split("/") ]

            #Generate seed from user input
            gen = seedgen()
            seed, ivs = gen.search(ec, pid, ivs)

            #Calculate star and square shiny frames based on seed
            calc = framecalc(seed)
            starFrame = calc.getStarShinyFrame()
            squareFrame = calc.getSquareShinyFrame()

            #Format message based on result and output
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

            await ctx.send("```python\nRaid seed: " + str(seed) + "\nAmount of IVs: " + str(ivs) + "\nStar Shiny at Frame: " + starFrameMessage + "\nSquare Shiny at Frame: " + squareFrameMessage + "```")
        except:
            await ctx.send("Please format your input as: ```$GetSeed [Encryption Constant] [PID] [IVs as HP/Atk/Def/SpA/SpD/Spe]```")

    @commands.command(name='GetFrameData')
    async def obtainFrameData(self, ctx, arg1=None):
    	try:
            #Convert user strings to a usable format
    		seed = hex(int(arg1, 16))

            #Calculate star and square shiny frames based on seed
    		calc = framecalc(seed)
    		starFrame= calc.getStarShinyFrame()
    		squareFrame= calc.getSquareShinyFrame()

            #Format message based on result and output
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

    		await ctx.send("```python\nFor Seed: " + str(seed) + "\nStar Shiny at Frame: " + starFrameMessage + "\nSquare Shiny at Frame: " + squareFrameMessage + "```")
    	except:
    		await ctx.send("```$GetFrameData [Input your Seed]```")
    	

def setup(client):
    client.add_cog(RaidCommands(client))