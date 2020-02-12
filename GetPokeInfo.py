import binascii
import struct
import time
from PK8 import *
from framecalc import *
from seedgen import *
from collections import namedtuple
import shiny_frames


def initializeDuduClient():
    try:
        # Checks flag if it's in use
        fileIn = open("communicate.bin", "rb")
        fileIn.seek(0)
        isInUse = int(fileIn.read()[0])
        fileIn.close()
        if isInUse == 1:
            return False

        outFlag = list()
        outFlag.append(1)
        outFlag.append(0)
        outFlag.append(0)

        fileOut = open("communicate.bin", "wb")
        fileOut.write(bytes(outFlag))
        fileOut.close()

        return True
    except:
        return False


def checkTimeOut():
    try:
        fileIn = open("communicate.bin", "rb")
        fileIn.seek(2)
        isInUse = int(fileIn.read()[0])
        fileIn.close()

        if isInUse == 1:
            fileOut = open("communicate.bin", "wb")
            outData = list()
            outData.append(0)
            outData.append(0)
            outData.append(0)
            fileOut.write(bytes(outData))
            fileOut.close()
            return True

        return False
    except:
        return False


def checkSearchStatus():
    try:
        fileIn = open("communicate.bin", "r+b")
        fileIn.seek(1)
        isInUse = int(fileIn.read()[0])
        if isInUse == 1:
            outData = list()
            outData.append(1)
            outData.append(0)
            fileIn.seek(0)
            fileIn.write(bytes(outData))
            fileIn.close()
            return 1

        return 0
    except:
        return 0


def getCodeString():
    while True:
        try:
            fileIn = open("code.txt", "r+")
            code = fileIn.readline()
            fileIn.close()
            return code
        except:
            print("File reading error occured, trying again!")


def checkDuduStatus():
    try:
        fileIn = open("communicate.bin", "rb")
        fileIn.seek(0)
        isInUse = int(fileIn.read()[0])
        fileIn.close()

        if isInUse == 1:
            return True
        else:
            return False
    except:
        return False


PokeData = namedtuple(
    "PokeData",
    [
        "name",
        "species",
        "nature",
        "gender",
        "ot",
        "ivs",
        "ec",
        "pid",
        "seed",
        "seed_found",
        "frames",
    ],
)

POKE_DATA_FILE_PATH = "out.pk8"


def getPokeData(file_path=POKE_DATA_FILE_PATH):
    with open(file_path, "rb") as file:
        data = PK8(file.read())

    pid = data.getPID()
    ec = data.getEncryptionConstant()

    IV1, IV2, IV3, IV4, IV5, IV6 = data.getIVs()
    ivs = [IV1, IV2, IV3, IV5, IV6, IV4]

    gen = seedgen()
    seed, _ = gen.search(ec, pid, ivs)

    seed_found = seed != -1

    seed_str, star_frame, square_frame = "", -1, -1

    if seed_found:
        seed_str = seed[2:]
        frames = shiny_frames.get_shiny_frames(seed)

    return PokeData(
        name=data.getPokemonName(),
        species=data.getSpecies(),
        nature=data.getNature(),
        gender=data.getGender(),
        ot=data.getOT(),
        ivs="/".join(map(str, ivs)),
        ec=hex(ec)[2:],
        pid=hex(pid)[2:],
        seed=seed_str,
        seed_found=seed_found,
        frames=frames,
    )


def get_frame_string(frame):

    if frame.type == shiny_frames.ShinyType.STAR:
        type = "\u2605"
    else:
        type = "\u25a1"

    ability = frame.ability

    if ability > 2:
        ability = "H"

    return (
        f" {frame.position:4} |   {type}  |"
        f"  {ability}  | {'/'.join(map(str, frame.ivs))}"
    )


def getPokeInfoString(file_path=POKE_DATA_FILE_PATH):
    data = getPokeData(file_path)

    if data.species != data.name:
        pokemon_name = f"{data.name} ({data.species})"
    else:
        pokemon_name = data.name

    info = [
        f"TRADED POKEMON INFO",
        f"==============================",
        f"Name      :: {pokemon_name}",
        f"OT        :: {data.ot}",
        f"Gender    :: {data.gender}",
        f"Nature    :: {data.nature}",
        f"IVs       :: {data.ivs}",
        f"EC        :: {data.ec}",
        f"PID       :: {data.pid}",
        f"\nDEN INFO",
        f"==============================",
    ]

    if data.seed_found:
        info.append(f"Seed      :: {data.seed}")

        if len(data.frames):
            info.append(f"\n--------------------------------------")
            info.append(f"Frame | Type | Ab. | IVs")
            info.append(f"--------------------------------------")
            info += [get_frame_string(frame) for frame in data.frames]

            info.append(f"\n* Shown stats are only for 4 IVs pokemon")
        else:
            info.append(f"\nThere are no shiny frames under 10000 frames.")

    else:
        info.append("This pokemon is not from a raid.")

    return "\n".join(info)
