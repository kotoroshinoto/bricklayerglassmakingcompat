import string
import os
import sys
import path
import itertools

json_template = """
{
  "code": "glasstype",
  "variants": [
    %s
  ]
}
"""

json_entry_template = """    {
      "code": "%s",
      "meltingPoint": %d
    }"""
glass_types = [
    "plain",
    "quartz",
    "milky",
    "smoky",
    "dark",
    "opaque"
]
glass_colors = [
    None,
    "black",
    "blue",
    "brown",
    "green",
    "orange",
    "pink",
    "red",
    "violet",
    "yellow",
    'white'
]

base_temp = 1300

type_temps = {
'quartz':1600,
'smoky':1600,
'dark':1400,
'opaque':1600
}

color_temps = {
'green':1400,
'pink':1600,
'violet':1400,
'black':1500,
'orange':1400
}

basegame = []

bricklayers = []



def calc_mix_temperature(type_input, color_input):
    if type_input in type_temps:
        type_temp = type_temps[type_input]
    else:
        type_temp = None
    if color_input in color_temps:
        color_temp = color_temps[color_input]
    else:
        color_temp = None
    if (type_temp is None) and (color_temp is None):
        return base_temp
    elif type_temp is None:
        return color_temp
    elif color_temp is None:
        return type_temp
    else:
        type_offset = type_temp - base_temp
        color_offset = color_temp - base_temp
        bigger_offset = max([type_offset,color_offset])
        smaller_offset = min([type_offset,color_offset])
        return base_temp + int(((bigger_offset * 4.0) + (smaller_offset*1.0)) / 4.0)

def generate_color_code(type_input, color_input):
    mix_temp = calc_mix_temperature(type_input, color_input)
    if color_input is None:
        if type_input == 'milky':
            basegame.append(json_entry_template % (('glass-%s' % "vintage"), mix_temp))
        elif type_input in ['dark','opaque']:
            return
        else:
            basegame.append(json_entry_template % (('glass-%s' % type_input), mix_temp))
    elif color_input == 'white':
        if type_input == 'opaque':
            bricklayers.append(json_entry_template % ('glasscolored-%s-%s' % (type_input, color_input), mix_temp))
        else:
            return
    elif type_input == 'plain':
        if color_input in ['black','orange']:
            bricklayers.append(json_entry_template % ('glasscolored-%s-%s' % (type_input, color_input), mix_temp))
        else:
            basegame.append(json_entry_template %(('glass-%s' % color_input), mix_temp))
    else:
        bricklayers.append(json_entry_template %('glasscolored-%s-%s' % (type_input, color_input), mix_temp))

for ti, ci in itertools.product(glass_types, glass_colors):
    generate_color_code(ti,ci)

print(json_template % (',\n'.join(basegame)))
print()
print(json_template % (',\n'.join(bricklayers)))
