from csv import reader
import os

# folder of this file, so '../maps/...' works no matter where it is launched from
CODE_DIR = os.path.dirname(os.path.abspath(__file__))

def import_csv_layout(path):
    terrain_map = []
    with open(os.path.join(CODE_DIR, path)) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
