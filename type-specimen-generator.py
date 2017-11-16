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
    font_names = []

    # Setup options
    current_dir = os.getcwd()
    export_path = current_dir + os.sep +args['export_path']
    font_path = current_dir + os.sep + args['font_path']
    export_format = args['export_format']
    canvas_size_in = args['canvas_size']
    dpi = args['dpi']
    font_size = int(args['font_size']*dpi/72)
    lookup_font_name = args['lookup_font_name']
    
    if lookup_font_name:
        font_path = '/Library/Fonts/'
        file_names = os.listdir(font_path)
        font_name = lookup_font_name
    else:
        # Check in 'fonts' subdirectory for font files
        file_names = os.listdir(font_path)
        font_name = ''
        
    print(file_names)
    for file in file_names:
        if re.search('%s.(?i)(ttf|otf|ttc)' % font_name,file):
            font_names.append(file)

    # Print message if no fonts are found
    if not file_names:
        print("No font files found. Check that fonts are in 'fonts' subdirectory")
    
    # Loop through fonts and create type specimen sheets
    # Set parameters
    spacing = 2 
    x_offset = font_size*3//2
    y_offset = font_size
    y_bottom_offset = font_size*3//2
    y_sep = font_size*3//2
    
    font_opts = {}
    fill_color = (0,0,0,255)
    font_opts['fill'] = fill_color
    

    width_px = int(canvas_size_in[0]*dpi)
    height_px = int(canvas_size_in[1]*dpi)
    
    for font_name in font_names:
        print('Processing {}'.format(font_name[:-4]))
        font = ImageFont.truetype(font_path + os.sep + font_name, font_size)
    
        font_opts['font'] = font
    
        # Create canvas
        txt = Image.new('RGB', [width_px,height_px], (255,255,255))
        d = ImageDraw.Draw(txt)

        d.text((x_offset, y_offset), space_text("ABCDEFGHI",spacing), **font_opts)
        d.text((x_offset, y_offset + y_sep), space_text("JKLMNOPQ",spacing), **font_opts)
        d.text((x_offset, y_offset + 2*y_sep), space_text("RSTUVWXYZ",spacing), **font_opts)

        d.text((x_offset, y_offset + 3*y_sep), space_text("abcdefghi",spacing), **font_opts)
        d.text((x_offset, y_offset + 4*y_sep), space_text("jklmnopq",spacing), **font_opts)
        d.text((x_offset, y_offset + 5*y_sep), space_text("rstuvwxyz",spacing), **font_opts)

        d.text((x_offset, y_offset + 6*y_sep), space_text("0123456789",spacing), **font_opts)
        d.text((x_offset, y_offset + 7*y_sep), space_text(".,!?#%@$&()’-+=/;:",spacing), **font_opts)
    
        d.text((x_offset, height_px - font_size - y_bottom_offset),font_name[:-4], **font_opts)


        txt.save(export_path + os.sep + font_name[:-4] + '.' + export_format,dpi=(dpi,dpi))
        
        
if __name__ == "__main__":
    # Import modules
    import re,os
    from PIL import Image,ImageFont,ImageDraw
    import argparse
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Generate type specimens.')
    parser.add_argument('-e','--export_subfolder',dest='export_path', type=str,
                        nargs='?',default='type specimens',
                        help='specify export path')
    parser.add_argument('-i','--import_subfolder',dest='font_path', type=str,
                        nargs='?',default='fonts',
                        help='specify import path')
    parser.add_argument('-f','--export_format',dest='export_format',type=str,
                        nargs='?',default='png',help="set export format")
    parser.add_argument('-s','--size',dest='canvas_size',type=float,
                        nargs='+',default=[11,8.5],help="set the canvas size in"
                        " inches")
    parser.add_argument('-d','--dpi',dest='dpi',type=int,
                        nargs='?',default=300,help="set the output resolution"
                        "in dots per inch (dpi)")
    parser.add_argument('-p','--font_size',dest='font_size',type=int,
                        nargs='?',default=36,help="set the font size pts"
                        "points")
    parser.add_argument('-l','--lookup_font',dest='lookup_font_name',type=str,
                        nargs='?',default=None,help="lookup system font")               
    
    args = vars(parser.parse_args())
    
    # Check if directory for exported type specimens exists. If not, create it
    if not os.path.exists(args['export_path']):
        os.mkdir(args['export_path'])
        
    create_specimens(args)
    