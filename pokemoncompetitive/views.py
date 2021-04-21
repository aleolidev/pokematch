from django.shortcuts import render
from pokemoncompetitive.models import Mon_Names
import pokebase as pb
import re
from math import floor
import colorsys

# Create your views here.
def index(request):
    mon_names = Mon_Names.objects.all
    player_mon_name, target_mon_name = None, None
    player_struct = {"name": "", "moves": list(), "hp": 0, "atk": 0, "deff": 0, "sp_atk": 0, "sp_def": 0, "speed": 0, "total": 0, "pct_hp": 0, "pct_atk": 0, "pct_deff": 0, "pct_sp_atk": 0, "pct_sp_def": 0, "pct_speed": 0, "pct_total": 0, "min_hp": 0, "min_atk": 0, "min_deff": 0, "min_sp_atk": 0, "min_sp_def": 0, "min_speed": 0, "max_hp": 0, "max_atk": 0, "max_deff": 0, "max_sp_atk": 0, "max_sp_def": 0, "max_speed": 0, "hex_hp": 0, "hex_atk": 0, "hex_deff": 0, "hex_sp_atk": 0, "hex_sp_def": 0, "hex_speed": 0, "icon": "", "abilities":list(), "types": list(), "weaknesses": list(), "resistance": list(), "noeffect": list(), "disp_weaknesses": "none", "disp_resistance": "none", "disp_noeffect": "none", "display": "none"}
    target_struct = {"name": "", "moves": list(), "hp": 0, "atk": 0, "deff": 0, "sp_atk": 0, "sp_def": 0, "speed": 0, "total": 0, "pct_hp": 0, "pct_atk": 0, "pct_deff": 0, "pct_sp_atk": 0, "pct_sp_def": 0, "pct_speed": 0, "pct_total": 0, "min_hp": 0, "min_atk": 0, "min_deff": 0, "min_sp_atk": 0, "min_sp_def": 0, "min_speed": 0, "max_hp": 0, "max_atk": 0, "max_deff": 0, "max_sp_atk": 0, "max_sp_def": 0, "max_speed": 0, "hex_hp": 0, "hex_atk": 0, "hex_deff": 0, "hex_sp_atk": 0, "hex_sp_def": 0, "hex_speed": 0, "icon": "", "abilities":list(), "types": list(), "weaknesses": list(), "resistance": list(), "noeffect": list(), "disp_weaknesses": "none", "disp_resistance": "none", "disp_noeffect": "none", "display": "none"}
    orig_p_name, orig_t_name = "", ""
    if request.method == "POST":
        # Process Player Mon POST
        player_mon_name = request.POST.get("playerMon", None)
        if Mon_Names.objects.filter(name=player_mon_name).exists():
            orig_p_name = player_mon_name
            player_mon_name = parse_name(player_mon_name)
            player_mon_name = pb.pokemon(player_mon_name)
            player_struct['name'] = player_mon_name
            player_struct['display'] = "block"

            get_base_stats(player_mon_name, player_struct)
            get_percent_stats(player_mon_name, player_struct)
            get_min_stats(player_mon_name, player_struct)
            get_max_stats(player_mon_name, player_struct)
            get_hex_colors(player_mon_name, player_struct)
            get_mon_types(player_mon_name, player_struct)
            get_type_damage_relation(player_mon_name, player_struct)
            get_abilities(player_mon_name, player_struct)
            # get_moves(player_mon_name, player_struct)

            # Get Icon
            player_struct['icon'] = getattr(player_mon_name.sprites.versions, "generation-vii").icons.front_default

        # Process Target Mon POST
        target_mon_name = request.POST.get("targetMon", None)
        if Mon_Names.objects.filter(name=target_mon_name).exists():
            orig_t_name = target_mon_name
            target_mon_name = parse_name(target_mon_name)
            target_mon_name = pb.pokemon(target_mon_name)
            target_struct['name'] = target_mon_name
            target_struct['display'] = "block"

            get_base_stats(target_mon_name, target_struct)
            get_percent_stats(target_mon_name, target_struct)
            get_min_stats(target_mon_name, target_struct)
            get_max_stats(target_mon_name, target_struct)
            get_hex_colors(target_mon_name, target_struct)
            get_mon_types(target_mon_name, target_struct)
            get_type_damage_relation(target_mon_name, target_struct)
            get_abilities(target_mon_name, target_struct)
            # get_moves(target_mon_name, target_struct)

            # Get Icon
            target_struct['icon'] = getattr(target_mon_name.sprites.versions, "generation-vii").icons.front_default
            
    return render(request, "pokemoncompetitive/base.html", {
        "showmons":mon_names, 
        "orig_p_name":orig_p_name,
        "player_struct":player_struct, 
        "orig_t_name":orig_t_name,
        "target_struct":target_struct
    })

def parse_name(raw_name):
    player_mon_name = raw_name
    if re.match('^Mega ', player_mon_name) is not None or re.match('^Primal ', player_mon_name) is not None:
        player_mon_name = re.sub(r'(\w+) (\w+)', r'\2 \1', player_mon_name)
    if re.match('^Alolan ', player_mon_name) is not None:
        player_mon_name = re.sub(r'(\w+) (\w+)', r'\2 Alola', player_mon_name)
    if re.match('^Galarian ', player_mon_name) is not None:
        player_mon_name = re.sub(r'(\w+) (\w+)', r'\2 Galar', player_mon_name)
    if re.match('^(\w+) (\w+) Form', player_mon_name) is not None:
        player_mon_name = re.sub(r'(\w+) (\w+) (\w+)', r'\1 \2', player_mon_name)
    player_mon_name = player_mon_name.lower().replace(' ', '-').replace('♀', '-f').replace('♂', '-m').replace("'", "")
    return player_mon_name

