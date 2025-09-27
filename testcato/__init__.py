# Package metadata for wheel
__title__ = "testcato"
__version__ = "1.2.5"

# Automatically create config file if not present
import os
import shutil


def _ensure_config():
    config_name = "testcato_config.yaml"
    config_src = os.path.join(os.path.dirname(__file__), "..", config_name)
    config_dst = os.path.join(os.getcwd(), config_name)
    if not os.path.exists(config_dst):
        if os.path.exists(config_src):
            shutil.copyfile(config_src, config_dst)


_ensure_config()
