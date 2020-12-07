from random import choice
from typing import Callable, Tuple, List, Dict, Optional

from sc2 import UnitTypeId
from sharpy.knowledges import KnowledgeBot
from sharpy.managers import ManagerBase

# This imports all the usual components for protoss bots
from sharpy.managers.extensions import DataManager, BuildDetector
from sharpy.plans.protoss import *

# This imports all the usual components for terran bots
# from sharpy.plans.terran import *

# This imports all the usual components for zerg bots
# from sharpy.plans.zerg import *

class ProtossBot(KnowledgeBot):
    data_manager: DataManager

    def __init__(self, build_name: str = "default"):
        super().__init__("ProtossSharpyExample")

        self.conceded = False

        self.builds: Dict[str, Callable[[], BuildOrder]] = {
            "zealots": lambda: self.zealot_build(),
            "sentries": lambda: self.sentry_build(),
        }
        self.build_name = build_name

    def configure_managers(self) -> Optional[List[ManagerBase]]:
        # self.knowledge.roles.role_count = 11

        # Return your custom managers here:
        return [BuildDetector()]

    async def create_plan(self) -> BuildOrder:
        if self.build_name == "default":
            self.build_name = choice(list(self.builds.keys()))

        self.data_manager.set_build(self.build_name)
        return self.builds[self.build_name]()

    async def on_step(self, iteration):
        # Optional way to leave the game when losing
        await self.give_up()
        return await super().on_step(iteration)

    async def give_up(self):
        if not self.conceded and self.game_analyzer.been_predicting_defeat_for > 5:
            # sc2ai phrase for leaving the game safely
            await self.chat_send("pineapple")
            self.conceded = True

        if self.conceded and self.game_analyzer.been_predicting_defeat_for > 10:
            # Leave the game
            await self.client.leave()

    def zealot_build(self) -> BuildOrder:
        # Builds 2 gates and endless wave of zealots
        return BuildOrder(
            Workers(16),
            ChronoBuilding(UnitTypeId.GATEWAY),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=1, priority=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
            Step(UnitExists(UnitTypeId.GATEWAY), AutoPylon()),
            ProtossUnit(unit_type=UnitTypeId.ZEALOT),
            self.create_common_strategy()
        )

    def sentry_build(self) -> BuildOrder:
        return BuildOrder(
            Workers(16),
            ChronoBuilding(UnitTypeId.GATEWAY),
            GridBuilding(unit_type=UnitTypeId.PYLON, to_count=1, priority=True),
            GridBuilding(unit_type=UnitTypeId.GATEWAY, to_count=2, priority=True),
            Step(UnitExists(UnitTypeId.GATEWAY), AutoPylon()),
            BuildGas(20),
            AutoWorker(),
            ProtossUnit(unit_type=UnitTypeId.SENTRY, priority=True),
            Expand(10),
            self.create_common_strategy()
        )

    def create_common_strategy(self) -> SequentialList:
         return SequentialList(
             # Sets workers to work
             DistributeWorkers(),
             # Detects enemy units as hallucinations
             PlanHallucination(),
             # Scouts with phoenixes
             HallucinatedPhoenixScout(time_interval=60),
             # Cancels buildings that are about to go down
             PlanCancelBuilding(),
             # Set worker rally point
             WorkerRallyPoint(),
             # Have the combat units gather in one place
             PlanZoneGather(),
             # Defend
             PlanZoneDefense(),
             # Attack, these 2 should be last in a sequential list in this order
             PlanZoneAttack(),
             PlanFinishEnemy(),
         )
