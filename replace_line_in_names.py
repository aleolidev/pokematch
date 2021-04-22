from django.conf import settings
import pokebase as pb
import progressbar
import json
import re
from math import floor
import colorsys
import requests

data = {}

with open('C:/Users/inmor/Documents/Python/Webs/Poketitive/src/static/mons.json') as input_file:
        data = json.load(input_file)
input_file.close()
    
counter = 0  # Failed in 812
pbar = progressbar.ProgressBar(maxval=len(data))
pbar.start()

with open('C:/Users/inmor/Documents/Python/Webs/Poketitive/src/static/mons.json', 'w') as outfile:
    for i in range(len(data)):
        data[i]['beauty_name'] = data[i]['beauty_name'].replace('-', ' ')
        for j in range(len(data[i]['abilities'])):
            data[i]['abilities'][j]['name'] = data[i]['abilities'][j]['name'].replace('-', ' ')
        outfile.seek(0)
        json.dump(data, outfile)

        counter = i
        pbar.update(counter)

    pbar.finish()
    outfile.close()