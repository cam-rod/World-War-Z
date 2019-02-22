# Steps to get this to work

## Requirements

- RECURSION
- Open a file
- Expands zombie by 1 each time
  - Check if there are any zombies (Error catching)
  - Checks if 15 zombies in line (all directions) and defense
  - printing each move is **OPTIONAL**
  
## Parts

- Open a file
  - Check if the file is valid (if Z=0, declare) (if not a box, declare: 15x40, no spaces) (only allowed characters:```. Z H T W```
  - Read the file
  - Place each item into a nested list [row][column]
- Begin the zombie invasion
  - Use the initial zombie to scan [up][down][left][right]
  - Determine what is in the corresponding spot
  - [ ] If a dot, fill
  - [ ] If a human, kill and check for other humans
  - [ ] If a zombie, check the next direction
  - [ ] If a wall, check for 15 in a row, and then check if something behind it, then immediately fill with zombie
  - [ ] if it cannot move, check the spot in SAME order (right/left/down/up) for a zombie and use that. Repeat as necessary; upon reaching the original zombie, search for other original zombies, then end the game.

Wingware Code 6N31E-RY9CY-J9VTQ-6KJD5

E:/ICS4U1/World-War-Z/Requirements/1.04 Testing Files/

**OR**

C:/Users/rodriguezc/World-War-Z/Requirements/1.04 Testing files/

CREATE GLOBAL VARS (despite my internal strife)
