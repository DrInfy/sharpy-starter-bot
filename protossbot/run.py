from ladder import run_ladder_game

from sc2 import Race
from sc2.player import Bot
from protossbot.bot import ProtossBot

zerg_bot = Bot(Race.Protoss, ProtossBot())


def main():
    # Ladder game started by LadderManager
    print("Starting ladder game...")
    result, opponentid = run_ladder_game(zerg_bot)
    print(result, " against opponent ", opponentid)


if __name__ == '__main__':
    main()
