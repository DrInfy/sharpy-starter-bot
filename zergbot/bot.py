from typing import List, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sharpy.combat.group_combat_manager import GroupCombatManager
from sharpy.knowledges import SkeletonBot
from sharpy.managers.core import *
from sharpy.managers.extensions import MemoryManager
from sharpy.plans.zerg import *



class ZergBot(SkeletonBot):
    cache: UnitCacheManager
    zone_manager: ZoneManager

    def __init__(self):
        self.attack_started = False
        super().__init__("Zerg Template")

    def configure_managers(self) -> Optional[List[ManagerBase]]:
        self.cache = UnitCacheManager()
        self.zone_manager = ZoneManager()
        return [
            MemoryManager(),
            PreviousUnitsManager(),
            LostUnitsManager(),
            EnemyUnitsManager(),
            self.cache,
            UnitValue(),
            UnitRoleManager(),
            PathingManager(),
            self.zone_manager,
            BuildingSolver(),
            IncomeCalculator(),
            CooldownManager(),
            GroupCombatManager(),
            GatherPointSolver(),
            ActManager(self.create_plan()),
        ]

    def create_plan(self) -> ActBase:
        return CounterTerranTie([
                Expand(1),  # expand if we run out of minerals in main
                AutoOverLord(),
                ZergUnit(UnitTypeId.DRONE, 16),
                GridBuilding(UnitTypeId.SPAWNINGPOOL, 1),
                ZergUnit(UnitTypeId.ZERGLING),
                ZergUnit(UnitTypeId.QUEEN, to_count=1),
                Expand(2),  # expand again if we have too many minerals
                DistributeWorkers(),
                InjectLarva()
            ]
        )

    async def execute(self):
        # Your custom logic here
        if not self.attack_started and len(self.cache.own(UnitTypeId.ZERGLING)) > 5:
            self.attack_started = True
        if self.attack_started:
            for ling in self.cache.own(UnitTypeId.ZERGLING):
                ling.attack(self.zone_manager.enemy_start_location)

