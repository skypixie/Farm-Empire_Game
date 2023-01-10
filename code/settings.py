FPS = 60
TILESIZE = 64

PLAYER_SPEED = 5

# оружия
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': '../graphics/weapons/sword/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': '../graphics/weapons/axe/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': '../graphics/weapons/lance/full.png'}
}

# магия
magic_data = {
    'fire': {'cooldown': 100, 'strength': 100, 'cost': 30, 'graphic': '../graphics/particles/flame/fire.png'}
}

# враги
monster_data = {
    'frog': {'health': 200, 'damage': 30, 'attack_type': 'slash', 'attack_sound': '../audio/attack/Hit.wav', 'speed': 3, 'resistance': 3, 'attack_radius': TILESIZE * 2, 'notice_radius': TILESIZE * 4},
    'raccoon': {'health': 300, 'damage': 40, 'attack_type': 'claw', 'attack_sound': '../audio/attack/Explosion.wav', 'speed': 3, 'resistance': 3, 'attack_radius': TILESIZE * 2, 'notice_radius': TILESIZE * 4},
    'spirit': {'health': 150, 'damage': 30, 'attack_type': 'thunder', 'attack_sound': '../audio/attack/Explosion4.wav', 'speed': 3, 'resistance': 3, 'attack_radius': TILESIZE * 2, 'notice_radius': TILESIZE * 4}
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

# UI RECTANGLE
ITEM_BOX_BG_COLOR = (59, 60, 54)
ITEM_BOX_BORDER_COLOR = (5, 5, 4)


# UI WEAPON COORDINATES
WEAPON_BOX_POS = (TILESIZE // 4, HP_POS[1] + HP_HEIGHT + MP_HEIGHT + TILESIZE // 5)
WEAPON_BOX_SIZE = (TILESIZE + 10, TILESIZE + 10)

# UI MAGIC COORDINATES
MAGIC_BOX_POS = (TILESIZE // 4, WEAPON_BOX_POS[1] + WEAPON_BOX_SIZE[1] + TILESIZE // 5)
MAGIC_BOX_SIZE = (TILESIZE + 10, TILESIZE + 10)
