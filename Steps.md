# Steps to get this to work

## Requirements

- RECURSION
- Open a file (does it need to save? does it need to print each time?)
- Expands zombie by 1 each time (Does each zombie get checked EACH TIME?)
  - Check if there are any zombies (Error catching)
  - Checks if 15 zombies in line (all directions) and defense
  
## Parts

- Open a file
  - Check if the file is valid (if Z=0, declare) (if not a box, declare: 15x40, no spaces) (only allowed characters: ```. Z H T W```
  - Read the file
  - Place each item into a nested list [row][column]
- Begin the zombie invasion
  - Use the initial zombie to scan [up][down][left][right]
  - Determine what is in the corresponding spot
  - [ ] If a dot, fill
  - [ ] If a human, kill and check for other humans
  - [ ] If a zombie, check the next direction
  - [ ] If a wall, check for 15 in a row, and then check if something behind it, then remove (can zombies block a wall from breaking? does the zombie immediately fill the space?) (then check for any other walls NEARBY to be broken)ot mo
  - [ ] if it cannot move, check the spot in reverse order (right/left/down/up) for a zombie and use that. Repeat as necessary; upon reaching the original zombie, search for other original zombies, then end the game.
  
Wingware Code 6N31E-RY9CY-J9VTQ-6KJD5
E:/ICS4U1/World-War-Z/Requirements/1.04 Testing Files/
