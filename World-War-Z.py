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
all_zombies: LIST: contains data on the location of all zombies
one_zombie: INT: keeps track while adding location of zombies to all_zombies

game_map: LIST: the returned list that stores the game map
"""
def load_map(text_file):
    game_map = []
    all_zombies = []
    one_zombie = 0
    
    # Open and read the file, then split into lines
    with open(text_file, 'r') as game_source:
        source_raw = game_source.read()
    source_lines = source_raw.splitlines()
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
    
    # Locate all zombies in the map, and append within a list as the final list value
    while True:
        if one_zombie >= len(source_raw):
            break
        # End if one_zombie
        try:
            one_zombie += source_raw.find('Z', one_zombie)
            line = (one_zombie / source_line_length)
            all_zombies.append([line, one_zombie-(line*source_line_length)])
            one_zombie += 1
        except ValueError:
            break
    # End while True

    # Load game data into all_zombies
    for l in range(len(source_lines)):
        one_row = [source_lines[l][i] for i in range(len(source_lines[l]))]
        game_map.append(one_row)
    # End for l 
    game_map.append(all_zombies)

    return game_map