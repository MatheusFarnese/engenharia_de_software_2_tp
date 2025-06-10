import streamlit as st
import pandas as pd
from clash import Manager

# --- Constants ---
TH_LEVELS = list(range(1, 18))
DEFAULT_HERO_LVLS = {'bk': 95, 'ac': 95, 'gw': 70, 'rc': 45}
DEFAULT_EQ_LVLS = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
SETUPS = ['fireball', 'spiky_ball', 'royal_champion']

HERO_NAMES = {'bk': 'Barbarian King', 'ac': 'Archer Queen', 'gw': 'Grand Warden', 'rc': 'Royal Champion'}
EQUIP_NAMES = {
    'spkb': 'Spiky Ball',
    'gnta': 'Giant Arrow',
    'frbl': 'Fireball',
    'sksh': 'Seeking Shield',
    'rcks': 'Rocket Spear'
}
HERO_LIMITS = {'bk': 100, 'ac': 100, 'gw': 75, 'rc': 50}
EQUIP_LIMITS = {'spkb': 27, 'gnta': 18, 'frbl': 27, 'sksh': 18, 'rcks': 27}
DEFENSE_LIMITS = {
    'air_defense': 17,
    'air_sweeper': 7,
    'archer_tower': 21,
    'bomb_tower': 14,
    'builder_hut': 9,
    'cannon': 21,
    'clan_castle': 13,
    'eagle_artillery': 7,
    'firespitter': 4,
    'hidden_tesla': 18,
    'inferno_tower': 13,
    'monolith': 6,
    'mortar': 19,
    'multi_archer': 5,
    'multi_gear_tower': 4,
    'ricochet_cannon': 5,
    'scattershot': 8,
    'spell_tower': 3,
    'townhall': 17,
    'wizard_tower': 19,
    'xbow': 14
}

# --- Initialize session state ---
if 'th' not in st.session_state:
    st.session_state.th = 17
if 'heroes' not in st.session_state:
    st.session_state.heroes = DEFAULT_HERO_LVLS.copy()
if 'equipments' not in st.session_state:
    st.session_state.equipments = DEFAULT_EQ_LVLS.copy()
if 'setup' not in st.session_state:
    st.session_state.setup = 'fireball'
if 'manager' not in st.session_state:
    st.session_state.manager = Manager('datasets', st.session_state.heroes, st.session_state.equipments, st.session_state.th)

st.title("Clash of Clans Setup Calculator")

# --- Step 1: Town Hall Selection ---
st.subheader("1. Select Town Hall Level")
cols = st.columns(6)
for i, th in enumerate(TH_LEVELS):
    if cols[i % 6].button(f"TH {th}"):
        st.session_state.th = th
        st.session_state.manager = Manager('datasets', st.session_state.heroes, st.session_state.equipments, st.session_state.th)

# --- Step 2: Adjust Hero and Equipment Levels ---
st.subheader("2. Adjust Hero and Equipment Levels")

new_hero_lvls = {}
st.markdown("### Heroes")
hero_rows = st.columns(2)
for idx, (hero, name) in enumerate(HERO_NAMES.items()):
    with hero_rows[idx % 2]:
        st.markdown(f"**{name}**")
        max_lvl = HERO_LIMITS[hero]
        new_hero_lvls[hero] = st.number_input("", min_value=1, max_value=max_lvl, value=st.session_state.heroes[hero], key=f"num_hero_{hero}", label_visibility="collapsed")

new_equip_lvls = {}
st.markdown("### Equipments")
equip_rows = st.columns(2)
for idx, (eq, name) in enumerate(EQUIP_NAMES.items()):
    with equip_rows[idx % 2]:
        st.markdown(f"**{name}**")
        max_lvl = EQUIP_LIMITS[eq]
        new_equip_lvls[eq] = st.number_input("", min_value=1, max_value=max_lvl, value=st.session_state.equipments[eq], key=f"num_eq_{eq}", label_visibility="collapsed")

if st.button("Apply Level Changes"):
    st.session_state.heroes = new_hero_lvls
    st.session_state.equipments = new_equip_lvls
    st.session_state.manager = Manager('datasets', st.session_state.heroes, st.session_state.equipments, st.session_state.th)

# --- Step 3: Select Setup Type ---
st.subheader("3. Choose Setup Type")
st.session_state.setup = st.selectbox(
    "Setup", options=SETUPS, index=SETUPS.index(st.session_state.setup), format_func=lambda x: x.replace('_', ' ').title(), key="setup_selector")

# --- Step 4: Display Setup Controls ---
st.subheader("4. Adjust Defense Levels")
data = st.session_state.manager.data.get_defenses()

defense_levels = {}
if isinstance(data, pd.DataFrame) and not data.empty:
    for i in range(0, len(data), 3):
        row_data = data.iloc[i:i+3]
        row_cols = st.columns(3)
        for j, (_, row) in enumerate(row_data.iterrows()):
            with row_cols[j]:
                name = row['defense']
                current_lvl = int(row['lvl'])
                max_def_lvl = DEFENSE_LIMITS.get(name, 100)

                st.markdown(f"**{name}**")

                new_lvl = st.number_input("", min_value=1, max_value=max_def_lvl, value=current_lvl, key=f"num_{name}", label_visibility="collapsed")
                st.session_state.manager.change_defense(name, new_lvl)

    if st.session_state.setup == 'royal_champion':
        st.write("\n**Rocket Spear shots needed**")
    else:
        st.write("\n**Earthquake spells needed**")
    st.dataframe(st.session_state.manager.setup(st.session_state.setup))
else:
    st.warning("No defense data available.")
