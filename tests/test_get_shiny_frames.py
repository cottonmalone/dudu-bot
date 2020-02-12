from shiny_frames import *

SEED = "58360e4ebf462e4a"

SHINY_FRAMES = [
    ShinyFrame(
        position=1461, type=ShinyType.STAR, ivs=[31, 15, 10, 31, 31, 31], ability=3
    ),
    ShinyFrame(
        position=6802, type=ShinyType.STAR, ivs=[21, 31, 31, 31, 31, 31], ability=2
    ),
    ShinyFrame(
        position=7465, type=ShinyType.STAR, ivs=[31, 31, 11, 31, 30, 31], ability=2
    ),
]


def test_get_shiny_frames():
    assert get_shiny_frames(SEED) == SHINY_FRAMES
