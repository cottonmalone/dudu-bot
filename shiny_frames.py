import collections
from XoroShiro import XoroShiro
from enum import Enum, auto

ShinyFrame = collections.namedtuple(
    "ShinyFrame", ["position", "type", "ivs", "ability"]
)


class ShinyType(Enum):
    NONE = auto()
    STAR = auto()
    SQUARE = auto()


def get_shiny_xor(val):
    return (val >> 16) ^ (val & 0xFFFF)


def get_shiny_type(pid, sidtid):
    p = get_shiny_xor(pid)
    t = get_shiny_xor(sidtid)

    if p == t:
        return ShinyType.SQUARE

    if (p ^ t) < 0x10:
        return ShinyType.STAR

    return ShinyType.NONE


def get_ivs_for_frame(rng, n_best_ivs):

    ivs = [-1] * 6
    count, n_ivs, offset = 0, n_best_ivs, -n_best_ivs

    while count < n_ivs:
        stat, offset = rng.next_int(7, 6, offset)

        if ivs[stat] == -1:
            ivs[stat] = 31
            count += 1

    for x in range(0, 6):
        if ivs[x] != 31:
            ivs[x] = rng.next_int(31)

    return ivs


def get_shiny_frames(seed, n_best_ivs=4, max_frames=10000):
    seed = int(seed, 16)
    rng = XoroShiro(seed)

    frames = []

    for i in range(1, max_frames + 1):
        # ignore characteristics
        _ = rng.next_int(0xFFFFFFFF, 0xFFFFFFFF)

        SIDTID = rng.next_int(0xFFFFFFFF, 0xFFFFFFFF)
        PID = rng.next_int(0xFFFFFFFF, 0xFFFFFFFF)

        shiny_type = get_shiny_type(PID, SIDTID)

        if shiny_type != ShinyType.NONE:
            frames.append(
                ShinyFrame(
                    position=i,
                    type=shiny_type,
                    ivs=get_ivs_for_frame(rng, n_best_ivs),
                    ability=rng.next_int(3, 3) + 1,
                )
            )

        rng.reset(seed)
        seed = rng.next()
        rng.reset(seed)

    return frames
