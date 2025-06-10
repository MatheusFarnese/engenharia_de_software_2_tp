import os
import pandas as pd
import numpy as np


class Dataset:
    def __init__(self, data_dir):
        self.__tables = {}
        for dirpath, _, filenames in os.walk(data_dir):
            for file in filenames:
                if file.endswith('.csv'):
                    file_path = os.path.join(dirpath, file)
                    table_name = os.path.splitext(os.path.relpath(file_path, data_dir))[0].replace(os.sep, '_')
                    self.__tables[table_name] = pd.read_csv(file_path)

    def defenses_by_th(self, th):
        results = []

        for name, df in self.__tables.items():
            if name.startswith("defenses_"):
                df_th = df[df['th'] <= th]
                if not df_th.empty:
                    max_lvl_row = df_th.loc[df_th['lvl'].abs().idxmax()].copy()
                    max_lvl_row['defense'] = name.replace("defenses_", "")
                    results.append(max_lvl_row)

        if results:
            self.__defenses = pd.DataFrame(results)
            self.__defenses.reset_index(drop=True, inplace=True)
            self.__defenses = self.__defenses.sort_values(by="defense", ascending=True)
        else:
            self.__defenses = pd.DataFrame(columns=['lvl', 'dps', 'dph', 'hp', 'th', 'defense'])

    def heroes_by_lvl(self, lvls):
        hero_lvls = {
            "heroes_barbarian_king": lvls['bk'],
            "heroes_archer_queen": lvls['ac'],
            "heroes_grand_warden": lvls['gw'],
            "heroes_royal_champion": lvls['rc']
        }

        results = []

        for table_name, lvl in hero_lvls.items():
            df = self.__tables.get(table_name)
            if df is not None:
                df_lvl = df[df['lvl'] == lvl]
                if not df_lvl.empty:
                    row = df_lvl.iloc[0].copy()
                    row["hero"] = table_name.replace("heroes_", "")
                    results.append(row)

        if results:
            self.__heroes = pd.DataFrame(results)
            self.__heroes.reset_index(drop=True, inplace=True)
        else:
            self.__heroes = pd.DataFrame(columns=['lvl', 'dps', 'dph', 'hero'])


    def equipments_by_lvl(self, lvls):
        equipment_lvls = {
            "equipments_spiky_ball": lvls['spkb'],
            "equipments_giant_arrow": lvls['gnta'],
            "equipments_fireball": lvls['frbl'],
            "equipments_seeking_shield": lvls['sksh'],
            "equipments_rocket_spear": lvls['rcks']
        }

        results = []

        for table_name, lvl in equipment_lvls.items():
            df = self.__tables.get(table_name)
            if df is not None:
                df_lvl = df[df['lvl'] == lvl]
                if not df_lvl.empty:
                    row = df_lvl.iloc[0].copy()
                    row["equipment"] = table_name.replace("equipments_", "")
                    results.append(row)

        if results:
            self.__equipments = pd.DataFrame(results)
            self.__equipments.reset_index(drop=True, inplace=True)
        else:
            self.__equipments = pd.DataFrame(columns=['lvl', 'dmg', 'dps', 'dph', 'equipment'])

    def defense_by_name_lvl(self, name, lvl):
        id = 'defenses_' + name
        if id in self.__tables:
            idx = self.__defenses.index[self.__defenses['defense'] == name]
            if not idx.empty:
                idx = idx[0]
                if not self.__tables[id].loc[self.__tables[id]['lvl'] == lvl].empty:
                    new_row = self.__tables[id].loc[self.__tables[id]['lvl'] == lvl].copy()
                    for col in new_row.columns:
                        if col in self.__defenses.columns and col != 'equipment':
                            self.__defenses.at[idx, col] = new_row.iloc[0][col]
            self.__defenses.reset_index(drop=True, inplace=True)

    def hero_by_name_lvl(self, name, lvl):
        id = 'heroes_' + name
        if id in self.__tables:
            idx = self.__heroes.index[self.__heroes['hero'] == name]
            if not idx.empty:
                idx = idx[0]
                if not self.__tables[id].loc[self.__tables[id]['lvl'] == lvl].empty:
                    new_row = self.__tables[id].loc[self.__tables[id]['lvl'] == lvl].copy()
                    for col in new_row.columns:
                        if col in self.__heroes.columns and col != 'equipment':
                            self.__heroes.at[idx, col] = new_row.iloc[0][col]
            self.__heroes.reset_index(drop=True, inplace=True)

    def equipment_by_name_lvl(self, name, lvl):
        id = 'equipments_' + name
        if id in self.__tables:
            idx = self.__equipments.index[self.__equipments['equipment'] == name]
            if not idx.empty:
                idx = idx[0]
                if not self.__tables[id].loc[self.__tables[id]['lvl'] == lvl].empty:
                    new_row = self.__tables[id].loc[self.__tables[id]['lvl'] == lvl].copy()
                    for col in new_row.columns:
                        if col in self.__equipments.columns and col != 'equipment':
                            self.__equipments.at[idx, col] = new_row.iloc[0][col]
            self.__equipments.reset_index(drop=True, inplace=True)

    def get_defenses(self):
        return self.__defenses

    def get_heroes(self):
        return self.__heroes

    def get_equipments(self):
        return self.__equipments



