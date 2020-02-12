import functools
import collections
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

DEFAULT_SETTINGS_FILE_PATH = "settings.yaml"


Settings = collections.namedtuple(
    "Settings", ["token", "admin_id", "bot_name", "switch_address", "ign"]
)


@functools.lru_cache(maxsize=None)
def get_settings(file_path=DEFAULT_SETTINGS_FILE_PATH):
    with open(file_path, "r") as file:
        return Settings(**yaml.load(file, Loader=Loader))
