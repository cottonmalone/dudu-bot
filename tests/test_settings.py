from settings import *

EXPECTED_SETTINGS = Settings(
    token="token", admin_id=666, bot_name="EvilFucker", switch_address="127.0.0.1"
)


def test_settings_load_correctly():
    assert get_settings("tests/data/settings.yaml") == EXPECTED_SETTINGS