class Earthquake:
    def __init__(self, percentage = 0.29):
        self.percentage = percentage

    def calculate_quantity(self, max_hp, dmg_dealt):
        base_dmg = self.percentage * max_hp
        current_hp = max_hp - dmg_dealt
        if current_hp <= 0:
            return 0
        counter = 1
        for i in (1, 3, 5, 7, 9):
            current_hp -= base_dmg / i
            if current_hp <= 0:
                return counter
            counter += 1
        return -1



class RoyalChampion:
    def __init__(self, data):
        self.assign_champion(data)

    def assign_champion(self, data):
        stats = data.get_heroes().loc[data.get_heroes()['hero'] == 'royal_champion']
        seeking_shield = data.get_equipments().loc[data.get_equipments()['equipment'] == 'seeking_shield']
        rocket_spear = data.get_equipments().loc[data.get_equipments()['equipment'] == 'rocket_spear']
        self.spear = rocket_spear
        self.dph = stats['dph'].iloc[0] + rocket_spear['dph'].iloc[0]
        self.dps = stats['dps'].iloc[0] + rocket_spear['dps'].iloc[0]
        self.spear_dmg = np.int64(rocket_spear['dmg'].iloc[0] + stats['dph'].iloc[0] + rocket_spear['dph'].iloc[0])
        self.shield_dmg = np.int64(seeking_shield['dmg'].iloc[0])

    def rocket_spear_recall(self, defenses):
        result = pd.DataFrame(columns=['defense', 'lvl', 'max hp', 'alone', 'with shield', '1 earthquake', 'shield + 1 earthquake'])
        for name in defenses['defense']:
            hp = np.int64(defenses.loc[defenses['defense'] == name].iloc[0]['hp'])
            lvl = np.int64(defenses.loc[defenses['defense'] == name].iloc[0]['lvl'])
            row = []
            row.append(name)
            row.append(lvl)
            row.append(hp)
            row.append(max(0, int(np.ceil( hp / self.spear_dmg ))))
            row.append(max(0, int(np.ceil( (hp - self.shield_dmg) / self.spear_dmg ))))
            row.append(max(0, int(np.ceil( (hp * 0.71) / self.spear_dmg ))))
            row.append(max(0, int(np.ceil( (hp * 0.71 - self.shield_dmg) / self.spear_dmg ))))

            result.loc[-1] = row
            result.index = result.index + 1
            result = result.sort_index()

        result = result.sort_values(by="defense", ascending=True)
        result.reset_index(drop=True, inplace=True)
        return result



