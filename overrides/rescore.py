import sys
from pathlib import Path
parent_path = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_path))

import backendTools.points as points
import backendTools.globals as globals
import firebase.firebaseTools as firebaseTools

# neatly package the correct points methods as executable
points.scoreAdjust()
output = points.map_to_json(globals.summoners)
firebaseTools.fb.storeData(output)