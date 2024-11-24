import sys
from pathlib import Path
parent_path = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_path))

import firebase.firebaseTools as firebaseTools
import json




mypoints = firebaseTools.fb.loadData()

print("Writing to file")
with open("saved_points_real.json", "w") as file:
    json.dump(mypoints, file, indent=4)
print("Points written to saved_points.json")