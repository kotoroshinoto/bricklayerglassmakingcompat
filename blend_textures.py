import string
import os
import sys
import path
import itertools
from PIL import Image,ImageChops
from pathlib import Path


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

source = Path("bricklayer_glass_block_textures")

overlays = dict()
special_base = {'dark', 'opaque'}
has_alternate_normal_for_plain = {'black', 'orange', None}

for glass_type in {'milky', 'quartz', 'smoky'}:
    overlay = Image.open(source / 'glass' / ('overlay_%s.png' % glass_type))
    overlays[glass_type] = overlay
    #print(glass_type, 'mode:', overlay.mode)
        
for glass_type in glass_types:
    if glass_type in overlays:
        overlay = overlays[glass_type]
    else:
        overlay = None
    print("TYPE:", glass_type)
    for glass_color in glass_colors:
        print("\tCOLOR:", glass_type)
        if glass_color == 'white':
            if glass_type != 'opaque':
                print("\tSKIP")
                continue
        if glass_color is None and glass_type not in {'plain', 'milky', 'quartz', 'smoky'}:
            print("\tSKIP")
            continue
        if glass_type in special_base:
            base_path = source / 'glass' / glass_type / ('%s.png' % glass_color)
        else:
            if glass_color in has_alternate_normal_for_plain:
                if glass_color is None:
                    color_name = 'plain_normal'
                else:
                    color_name = '%s_normal' % glass_color
            else:
                color_name = glass_color
            base_path = source / 'glass' / 'normal' / ('%s.png' % color_name)
        if not base_path.exists() or base_path.is_dir():
            print("\tCOULDN'T OPEN BASE:", base_path)
            continue
        base = Image.open(base_path).convert(mode='RGBA')
        #print(color_name, 'mode:', base.mode)
        if overlay is None:
            blended = base
        else:
            try:
                blended = ImageChops.overlay(base, overlay)
            except Exception as e:
                print("exception with inputs:", glass_type, glass_color, color_name, base.size, overlay.size)
                print(base.mode, overlay.mode)
                raise e
        if glass_color is None:
            if glass_type == 'plain':
                save_name = '%s_%s.png' % (glass_type,'nocolor')
            elif glass_type in {'milky','quartz','smoky'}:
                save_name = '%s_%s.png' % (glass_type, 'smoky')
            else:
                continue
        else:
            save_name = '%s-%s.png' % (glass_type, glass_color)
        print("\tSUCCESS")
        blended.save(save_name)