from clash import GameData, Earthquake, RoyalChampion, NukeEquipments, Manager

DATASET_PATH = "./datasets"

def test_get_th_defenses():
    d = GameData(DATASET_PATH)
    d.defenses_by_th(16)
    for th in d.get_defenses()['th']:
        assert th <= 16
    d.defenses_by_th(14)
    for th in d.get_defenses()['th']:
        assert th <= 14

def test_no_higher_tier_defenses():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 14
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th)
    flag = False

    for dfs in m.data.get_defenses()['defense']:
        if dfs == 'monolith' or dfs == 'spell_tower' or dfs == 'multi_archer' or dfs == 'ricochet_cannon':
            flag = True
    assert flag == False

def test_no_over_leveled_defenses():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 14
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th)
    flag = False

    assert m.data.get_defenses()[m.data.get_defenses()['defense'] == 'xbow'].iloc[0]['lvl'] <= 9
    assert m.data.get_defenses()[m.data.get_defenses()['defense'] == 'archer_tower'].iloc[0]['lvl'] <= 20
    assert m.data.get_defenses()[m.data.get_defenses()['defense'] == 'inferno_tower'].iloc[0]['lvl'] <= 8

def test_single_line_changes():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 16
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th)
    
    m.change_defense("multi_archer", 1)
    m.change_hero("archer_queen", 100)
    m.change_equipment("fireball", 24)

    assert m.data.get_defenses()[m.data.get_defenses()['defense'] == 'multi_archer'].iloc[0]['hp'] == 5000
    assert m.data.get_heroes()[m.data.get_heroes()['hero'] == 'archer_queen'].iloc[0]['dps'] == 780
    assert m.data.get_equipments()[m.data.get_equipments()['equipment'] == 'fireball'].iloc[0]['dmg'] == 3900

def test_no_invalid_single_line_changes():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 16
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th)

    m.change_defense("multi_archer", 60)
    m.change_hero("archer_queen", 1707)
    m.change_equipment("fireball", 666)

    assert m.data.get_defenses()[m.data.get_defenses()['defense'] == 'multi_archer'].iloc[0]['lvl'] == 2
    assert m.data.get_heroes()[m.data.get_heroes()['hero'] == 'archer_queen'].iloc[0]['lvl'] == 95
    assert m.data.get_equipments()[m.data.get_equipments()['equipment'] == 'fireball'].iloc[0]['lvl'] == 27

def test_earthquake_calculations():
    eq = Earthquake()
    n1 = eq.calculate_quantity(1707, 1212)
    n2 = eq.calculate_quantity(1707, 1211)
    assert n1 == 1
    assert n2 == 2

def test_cant_kill_with_earthquake():
    eq = Earthquake()
    n = eq.calculate_quantity(666, 0)
    assert n == -1

def test_royal_champion_setup():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 17
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th)

    setup = m.setup('royal_champion')

    assert setup[setup['defense'] == 'wizard_tower'].iloc[0]['max hp'] == 3375
    assert setup[setup['defense'] == 'wizard_tower'].iloc[0]['alone'] == 2
    assert setup[setup['defense'] == 'wizard_tower'].iloc[0]['with shield'] == 1
    assert setup[setup['defense'] == 'wizard_tower'].iloc[0]['1 earthquake'] == 2
    assert setup[setup['defense'] == 'wizard_tower'].iloc[0]['shield + 1 earthquake'] == 0

def test_fireball_setup():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 17
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th)

    setup = m.setup('fireball')

    assert setup[setup['defense'] == 'townhall'].iloc[0]['max hp'] == 10400
    assert setup[setup['defense'] == 'townhall'].iloc[0]['alone'] == -1
    assert setup[setup['defense'] == 'townhall'].iloc[0]['giant arrow'] == 3
    assert setup[setup['defense'] == 'townhall'].iloc[0]['spiky ball'] == 2

def test_spiky_ball_setup():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 17
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th)

    setup = m.setup('spiky_ball')

    assert setup[setup['defense'] == 'clan_castle'].iloc[0]['max hp'] == 5800
    assert setup[setup['defense'] == 'clan_castle'].iloc[0]['alone'] == 3
    assert setup[setup['defense'] == 'clan_castle'].iloc[0]['giant arrow'] == 1

def test_setup_with_defense_changes():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 17
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th)

    setup = m.setup('fireball')
    assert setup[setup['defense'] == 'monolith'].iloc[0]['alone'] == 2

    m.change_defense('monolith', 4)
    setup = m.setup('fireball')
    assert setup[setup['defense'] == 'monolith'].iloc[0]['alone'] == 1

def test_setup_with_hero_changes():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 17
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th)

    setup = m.setup('royal_champion')
    assert setup[setup['defense'] == 'xbow'].iloc[0]['alone'] == 3

    m.change_hero('royal_champion', 1)
    setup = m.setup('royal_champion')
    assert setup[setup['defense'] == 'xbow'].iloc[0]['alone'] == 4

def test_setup_with_equipment_changes():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 17
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th)

    setup = m.setup('fireball')
    assert setup[setup['defense'] == 'clan_castle'].iloc[0]['giant arrow'] == 0

    m.change_equipment('fireball', 26)
    setup = m.setup('fireball')
    assert setup[setup['defense'] == 'clan_castle'].iloc[0]['giant arrow'] == 0

    m.change_equipment('giant_arrow', 17)
    setup = m.setup('fireball')
    assert setup[setup['defense'] == 'clan_castle'].iloc[0]['giant arrow'] == 1

def test_spiky_ball_with_lower_lvl_earthquake():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 12, 'gnta': 12, 'frbl': 18, 'sksh': 1, 'rcks': 2}
    th = 14
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th)

    setup = m.setup('spiky_ball')
    assert setup[setup['defense'] == 'scattershot'].iloc[0]['max hp'] == 4800
    assert setup[setup['defense'] == 'scattershot'].iloc[0]['alone'] == -1
    assert setup[setup['defense'] == 'scattershot'].iloc[0]['giant arrow'] == 1

    m.change_earthquake_percentage(0.25)
    setup = m.setup('spiky_ball')
    assert setup[setup['defense'] == 'scattershot'].iloc[0]['max hp'] == 4800
    assert setup[setup['defense'] == 'scattershot'].iloc[0]['alone'] == -1
    assert setup[setup['defense'] == 'scattershot'].iloc[0]['giant arrow'] == 2

def test_fireball_with_lower_lvl_earthquake():
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 15
    m = Manager(DATASET_PATH, heroes_lvl, equipments_lvl, th, 0.21)
    m.change_equipment("fireball", 15)
    m.change_equipment("giant_arrow", 1)
    m.change_equipment("spiky_ball", 16)


    setup = m.setup('fireball')
    assert setup[setup['defense'] == 'inferno_tower'].iloc[0]['max hp'] == 4000
    assert setup[setup['defense'] == 'inferno_tower'].iloc[0]['alone'] == 2
    assert setup[setup['defense'] == 'inferno_tower'].iloc[0]['giant arrow'] == 1
    assert setup[setup['defense'] == 'inferno_tower'].iloc[0]['spiky ball'] == 0

    m.change_earthquake_percentage(0.29)
    setup = m.setup('fireball')
    assert setup[setup['defense'] == 'inferno_tower'].iloc[0]['max hp'] == 4000
    assert setup[setup['defense'] == 'inferno_tower'].iloc[0]['alone'] == 1
    assert setup[setup['defense'] == 'inferno_tower'].iloc[0]['giant arrow'] == 1
    assert setup[setup['defense'] == 'inferno_tower'].iloc[0]['spiky ball'] == 0
