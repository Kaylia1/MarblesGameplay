
# Dependencies
- python3
- selenium `pip3 install selenium`
- tkinter `pip3 install tk`

# Run Instructions 
cd into marbles top folder
- python3 points.py

# Assumed Input Guidelines
- marbles_output.txt is exactly copy-pasted from the Marbles on Stream game, and follows the exact format of data/MoneyMarbles.csv

# Rulebook - Monopoly Marbles Rules
1: RANK ONE MARBLE-    can FORCIBLY swap places with anyone in the top 10
                       BESIDES MARBLE GOD

2: LEVEL ONE MARBLE-   very low freedom, someone with a higher level marble may
                       be able to take your role since they choose first. 

3: LEVEL TWO MARBLE-   can trade with another player's FIRST PLACE marble that
                       is Lvl2 or lower WITH CONSENT

3: LEVEL THREE MARBLE- similar to above,can trade with Lvl3's or lower WITH CONSENT
                       
4: LEVEL FOUR MARBLE- enjoy your freedom, or you can trade with anyone else's first 
                      place if below Lvl4

6: MARBLE GOD MARBLE- you take priority, pick everyone's champ & role...be nice
   
7: LEVEL ZERO MARBLE- really sorry. You are last pick, the group decides between
                      your top 5 Lvl1 marbles for that role

        Pick order goes MARBLE GOD > WHEEL > RANK 1 > LEVELS 4, 3, 2, 1, 0
                                ties broken by marble placement 
        Kills:   $4
        Assists: $1
        Deaths: -$3
        SPIN=  $100

## Rule Flow
The rules for role assignments are as follows:
1. Get the top marble for ea of 5 ppl.
2. Check if any person's top 1 is marble god
3. Top 1 can choose to swap marbles with any of the top 10 marbles
4. Allocate roles to people according to highest marble level in decreasing order, tiebreak via marble placement
  - if a role is already taken and they can't be assigned that role, get that person's next placing marble of the same marble level
  - if any of the newly retrieved marbles are marble god, throw that result out too
5. Show 5 allocations.
6. n number of Wheel spin(s) adjustments

# TODO
- PARALYZED, test freedom
- make wheel spin after picking rather than after winning
  - wheel spin updates are manual currently, make this a map to functions so that it is scalable
- print champions by letter!
  - if not enough champs under a letter (ie all 5 people get V), add option to go to next marble. Leave margin of error=1
- EOD game stats?
  - winrate, kda, $ change, percentage of times assigned position

- UI
  - crying emoji everytime Kaylia gets top

# edge cases:
- top 1 no longer picks first if they pick into paralysis
- "next marble of same marble level" is a marble in a placement larger than the current marble assignment, ie if after paralysis you get assigned your 3rd lvl1 marble, your next lvl1 marble would be your 4th lvl1 marble
- marbles currently only supports 1 letter prefixes due to winrate logic