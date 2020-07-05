# Script for creating Ladder Manager compatible Zip archives.

import os
import argparse


import sub_module  # Important, do not remove!
from version import update_version_txt
from bot_loader import LadderZip

root_dir = os.path.dirname(os.path.abspath(__file__))

# Files or folders common to all bots.
common = [
    (os.path.join("sharpy-sc2", "jsonpickle"), "jsonpickle"),
    (os.path.join("sharpy-sc2", "sharpy"), "sharpy"),
    (os.path.join("sharpy-sc2", "python-sc2", "sc2"), "sc2"),
    (os.path.join("sharpy-sc2", "sc2pathlibp"), "sc2pathlibp"),
    ("requirements.txt", None),
    ("version.txt", None),
    (os.path.join("sharpy-sc2", "config.py"), "config.py"),
    ("config.ini", None),
    (os.path.join("sharpy-sc2", "ladder.py"), "ladder.py"),
    ("ladderbots.json", None),
]

# Files or folders to be ignored from the archive.
ignored = [
    "__pycache__",
]


protoss_zip = LadderZip(
    "ProtossSharpyExample", "Protoss", [("protossbot", None), (os.path.join("protossbot", "run.py"), "run.py")], common
)


zip_types = {
    "protoss": protoss_zip,
    # All
    "all": None,
}


def main():
    zip_keys = list(zip_types.keys())
    parser = argparse.ArgumentParser(
        description="Create a Ladder Manager ready zip archive for SC2 AI, AI Arena, Probots, ..."
    )
    parser.add_argument("-n", "--name", help=f"Bot name: {zip_keys}.")
    parser.add_argument("-e", "--exe", help="Also make executable (Requires pyinstaller)", action="store_true")
    args = parser.parse_args()

    bot_name = args.name

    if not os.path.exists("dummy"):
        os.mkdir("dummy")

    update_version_txt()

    if bot_name == "all" or not bot_name:
        zip_keys.remove("all")
        for key in zip_keys:
            zip_types.get(key).create_ladder_zip(args.exe)
    else:
        if bot_name not in zip_keys:
            raise ValueError(f"Unknown bot: {bot_name}, allowed values are: {zip_keys}")

        zip_types.get(bot_name).create_ladder_zip(args.exe)


if __name__ == "__main__":
    main()
