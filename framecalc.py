from XoroShiro import *


class framecalc:
    XC = int("82A2B175229D6A5B", 16)
    MASK = int("FFFFFFFFFFFFFFFF", 16)

    def __init__(self, seed):
        self.seed = int(seed, 16)

    def getShinyXOR(self, val):
        return (val >> 16) ^ (val & 0xFFFF)

    def getShinyValue(self, num):
        return self.getShinyXOR(num) >> 4

    def getShinyType(self, pid, tisid):
        p = self.getShinyXOR(pid)
        t = self.getShinyXOR(tisid)
        if p == t:
            return 2  # square shiny
        if (p ^ t) < 0x10:
            return 1  # star shiny
        return 0

    # WIP
    def isHiddenAbility(self, rng):
        return rng.nextInt((3 & 0xFFFFFFFF), (3 & 0xFFFFFFFF))

    def getShinyFrames(self):
        print(f"{self.seed}")
        seed = self.seed
        rng = XoroShiro(seed)
        starFrame = -1
        squareFrame = -1

        i = 1
        while True:
            a = rng.nextInt(0xFFFFFFFF, 0xFFFFFFFF)
            SIDTID = rng.nextInt(0xFFFFFFFF, 0xFFFFFFFF)
            PID = rng.nextInt(0xFFFFFFFF, 0xFFFFFFFF)

            shinyType = self.getShinyType(PID, SIDTID)

            if starFrame == -1 and shinyType == 1:
                starFrame = i

            if squareFrame == -1 and shinyType == 2:
                squareFrame = i

            rng.reset(seed)
            seed = rng.next()
            rng.reset(seed)
            i += 1

            if starFrame != -1 and squareFrame != -1:
                return starFrame, squareFrame

            if i >= 10000:
                return starFrame, squareFrame

    def getShinyFramesInfo(self):
        seed = self.seed
        rng = XoroShiro(seed)

        for i in range(1, 10001):
            _ = rng.nextInt(0xFFFFFFFF, 0xFFFFFFFF)
            SIDTID = rng.nextInt(0xFFFFFFFF, 0xFFFFFFFF)
            PID = rng.nextInt(0xFFFFFFFF, 0xFFFFFFFF)

            shinyType = self.getShinyType(PID, SIDTID)

            if shinyType > 0:
                print(f"{i}: {shinyType}")

                ivs = [-1] * 6
                count, n_ivs, offset = 0, 4, -4

                while count < n_ivs:
                    stat, offset = rng.nextIntWithOffser(6, 7, offset)

                    if ivs[stat] == -1:
                        ivs[stat] = 31
                        count += 1

                for x in range(0, 6):
                    if ivs[x] != 31:
                        ivs[x] = rng.next_with_mask(31)

                print(ivs, rng.nextInt(3, 3) + 1)

            rng.reset(seed)
            seed = rng.next()
            rng.reset(seed)