class NukeEquipments:
    def __init__(self, equipments, eq_perc = 0.29):
        self.assign_equipments(equipments, eq_perc)

    def assign_equipments(self, equipments, eq_perc = 0.29):
        self.spiky_ball = np.int64(equipments.loc[equipments['equipment'] == 'spiky_ball']['dmg'].iloc[0])
        self.giant_arrow = np.int64(equipments.loc[equipments['equipment'] == 'giant_arrow']['dmg'].iloc[0])
        self.fireball = np.int64(equipments.loc[equipments['equipment'] == 'fireball']['dmg'].iloc[0])
        self.seeking_shield = np.int64(equipments.loc[equipments['equipment'] == 'seeking_shield']['dmg'].iloc[0])
        self.earthquake = Earthquake(eq_perc)

    def fireball_setup(self, defenses):
        result = pd.DataFrame(columns=['defense', 'lvl', 'max hp', 'alone', 'giant arrow', 'spiky ball'])
        for name in defenses['defense']:
            hp = np.int64(defenses.loc[defenses['defense'] == name].iloc[0]['hp'])
            lvl = np.int64(defenses.loc[defenses['defense'] == name].iloc[0]['lvl'])
            row = []
            row.append(name)
            row.append(lvl)
            row.append(hp)
            row.append(self.earthquake.calculate_quantity(hp, self.fireball))
            row.append(self.earthquake.calculate_quantity(hp, self.fireball + self.giant_arrow))
            row.append(self.earthquake.calculate_quantity(hp, self.fireball + self.spiky_ball))

            result.loc[-1] = row
            result.index = result.index + 1
            result = result.sort_index()

        result = result.sort_values(by="defense", ascending=True)
        result.reset_index(drop=True, inplace=True)
        return result

    def spiky_ball_setup(self, defenses):
        result = pd.DataFrame(columns=['defense', 'lvl', 'max hp', 'alone', 'giant arrow'])
        for name in defenses['defense']:
            hp = np.int64(defenses.loc[defenses['defense'] == name].iloc[0]['hp'])
            lvl = np.int64(defenses.loc[defenses['defense'] == name].iloc[0]['lvl'])
            row = []
            row.append(name)
            row.append(lvl)
            row.append(hp)
            row.append(self.earthquake.calculate_quantity(hp, self.spiky_ball))
            row.append(self.earthquake.calculate_quantity(hp, self.spiky_ball + self.giant_arrow))

            result.loc[-1] = row
            result.index = result.index + 1
            result = result.sort_index()

        result = result.sort_values(by="defense", ascending=True)
        result.reset_index(drop=True, inplace=True)
        return result



class Manager:
    def __init__(self, dataset_path, heroes_lvl, equipments_lvl, th = 17, eq_perc = 0.29):
        self.data = Dataset(dataset_path)
        self.data.heroes_by_lvl(heroes_lvl)
        self.data.equipments_by_lvl(equipments_lvl)
        self.data.defenses_by_th(th)
        self.eq_perc = eq_perc

        self.nukes = NukeEquipments(self.data.get_equipments(), eq_perc)

        self.rc = RoyalChampion(self.data)

    def setup(self, op):
        if op == 'fireball':
            return self.nukes.fireball_setup(self.data.get_defenses())
        elif op == 'spiky_ball':
            return self.nukes.spiky_ball_setup(self.data.get_defenses())
        elif op == 'royal_champion':
            return self.rc.rocket_spear_recall(self.data.get_defenses())
        else:
            return None

    def change_defense(self, name, lvl):
        self.data.defense_by_name_lvl(name, lvl)

    def change_hero(self, name, lvl):
        self.data.hero_by_name_lvl(name, lvl)
        if name == 'royal_champion':
            self.rc.assign_champion(self.data)

    def change_equipment(self, name, lvl):
        self.data.equipment_by_name_lvl(name, lvl)
        if name == 'rocket_spear':
            self.rc.assign_champion(self.data)
        self.nukes.assign_equipments(self.data.get_equipments(), self.eq_perc)

    def change_earthquake_percentage(self, perc):
        self.eq_perc = perc
        self.nukes.assign_equipments(self.data.get_equipments(), perc)



def example():
    path = 'datasets'
    heroes_lvl = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
    equipments_lvl = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
    th = 17
    m = Manager(path, heroes_lvl, equipments_lvl, th)

    print(m.setup('fireball'))
    print(m.setup('spiky_ball'))
    print(m.setup('royal_champion'))
#example()