def get_base_stats(mon_name, mon_struct):
    mon_struct['hp'] = mon_name.stats[0].base_stat
    mon_struct['atk'] = mon_name.stats[1].base_stat
    mon_struct['deff'] = mon_name.stats[2].base_stat
    mon_struct['sp_atk'] = mon_name.stats[3].base_stat
    mon_struct['sp_def'] = mon_name.stats[4].base_stat
    mon_struct['speed'] = mon_name.stats[5].base_stat
    mon_struct['total'] = mon_struct['hp'] + mon_struct['atk'] + mon_struct['deff'] + mon_struct['sp_atk'] + mon_struct['sp_def'] + mon_struct['speed']

def get_percent_stats(mon_name, mon_struct):
    mon_struct['pct_hp'] = (mon_struct['hp'] / 255) * 100
    mon_struct['pct_atk'] = (mon_struct['atk'] / 255) * 100
    mon_struct['pct_deff'] = (mon_struct['deff'] / 255) * 100
    mon_struct['pct_sp_atk'] = (mon_struct['sp_atk'] / 255) * 100
    mon_struct['pct_sp_def'] = (mon_struct['sp_def'] / 255) * 100
    mon_struct['pct_speed'] = (mon_struct['speed'] / 255) * 100
    mon_struct['pct_total'] = ((mon_struct['hp'] + mon_struct['atk'] + mon_struct['deff'] + mon_struct['sp_atk'] + mon_struct['sp_def'] + mon_struct['speed'])/(255*6))*100

def get_min_stats(mon_name, mon_struct):
    mon_struct['min_hp'] = (mon_name.stats[0].base_stat*2)+110
    mon_struct['min_atk'] = floor(((mon_name.stats[1].base_stat*2)+5)*0.9)
    mon_struct['min_deff'] = floor(((mon_name.stats[2].base_stat*2)+5)*0.9)
    mon_struct['min_sp_atk'] = floor(((mon_name.stats[3].base_stat*2)+5)*0.9)
    mon_struct['min_sp_def'] = floor(((mon_name.stats[4].base_stat*2)+5)*0.9)
    mon_struct['min_speed'] = floor(((mon_name.stats[5].base_stat*2)+5)*0.9)

def get_max_stats(mon_name, mon_struct):
    mon_struct['max_hp'] = (mon_name.stats[0].base_stat*2)+204
    mon_struct['max_atk'] = floor(((mon_name.stats[1].base_stat*2)+99)*1.1)
    mon_struct['max_deff'] = floor(((mon_name.stats[2].base_stat*2)+99)*1.1)
    mon_struct['max_sp_atk'] = floor(((mon_name.stats[3].base_stat*2)+99)*1.1)
    mon_struct['max_sp_def'] = floor(((mon_name.stats[4].base_stat*2)+99)*1.1)
    mon_struct['max_speed'] = floor(((mon_name.stats[5].base_stat*2)+99)*1.1)

def get_hex_colors(mon_name, mon_struct):
    mon_struct['hex_hp'] = '#%02x%02x%02x' % get_rgb_color(mon_struct['hp'])
    mon_struct['hex_atk'] = '#%02x%02x%02x' % get_rgb_color(mon_struct['atk'])
    mon_struct['hex_deff'] = '#%02x%02x%02x' % get_rgb_color(mon_struct['deff'])
    mon_struct['hex_sp_atk'] = '#%02x%02x%02x' % get_rgb_color(mon_struct['sp_atk'])
    mon_struct['hex_sp_def'] = '#%02x%02x%02x' % get_rgb_color(mon_struct['sp_def'])
    mon_struct['hex_speed'] = '#%02x%02x%02x' % get_rgb_color(mon_struct['speed'])

def get_mon_types(mon_name, mon_struct):
    for types in mon_name.types:
        mon_struct['types'].append(types.type.name.lower())

def get_type_damage_relation(mon_name, mon_struct):
    wr_type_list = {}
    for types in mon_name.types:
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
            mon_struct['weaknesses'].append({"name":name, "multiple":int(wr_type_list[name])})
        elif wr_type_list[name] > 0 and wr_type_list[name] < 1:
            mon_struct['resistance'].append({"name":name, "multiple":wr_type_list[name]})
        elif wr_type_list[name] == 0:
            mon_struct['noeffect'].append({"name":name, "multiple":wr_type_list[name]})

    if bool(mon_struct['weaknesses']):
        mon_struct['disp_weaknesses'] = "flex"
    if bool(mon_struct['resistance']):
        mon_struct['disp_resistance'] = "flex"
    if bool(mon_struct['noeffect']):
        mon_struct['disp_noeffect'] = "flex"

def get_abilities(mon_name, mon_struct):
    for ability in mon_name.abilities:
        ab = pb.ability(ability.ability.name)
        short_desc = ab.effect_entries[0].short_effect
        for entry in ab.effect_entries:
            if entry.language.name == "en":
                short_desc = entry.short_effect
                break
        mon_struct['abilities'].append({"name": ab.name.capitalize(), "short_description": short_desc, "is_hidden": "inline-block" if ability.is_hidden else "none"})

def get_moves(mon_name, mon_struct):
    # for move in mon_name.moves:
    move = mon_name.moves[0]
    print(move.move.name)
    name = move.move.name.replace('-', ' ').capitalize()
    mov = pb.move(move.move.name)
    accuracy = str(mov.accuracy) if mov.accuracy is not None else "—"
    power = str(mov.power) if mov.power is not None else "—"
    mov_type = mov.type.name
    dmg_class = mov.damage_class.name
    mon_struct['moves'].append({"name":name, "accuracy":accuracy, "power":power, "mov_type": mov_type, "dmg_class": dmg_class})

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
