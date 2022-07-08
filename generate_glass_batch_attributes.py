import string
import os
import sys
import path
import itertools


def expand_variants(types, colors):
    excluded = {
        ('plain', 'smoky'),
        ('opaque', 'smoky'),
        ('dark', 'smoky'),
        ('plain', 'white'),
        ('dark', 'white'),
        ('milky', 'white'),
        ('quartz', 'white'),
        ('smoky', 'white'),
        ('dark', 'nocolor'),
        ('milky', 'nocolor'),
        ('quartz', 'nocolor'),
        ('smoky', 'nocolor'),
        ('opaque', 'nocolor')
    }
    combos = []
    for x in itertools.product(types, colors):
        if x not in excluded:
        #    print('including:', x)
            combos.append(x)
        #else:
        #    print('skipping:', x)
    return combos


def calc_mix_temperature(type_input, color_input):
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


def main_func():
    glass_types = [
        "plain",
        "quartz",
        "milky",
        "smoky",
        "dark",
        "opaque"
    ]
    glass_colors = [
        "nocolor",
        "smoky",
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
    has_special_handbook_text = {('milky', 'smoky'), ('quartz', 'smoky'), ('smoky', 'smoky'), ('plain', 'nocolor')}
    is_basegame_glass = {
        ('plain', 'nocolor'),
        ('plain', 'blue'),
        ('plain', 'brown'),
        ('plain', 'green'),
        ('plain', 'pink'),
        ('plain', 'red'),
        ('plain', 'violet'),
        ('plain', 'yellow'),
        ('quartz', 'smoky'),
        ('milky', 'smoky'),
        ('smoky', 'smoky')
    }
    basegame_glass_name = {
        ('plain', 'nocolor'): 'plain',
        ('plain', 'blue'): 'blue',
        ('plain', 'brown'): 'brown',
        ('plain', 'green'): 'green',
        ('plain', 'pink'): 'pink',
        ('plain', 'red'): 'red',
        ('plain', 'violet'): 'violet',
        ('plain', 'yellow'): 'yellow',
        ('quartz', 'smoky'): 'quartz',
        ('milky', 'smoky'): 'vintage',
        ('smoky', 'smoky'): 'smoky'
    }
    
    double_glass_value = {
        ('plain', 'nocolor'),
        ('quartz', 'smoky'),
        ('milky', 'smoky'),
        ('smoky', 'smoky')
    }
    variant_combos = expand_variants(glass_types, glass_colors)
    json_template = """ {%s}"""
    def generate_entry(combo_tuple):
        json_entry_template = """
		"*-%s": {
			"handbook": {
				"extraSections": [ {
					"title": "handbook-item-usage",
					"text": "handbook-item-usage-glassbatch-%s"
				} ],
				"groupBy": "*-%s-*"
			},
			"glassmaking:glassblend": {
				"code": "%s:%s",
				"amount": %d
			}
        }"""
        gtype = combo_tuple[0]
        gcolor = combo_tuple[1]
        variant_string = '-'.join(combo_tuple)
        if combo_tuple in double_glass_value:
            glass_amount = 500
        else:
            glass_amount = 250
        if combo_tuple in basegame_glass_name:
            domain = 'game'
            glassname = basegame_glass_name[combo_tuple]
        else:
            domain = 'bricklayers'
            glassname = variant_string
        if combo_tuple in has_special_handbook_text:
            handbook_suffix = variant_string
        else:
            handbook_suffix = gtype
        return json_entry_template % (variant_string, handbook_suffix, gtype, domain, glassname, glass_amount)
    print(json_template % ",".join([generate_entry(x) for x in variant_combos]))
    # print('\n'.join(['-'.join(x) for x in variant_combos]))
    return


if __name__ == "__main__":
    main_func()
