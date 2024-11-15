import backendTools.points as points
import backendTools.globals as globals

# neatly package the correct points methods as executable
points.scoreAdjust()
output = points.map_to_json(globals.summoners)
points.save_state(output)