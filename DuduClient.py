#These are the comments provided by olliz0r. These may be useful if you need to calibrate for other languages
#Commands:
#make sure to append \r\n to the end of the command string or the switch args parser might not work
#responses end with a \n (only poke has a response atm)

#click A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE
#press A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE
#release A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE

#peek <address in hex, prefaced by 0x> <amount of bytes, dec or hex with 0x>
#poke <address in hex, prefaced by 0x> <data, if in hex prefaced with 0x>

#setStick LEFT/RIGHT <xVal from -0x8000 to 0x7FFF> <yVal from -0x8000 to 0x7FFF


import socket
import time
import binascii
import struct
from PK8 import *
from NumpadInterpreter import *

#Get yuor switch IP from the system settings under the internet tab
#Should be listed under "Connection Status" as 'IP Address'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("YOUR SWITCH IP HERE", 6000))
code = ""

def bytesToInt(bytedata, length):
        data = list()
        j = 0
        while j < length:
            data.append(bytedata[j])
            j += 1
        return data

def sendCommand(s, content):
    content += '\r\n' #important for the parser on the switch side
    s.sendall(content.encode())

#Cleans out the file relied for communication
def cleanEnvironment():
    fileOut = open("communicate.bin", "wb")
    outData = list()
    outData.append(0)
    outData.append(0)
    outData.append(0)
    fileOut.write(bytes(outData))
    fileOut.close()

#Writes timeout flag to file
def timedOut():
    fileOut = open("communicate.bin", "wb")
    outData = list()
    outData.append(0)
    outData.append(0)
    outData.append(1)
    fileOut.write(bytes(outData))
    fileOut.close()

#Interprets sequence of strings in arraylist
def interpretStringList(arr):
    length = len(arr)
    i = 0
    while i < length:
        sendCommand(s, arr[i])
        i+=1
        time.sleep(2.0)

#Calibrated for games set to english
#Will exit the trade once the timeout period is reached
def timeOutTradeSearch():
    sendCommand(s, "click Y")
    time.sleep(1.0)
    sendCommand(s, "click A");
    time.sleep(1.0)
    sendCommand(s, "click A");
    time.sleep(1.5)
    sendCommand(s, "click A");
    time.sleep(1.5)
    sendCommand(s, "click A");
    time.sleep(1.5)
    sendCommand(s, "click A");
    time.sleep(1.5)

    #uncomment if you are using in Japanese
    #sendCommand(s, "click A");
    #time.sleep(1.5)
    sendCommand(s, "click B");
    time.sleep(1.5)
    sendCommand(s, "click B");
    time.sleep(1.5)

#Exits trade if a disconnection occured
#or if the player refused to input a pokemon
def exitTrade():
    sendCommand(s, "click B")
    time.sleep(1.0)
    sendCommand(s, "click A")
    time.sleep(1.0)

#Calibrated for games set to english
#Starts up trade and inputs code
def initiateTrade():
    global code

    #Gets to the code input menu
    sendCommand(s, "click Y")
    time.sleep(1.0)
    sendCommand(s, "click A");
    time.sleep(1.0)
    sendCommand(s, "click DDOWN")
    time.sleep(2.5)
    sendCommand(s, "click A")
    time.sleep(1.5)
    sendCommand(s, "click A")
    time.sleep(1.5)

    #uncomment if you are using in Japanese
    #sendCommand(s, "click A")
    #time.sleep(1.5)


    #Get passcode button sequence and input them
    #Pass None if you want your code randomly generated
    #Pass in a 4 digit number not containing any zeros for a fixed code
    datalist, code = getButtons(4321)
    interpretStringList(datalist)

    #Confirm passcode and exit the menu
    sendCommand(s, "click PLUS")
    time.sleep(2.0)
    sendCommand(s, "click A")
    time.sleep(1.5)
    sendCommand(s, "click A")
    time.sleep(1.5)
    sendCommand(s, "click A")
    time.sleep(1.5)
    sendCommand(s, "click A")
    time.sleep(1.5)

    #Just to be safe since this is a very important part
    sendCommand(s, f"poke 0x2E32209A 0x00000000")
    time.sleep(0.5)
    sendCommand(s, f"poke 0x2E32209A 0x00000000")
    time.sleep(0.5)
    sendCommand(s, f"poke 0x2E322064 0x00000000")
    time.sleep(0.5)
    sendCommand(s, f"poke 0x2E322064 0x00000000")
    time.sleep(0.5)

#Start up program and clean up necessary files
print("Cleaning environment...")
cleanEnvironment()
print("Environment cleaned!")
print("Awaiting inputs...")
while True:
    fileIn = open("communicate.bin", "rb")
    fileIn.seek(0)
    tradeState = int(fileIn.read()[0])
    
    if tradeState == 1:
        print("Bot initialized!")
        fileIn.close()
        initiateTrade()

        fcode = open("code.txt", "w")
        fcode.write(code)
        fcode.close()
        
        fileOut = open("communicate.bin", "wb")

        outData = list()
        outData.append(0)
        outData.append(1)
        outData.append(0)

        fileOut.write(bytes(outData))
        fileOut.close()

        canTrade = True

        start = time.time()
        while True:
            sendCommand(s, "peek 0x2E322064 4")
            time.sleep(0.5)
            tradeCheck = s.recv(689)
            tradeCheck = binascii.unhexlify(tradeCheck[0:-1])
            tradeCheck = int(struct.unpack("I", tradeCheck[0:4])[0])
            end = time.time()
            if tradeCheck != 0:
                print("Trade Started!")
                canTrade = True
                break
            if (end - start) >= 60:
                timeOutTradeSearch()
                timedOut()
                canTrade = False
                break
        if canTrade:
            start = time.time()
            while True:
                sendCommand(s, "peek 0x2E32209A 4")
                time.sleep(0.5)
                memCheck = s.recv(689)
                memCheck = binascii.unhexlify(memCheck[0:-1])
                memCheck = int(struct.unpack("I", memCheck[0:4])[0])

                end = time.time()
                if memCheck != 0:
                    canTrade = True
                    break
                if (end - start) >= 40:
                    exitTrade()
                    timedOut()
                    canTrade = False
                    break

            
            if canTrade:
                exitTrade()
                sendCommand(s, "peek 0x2E32206A 328")
                time.sleep(0.5)

                ek8 = s.recv(689)
                ek8 = binascii.unhexlify(ek8[0:-1])
                data = bytesToInt(ek8, 0x148)
                decryptor = PK8(data)
                decryptor.decrypt()
                pk8 = decryptor.getData()

                ec = decryptor.getEncryptionConstant()
                pid = decryptor.getPID()
                

                pk8Out = open("out.pk8", "wb")
                pk8Out.write(bytes(pk8))
                pk8Out.close()

                fileOut = open("communicate.bin", "wb")
                outData = list()
                outData.append(0)
                outData.append(0)
                outData.append(0)
                fileOut.write(bytes(outData))
                fileOut.close()

                print("Encryption Constant: " + str(hex(ec)))
                print("pid: " + str(hex(pid)))

        print("Awaiting...")
    time.sleep(1.0)