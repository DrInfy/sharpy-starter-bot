from typing import List, Optional

from sc2.ids.unit_typeid import UnitTypeId
from sharpy.combat.group_combat_manager import GroupCombatManager
from sharpy.knowledges import SkeletonBot
from sharpy.managers import ManagerBase
from sharpy.managers.core import *
from sharpy.managers.extensions import MemoryManager
from sharpy.plans.terran import *



class TerranBot(SkeletonBot):
    def __init__(self):
        super().__init__("Terran Template")

    def configure_managers(self) -> Optional[List[ManagerBase]]:
        return [
            MemoryManager(),
            PreviousUnitsManager(),
            LostUnitsManager(),
            EnemyUnitsManager(),
            UnitCacheManager(),
            UnitValue(),
            UnitRoleManager(),
            PathingManager(),
            ZoneManager(),
            BuildingSolver(),
            IncomeCalculator(),
            CooldownManager(),
            GroupCombatManager(),
            GatherPointSolver(),
            ActManager(self.create_plan()),
        ]

    def create_plan(self) -> ActBase:
        return BuildOrder(
            Expand(1),  # expand if we run out of minerals in main
            AutoWorker(),
            AutoDepot(),
            TerranUnit(UnitTypeId.MARINE, priority=True),
            GridBuilding(UnitTypeId.BARRACKS, 5),
            DistributeWorkers(),
            LowerDepots(),
            # Have the combat units gather in one place
            PlanZoneGather(),
            # Defend
            PlanZoneDefense(),
            SequentialList(
                # Attack, these 2 should be last in a sequential list in this order
                PlanZoneAttack(5,),
                # Roam the map until last building is found.
                PlanFinishEnemy(),
            )
        )
