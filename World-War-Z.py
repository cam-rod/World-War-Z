# Cameron Rodriguez
# DATE GOES HERE
# This program is a game that determines whether humans are kept safe from zombies.

# This module is used to validate the source text file.
import re

"""
This function will read the file, verify the data, and save it to a list.

text_file: STR: the location of the file containing the game map

game_source: FILE:  the file that contains the text form of the game map
source_raw: STR: raw form of the entire file, used for verification
source_lines: LIST: a list storing each line of game_source, used to load game_map
source_line_length: INT: contains the length of the first line, to ensure all lines are the same length
total_zombies: INT: a count of how many zombies are in the file

game_map: LIST: the returned list that stores the game map
"""
def load_map(text_file):
    game_map = []
    
    # Open and read the file, then split into lines
    with open(text_file, 'r') as game_source:
        source_raw = game_source.read()
    source_lines = source_raw.splitlines()
   
    # Determine length of first line for rectangle verification
    source_line_length = len(source_lines[0])
    
    # Validate game_source has 1 human, only contains valid characters, and is a rectangle
    if len(re.findall('H', source_raw)) == 1:
        if re.search(r'[^HWTZ.\n]', source_raw) is None:
            for l in source_lines[1:]:
                if len(l) == source_line_length:
                    continue
                else:
                    return False
                # End if len(l)
            # End for l, file has been validated
        else:
            return False
        # End if re.search        
    else:
        return False        
    # End if re.findall
    
    # Load game data into list; appends each character into a list, which is appended to the list game_map
    for l in range(len(source_lines)):
        one_row = [source_lines[l][i] for i in range(len(source_lines[l]))]
        game_map.append(one_row)
    # End for l 
    
    # Determine how many zombies are in the map, and append as the final list value
    total_zombies = len(re.findall('Z', source_raw))
    game_map.append(total_zombies)
    
    return game_map

"""
This function will determine an initial zombie for the invasion to begin with.

map: LIST: contains the map used by the zombie invasion

location: LIST: the returned list that provides the location of the first zombie
"""
def first_zombie(map):
    # Scan each spot for a zombie, and end the loop when a zombie is found
    for i in range(len(map)):
        for j in range(len(map[i])):
            
