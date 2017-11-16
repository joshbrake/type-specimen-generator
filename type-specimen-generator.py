#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 17:47:34 2017

@author: joshbrake

Script to create type specimens. Checks for truetype (.ttf) or opentype fonts
(.otf) in a subdirectory named 'fonts'. Generates type specimens with uppercase
letters, lowercase letters, and numerals. Then, exports .png of type specimen
to subfolder titled 'type specimens'.
"""

def space_text(string,spaces):
    """
    Return a version of the string with the designated number of spaces between each character.
    
    Parameters
    ----------
    string : str
        Input string to be spaced out
    spaces : int
        Number of spaces to put between each character
    
    Returns
    -------
    spaced_string : str
        New string with spaces in between each character
    """
    spaced_string = ''
    for x in string:
        spaced_string += x + ' '*spaces
        
    return spaced_string

def create_specimens(args):
    # Set up font size
    font_size = 200
    font_names = []

    # Setup paths
    current_dir = os.getcwd()
    export_path = current_dir + os.sep +args['export_path']
    font_path = current_dir + os.sep + args['font_path']

    # Check in 'fonts' subdirectory for font files
    file_names = os.listdir(font_path)

    for file in file_names:
        if re.search('.(?i)(ttf|otf)',file):
            font_names.append(file)

    # Print message if no fonts are found
    if not file_names:
        print("No font files found. Check that fonts are in 'fonts' subdirectory")
    
    # Loop through fonts and create type specimen sheets
    # Set parameters
    canvas_size_in = [11,8.5]
    dpi = 300
    spacing = 2 
    x_offset = 150
    y_offset = 100
    y_bottom_offset = font_size*0.75
    y_sep = 300
    file_format = 'png'

    width_px = int(canvas_size_in[0]*dpi)
    height_px = int(canvas_size_in[1]*dpi)
    for font_name in font_names:
        print('Processing {}'.format(font_name[:-4]))
        font = ImageFont.truetype(font_path + os.sep + font_name, font_size)
    
        # Create canvas
        txt = Image.new('RGB', [width_px,height_px], (255,255,255))
        d = ImageDraw.Draw(txt)
    
        d.text((x_offset, y_offset), space_text("ABCDEFGHI",spacing),font=font,fill=(0,0,0,255))
        d.text((x_offset, y_offset + y_sep), space_text("JKLMNOPQ",spacing),font=font,fill=(0,0,0,255))
        d.text((x_offset, y_offset + 2*y_sep), space_text("RSTUVWXYZ",spacing), font=font,fill=(0,0,0,255))
    
        d.text((x_offset, y_offset + 3*y_sep), space_text("abcdefghi",spacing), font=font,fill=(0,0,0,255))
        d.text((x_offset, y_offset + 4*y_sep), space_text("jklmnopq",spacing), font=font,fill=(0,0,0,255))
        d.text((x_offset, y_offset + 5*y_sep), space_text("rstuvwxyz",spacing), font=font,fill=(0,0,0,255))

        d.text((x_offset, y_offset + 6*y_sep), space_text("0123456789",spacing), font=font,fill=(0,0,0,255))
    
        d.text((x_offset, height_px - font_size - y_bottom_offset),font_name[:-4],font=font,fill=(0,0,0,255))
    
    
        txt.save(export_path + os.sep + font_name[:-4] + '.' + file_format,dpi=(dpi,dpi))
        
        
if __name__ == "__main__":
    # Import modules
    import re,os
    from PIL import Image,ImageFont,ImageDraw
    import argparse
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Generate type specimens.')
    parser.add_argument('-e','--export_folder',dest='export_path', type=str,
                        nargs='?',default='type specimens',
                        help='specify export path')
    parser.add_argument('-f','--font_folder',dest='font_path', type=str,
                        nargs='?',default='fonts',
                        help='specify import path')
    
    args = vars(parser.parse_args())
    print(args)
    
    # Check if directory for exported type specimens exists. If not, create it
    if not os.path.exists(args['export_path']):
        os.mkdir(args['export_path'])
        
    create_specimens(args)
    