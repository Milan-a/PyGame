def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.split() for line in mapFile]
    return level_map


def next_level(lvl):
    return load_level(f'level_{lvl}.txt')
