FPS = 60
TILESIZE = 64

# оружия
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': '../graphics/weapons/sword/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': '../graphics/weapons/axe/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': '../graphics/weapons/lance/full.png'}
}


# stats background color
STATS_BG_COLOR = (0, 0, 0)

# HP UI
HP_POS = (TILESIZE // 4, TILESIZE // 2)
HP_WIDTH = TILESIZE * 3
HP_HEIGHT = TILESIZE // 3
HP_COLOR = (0, 153, 0)

# MP UI
MP_POS = (HP_POS[0], HP_POS[1] + HP_HEIGHT + TILESIZE // 10)
MP_WIDTH = TILESIZE * 2
MP_HEIGHT = TILESIZE // 4
MP_COLOR = (139, 0, 255)
