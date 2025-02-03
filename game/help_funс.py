def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.split() for line in mapFile]
    return level_map


def next_level(lvl):
    return load_level(f'level_{lvl}.txt')


def draw_text(screen, text, font, t_color, x, y):
    txt = font.render(text, True, t_color)
    screen.blit(txt, (x, y))
