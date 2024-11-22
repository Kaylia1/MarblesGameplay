import sys
from pathlib import Path
parent_path = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_path))

import firebase.firebaseTools as firebaseTools
import json

json_data = {}
with open("saved_points_real.json", "r") as file:
    json_data = json.load(file)

# confirm
firebaseTools.fb.storeData(json_data)
print(firebaseTools.fb.loadData())