import pokebase as pb
import progressbar
import json
import re
from math import floor
import colorsys
import requests

data = list()

# for i in range(1, 9):
#     for pokemon in pb.generation(i).pokemon_species:
#         print(pokemon.name)
#         count += 1


def set_mon_data(data, mon):
    data_struct = {"beauty_name": "","name": "", "moves": list(), "hp": 0, "atk": 0, "deff": 0, "sp_atk": 0, "sp_def": 0, "speed": 0, "total": 0, "pct_hp": 0, "pct_atk": 0, "pct_deff": 0, "pct_sp_atk": 0, "pct_sp_def": 0, "pct_speed": 0, "pct_total": 0, "min_hp": 0, "min_atk": 0, "min_deff": 0, "min_sp_atk": 0, "min_sp_def": 0, "min_speed": 0, "max_hp": 0, "max_atk": 0, "max_deff": 0, "max_sp_atk": 0, "max_sp_def": 0, "max_speed": 0, "hex_hp": 0, "hex_atk": 0, "hex_deff": 0, "hex_sp_atk": 0, "hex_sp_def": 0, "hex_speed": 0, "icon": "", "abilities":list(), "types": list(), "weaknesses": list(), "resistance": list(), "noeffect": list(), "disp_weaknesses": "none", "disp_resistance": "none", "disp_noeffect": "none", "display": "block"}
    data_struct['beauty_name'] = mon.name.title()
    data_struct['name'] = mon.name

    stats = mon.stats
    # Normal stats

    data_struct['hp'] = stats[0].base_stat
    data_struct['atk'] = stats[1].base_stat
    data_struct['deff'] = stats[2].base_stat
    data_struct['sp_atk'] = stats[3].base_stat
    data_struct['sp_def'] = stats[4].base_stat
    data_struct['speed'] = stats[5].base_stat
    data_struct['total'] = data_struct['hp'] + data_struct['atk'] + data_struct['deff'] + data_struct['sp_atk'] + data_struct['sp_def'] + data_struct['speed']

    # Percentage stats
    data_struct['pct_hp'] = (data_struct['hp'] / 255) * 100
    data_struct['pct_atk'] = (data_struct['atk'] / 255) * 100
    data_struct['pct_deff'] = (data_struct['deff'] / 255) * 100
    data_struct['pct_sp_atk'] = (data_struct['sp_atk'] / 255) * 100
    data_struct['pct_sp_def'] = (data_struct['sp_def'] / 255) * 100
    data_struct['pct_speed'] = (data_struct['speed'] / 255) * 100
    data_struct['pct_total'] = ((data_struct['hp'] + data_struct['atk'] + data_struct['deff'] + data_struct['sp_atk'] + data_struct['sp_def'] + data_struct['speed'])/(255*6))*100

    # Min stats
    data_struct['min_hp'] = (stats[0].base_stat*2)+110
    data_struct['min_atk'] = floor(((stats[1].base_stat*2)+5)*0.9)
    data_struct['min_deff'] = floor(((stats[2].base_stat*2)+5)*0.9)
    data_struct['min_sp_atk'] = floor(((stats[3].base_stat*2)+5)*0.9)
    data_struct['min_sp_def'] = floor(((stats[4].base_stat*2)+5)*0.9)
    data_struct['min_speed'] = floor(((stats[5].base_stat*2)+5)*0.9)

    # Max stats
    data_struct['max_hp'] = (stats[0].base_stat*2)+204
    data_struct['max_atk'] = floor(((stats[1].base_stat*2)+99)*1.1)
    data_struct['max_deff'] = floor(((stats[2].base_stat*2)+99)*1.1)
    data_struct['max_sp_atk'] = floor(((stats[3].base_stat*2)+99)*1.1)
    data_struct['max_sp_def'] = floor(((stats[4].base_stat*2)+99)*1.1)
    data_struct['max_speed'] = floor(((stats[5].base_stat*2)+99)*1.1)

    # Hex colors
    data_struct['hex_hp'] = '#%02x%02x%02x' % get_rgb_color(data_struct['hp'])
    data_struct['hex_atk'] = '#%02x%02x%02x' % get_rgb_color(data_struct['atk'])
    data_struct['hex_deff'] = '#%02x%02x%02x' % get_rgb_color(data_struct['deff'])
    data_struct['hex_sp_atk'] = '#%02x%02x%02x' % get_rgb_color(data_struct['sp_atk'])
    data_struct['hex_sp_def'] = '#%02x%02x%02x' % get_rgb_color(data_struct['sp_def'])
    data_struct['hex_speed'] = '#%02x%02x%02x' % get_rgb_color(data_struct['speed'])

    # Mon types
    for types in mon.types:
        data_struct['types'].append(types.type.name.lower())

    # Types damaga relation
    wr_type_list = {}
    for types in mon.types:
        for x2 in pb.type_(types.type.name.lower()).damage_relations.double_damage_from:
            if x2.name in wr_type_list:
                wr_type_list[x2.name] = wr_type_list[x2.name] * 2.
            else:
                wr_type_list[x2.name] = 2.
        for x05 in pb.type_(types.type.name.lower()).damage_relations.half_damage_from:
            if x05.name in wr_type_list:
                wr_type_list[x05.name] = wr_type_list[x05.name] * 0.5
            else:
                wr_type_list[x05.name] = 0.5
        for x0 in pb.type_(types.type.name.lower()).damage_relations.no_damage_from:
            wr_type_list[x0.name] = 0

    for name in sorted(wr_type_list, key=wr_type_list.get, reverse=True):
        # print(name, wr_type_list[name])
        if wr_type_list[name] > 1:
            data_struct['weaknesses'].append({"name":name, "multiple":int(wr_type_list[name])})
        elif wr_type_list[name] > 0 and wr_type_list[name] < 1:
            data_struct['resistance'].append({"name":name, "multiple":wr_type_list[name]})
        elif wr_type_list[name] == 0:
            data_struct['noeffect'].append({"name":name, "multiple":wr_type_list[name]})

    if bool(data_struct['weaknesses']):
        data_struct['disp_weaknesses'] = "flex"
    if bool(data_struct['resistance']):
        data_struct['disp_resistance'] = "flex"
    if bool(data_struct['noeffect']):
        data_struct['disp_noeffect'] = "flex"

    
    # Abilities
    for ability in mon.abilities:
        ab = pb.ability(ability.ability.name)
        short_desc = ""
        for entry in ab.effect_entries:
            if entry.language.name == "en":
                short_desc = entry.short_effect
                break
        data_struct['abilities'].append({"name": ab.name.capitalize(), "short_description": short_desc, "is_hidden": "inline-block" if ability.is_hidden else "none"})

    data.append(data_struct)

    # Icon
    data_struct["icon"] = getattr(mon.sprites.versions, "generation-viii").icons.front_default


def get_rgb_color(base_hue):
    hue = 0
    if (base_hue >= 20 and base_hue < 50):
        hue = 19
    elif (base_hue >= 50 and base_hue < 100):
        hue = 32
    elif (base_hue >= 100 and base_hue < 120):
        hue = 53
    elif (base_hue >= 120 and base_hue < 150):
        hue = 94
    elif (base_hue >= 150):
        hue = 118

    r, g, b = colorsys.hls_to_rgb(hue/240., 0.55, 0.833)
    return (int(r*255), int(g*255), int(b*255))

with open('C:/Users/inmor/Desktop/data.json', 'w') as outfile:
    api_data = (requests.get("https://pokeapi.co/api/v2/pokemon?offset=0&limit=9999")).json()
    
    counter = 0  # Failed in 812
    start_offset = 0  # By if it fails
    pbar = progressbar.ProgressBar(maxval=api_data['count'])
    pbar.start()

    for pokemon in api_data['results']:
        if counter >= start_offset:
            mon = pb.pokemon(pokemon['name'])
            set_mon_data(data, mon)
            outfile.seek(0)
            json.dump(data, outfile)

        counter += 1
        pbar.update(counter)

    outfile.close()

    pbar.finish()
