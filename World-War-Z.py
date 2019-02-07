# Cameron Rodriguez
# DATE GOES HERE
# This program is a game that determines whether humans are kept safe from zombies.

# This module is used to validate the source text file.
import re

"""
This function will read the file, verify the data, and save it to a list.

text_file: STR: the location of the file containing the game map
game_map: LIST: the list that stores the game map
game_source: FILE:  the file that contains the text form of the game map
source_lines: LIST: a list storing each line of game_source, used to load game_map
l: INT or STR: a variable used to iterate through lines of source_lines, for verification and loading the map
"""
def load_map(text_file):
    game_map = []
    game_source = open(text_file, 'r')
    source_lines = game_source.readlines()
    game_source.seek(0)
    
    # Validate game_source has 1 human, only contains valid characters, and the correct size
    if len(re.findall('H', game_source.read())) == 1:
        game_source.seek(0)
        if re.search(r'[^HWTZ.\n]', game_source.read()) is None:
            game_source.seek(0)
            if source_lines == 15:
                for l in source_lines:
                    if len(l) in [40, 41]:
                        continue
                    else:
                        game_source.close()
                        return False
                    # End if len(l)
                # End for l
            game_source.close()
            # End if source_lines, file is valid
        else:
            game_source.close()
            return False
        # End if re.search        
    else:
        game_source.close()
        return False        
    # End if re.findall
    
    # Load data into list
    for l in xrange(len(source_lines)):
        game_map.append([source_lines[l][0][i] for i in xrange(40)])
    # End for l 
    
    return game_map

t = raw_input("where's the file? ")
a = load_map(t)
if a is False:
    print('uh oh')
else:
    print a