FPS = 60
TILESIZE = 128

PLAYER_SPEED = 10

# оружия
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 100, 'graphic': '../graphics/weapons2/sword/full.png'},
    'axe': {'cooldown': 300, 'damage': 150, 'graphic': '../graphics/weapons2/axe/full.png'},
    'lance': {'cooldown': 400, 'damage': 200, 'graphic': '../graphics/weapons2/lance/full.png'}
}

# магия
magic_data = {
    'flame': {'cooldown': 100, 'strength': 100, 'cost': 20, 'graphic': '../graphics/particles2/flame/fire.png',
              'sound': '../audio/flame.wav'},
    'heal': {'cooldown': 100, 'strength': 20, 'cost': 20, 'graphic': '../graphics/particles2/heal/heal.png',
             'sound': '../audio/heal.wav'},
    'spark': {'cooldown': 100, 'strength': 130, 'cost': 30, 'graphic': '../graphics/particles2/spark/spark.png',
              'sound': '../audio/spark.wav'}
}


# враги
monster_data = {
    'reptile': {'health': 200, 'damage': 20, 'attack_type': 'slash',
             'attack_sound': '../audio/attack/Hit.wav', 'speed': 6,
             'resistance': 3, 'attack_radius': TILESIZE, 'notice_radius': TILESIZE * 3},

    'dragon': {'health': 300, 'damage': 30, 'attack_type': 'claw',
               'attack_sound': '../audio/attack/Explosion.wav', 'speed': 6,
               'resistance': 3, 'attack_radius': TILESIZE, 'notice_radius': TILESIZE * 3},

    'mole': {'health': 150, 'damage': 20, 'attack_type': 'thunder',
             'attack_sound': '../audio/attack/Explosion4.wav', 'speed': 8,
             'resistance': 3, 'attack_radius': TILESIZE, 'notice_radius': TILESIZE * 3}
}

# ключи для id букв-обозначений полей
FIELDS_IDS = {52: 1, 60: 2, 68: 3, 76: 4}

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

# FIELD ACTIVE ZONE
FIELD_ACTIVE_ZONE = TILESIZE * 3
