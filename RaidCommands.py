from discord.ext import tasks, commands
import discord
from framecalc import *
from seedgen import *
from GetPokeInfo import *
from bot import *
from Person import *
from ArrayQueue import *
import time

q = ArrayQueue()

class RaidCommands(commands.Cog):
	def __init__(self, client):
		self.checkDataReady.start()
		self.userChannel = None
		self.user = None
		self.id = None
		self.person = None
		self.idInt = None

	#Queues up person if they are not already in the queue to initiate searching
	@commands.command(name="CheckMySeed")
	async def checkMySeed(self, ctx):
		global q
		if ctx.message.guild != None:
			id = ctx.message.author.id
			userChannel = ctx.message.channel
			user = ctx.message.author
			p = Person(id, userChannel, user)
			
			if not q.contains(p) and self.idInt != id:
				size = q.size()
				if size <= 10 and self.person == None:
					q.enqueue(p)
					await ctx.send("Lanturn bot dispatched, I will ping you once I start searching! There are currently no people ahead of you")
				elif size <= 10 and self.person.getID() != id:
					q.enqueue(p)
					prsn = ""
					pre = ""
					if q.size() == 1:
						prsn = " person "
						pre = " is "
					else:
						prsn = " people "
						pre = " are "
					await ctx.send("Lanturn bot dispatched, I will ping you once I start searching! There" + pre + "currently " + str(q.size()) + prsn + "waiting in front of you.")
				elif size <= 10 and self.person.getID() == id:
					await ctx.send("You are already being served, please wait!")
				else:
					await ctx.send("The queue is already full! Please wait a while before trying to register.")
			else:
				await ctx.send("You are already in line! Please wait until I ping you for your turn.")

	#Handles all of the dudu logic. Very messy, but it does work well. I suggest not messing unless you know what you're doing
	@tasks.loop(seconds=0.1)
	async def checkDataReady(self):
		global q
		if not q.isEmpty() and self.person == None:
			self.person = q.dequeue()
			initializeDuduClient()
		if checkSearchStatus() == 1 and self.person != None:
			self.userChannel = self.person.getUserChannel()
			self.user = self.person.getUser()
			self.id = self.person.getIDString()
			self.idInt = self.person.getID()
			
			code = getCodeString()

			#Change <placeholder> with the IGN of the switch you're using
			await self.userChannel.send(self.id + " I am now searching! I have sent your unique link code as a private message. My in game name is: <placeholder>")
			await self.user.send("```python\nHi there! Your private link code is: " + code + "\nPlease use it to match up with me in trade!```")

		if checkTimeOut() and self.userChannel != None:
			await self.userChannel.send(self.id + " You have been timed out! You either took too long to respond or you lost connection. You have been dequeued.")
			self.userChannel = None
			self.user = None
			self.id = None
			self.idInt = None
			self.person = None

		if checkDuduStatus() == False and self.userChannel != None:
			time.sleep(2.0)
			ec, pid, seed, ivs, iv = getPokeData()

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

				await self.userChannel.send(self.id + "```python\nEncryption Constant: " + str(hex(ec)) +
					"\nPID: " + str(hex(pid)) +
					"\nSeed: " + seed +
					"\nAmount of IVs: " + str(ivs) +  
					"\nIVs: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
					"\nStar Shiny at Frame: " + starFrameMessage +
					"\nSquare Shiny at Frame: " + squareFrameMessage + "```")
				self.userChannel = None
				self.user = None
				self.id = None
				self.person = None
				self.idInt = None
			else:
				await self.userChannel.send("Invalid seed. Please try a different Pokemon.")
				self.userChannel = None
				self.user = None
				self.id = None
				self.person = None
				self.idInt = None

			
		#await ctx.send("Invoked")

	#This is for people who have their encryption constant, IVs, and pid.
	#This will derive a seed and frame data based on that info
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

	#Will get a user's frame data based on their seed
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