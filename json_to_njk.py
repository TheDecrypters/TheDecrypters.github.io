import json
import os
from pathlib import Path
from genericpath import exists
 
with open('puzzles_json/2023_01_29.json', 'r') as openfile:
    puzzle = json.load(openfile)

y, m, d = '2023/01/29'.split('/')[-3:]
folder_name = y + '_' + m + '_' + d
path = os.getcwd() + '/puzzles/'
Path(path + folder_name).mkdir(parents=True, exist_ok=True)

with open(path + folder_name + '/' + folder_name + '.md', 'w+') as f:
    f.write(f'''---
title: '{puzzle['title']}'
date: {y+'-'+m+'-'+d}
tags:
  - cryptic
  - posts
layout: layouts/post.njk
---
    ''')

for clue in puzzle['clues']:
    Path(path + folder_name + '/clues/').mkdir(parents=True, exist_ok=True)
    
    explanation = ''

    for explanation_component in clue['explanation']:
        explanation += f"<li>{explanation_component['puzzle_component']} → <span style='color:green'><b>{explanation_component['component_solution'].upper()}</b></span> ({explanation_component['parenthetical']})</li>"

    with open(path + folder_name + '/clues/' + clue["clue"].replace(' ','_').lower() + '.md', 'w+') as f:
        f.write(f'''---
layout: layouts/clue.njk
tags: clue
puzzle: '{puzzle['title']}'
clue: '{clue['clue']}'
letters: '{clue['letters']}'
answer: '{clue['answer']}'
straight_explanation: '{clue['straight_explanation']}'
straight: '{clue['straight']}'
cryptic: '{clue['cryptic']}'
straight_is_first: '{clue['straight_is_first']}'
type_of_clue: '{clue['type_of_clue']}'
---
{explanation}''')

