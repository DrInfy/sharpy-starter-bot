import os
import sys

# This file imports submodules correctly

if "sharpy-sc2" not in sys.path:
    sys.path.insert(1, "sharpy-sc2")

sc2_path = os.path.join("sharpy-sc2", "python-sc2")
if sc2_path not in sys.path:
    sys.path.insert(1, sc2_path)
