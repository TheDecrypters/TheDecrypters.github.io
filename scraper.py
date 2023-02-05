from genericpath import exists
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from pathlib import Path

def build_clue(clue_num, clue, letters):
    return {
        "clue_num": clue_num,
        "clue": clue,
        "letters": letters,
        "answer": "",
        "straight": "",
        "cryptic": "",
        "straight_is_first": False,
        "explanation": "",
    }

driver = webdriver.Chrome()
url =  'https://www.newyorker.com/puzzles-and-games-dept/cryptic-crossword/2023/01/29'
driver.get(
   url)
title = driver.find_element(By.TAG_NAME, "h1").text
WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
    (By.CSS_SELECTOR, "iframe[title='Embedded Crossword']")))

puzzle = {
    "title": title,
    "clues": {
        "across": [],
        "down": [],
    },
}

# Add the across clues
a_clues_el = driver.find_element(By.CLASS_NAME, "aclues")
a_clue_divs = a_clues_el.find_elements(By.CLASS_NAME, "clueDiv")
for clue in a_clue_divs:
    clue_num_el = clue.find_element(By.CLASS_NAME, "clueNum")
    clue_text_el = clue.find_element(By.CLASS_NAME, "clueText")
    clue_text = clue_text_el.text

    puzzle["clues"]["across"].append(
        build_clue(
            clue_num_el.text,
            ' '.join(clue_text.split(' ')[:-1]),
            clue_text.split(' ')[-1]
        )
    )

# Add the down clues
d_clues_el = driver.find_element(By.CLASS_NAME, "dclues")
d_clue_divs = d_clues_el.find_elements(By.CLASS_NAME, "clueDiv")
for clue in d_clue_divs:
    clue_num_el = clue.find_element(By.CLASS_NAME, "clueNum")
    clue_text_el = clue.find_element(By.CLASS_NAME, "clueText")
    clue_text = clue_text_el.text

    puzzle["clues"]["down"].append(
        build_clue(
            clue_num_el.text,
            ' '.join(clue_text.split(' ')[:-1]),
            clue_text.split(' ')[-1]
        )
    )

driver.close()

json_object = json.dumps(puzzle, indent=2)

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

Path(path + folder_name + '/clues/').mkdir(parents=True, exist_ok=True)
Path(path + folder_name + '/clues/across').mkdir(parents=True, exist_ok=True)
for clue in puzzle['clues']['across']:
        with open(path + folder_name + '/clues/across/' + clue["clue_num"].zfill(2) + '_' + clue["clue"].replace(' ','_').lower() + '.md', 'w+') as f:
            f.write(f'''---
layout: layouts/clue.njk
tags: clue
puzzle: '{puzzle['title']}'
clue: '{clue['clue']}'
clue_num: '{clue['clue_num']}'
clue_category: 'across'
letters: '{clue['letters']}'
answer: '{clue['answer']}'
straight_is_first: '{'true' if clue['straight_is_first'] else 'false'}'
straight: '{clue['straight']}'
cryptic: '{clue['cryptic']}'
---
<li> → <b></b></li>''')

Path(path + folder_name + '/clues/down').mkdir(parents=True, exist_ok=True)
for clue in puzzle['clues']['down']:
        with open(path + folder_name + '/clues/down/' + clue["clue_num"].zfill(2) + '_' + clue["clue"].replace(' ','_').lower() + '.md', 'w+') as f:
            f.write(f'''---
layout: layouts/clue.njk
tags: clue
puzzle: '{puzzle['title']}'
clue: '{clue['clue']}'
clue_num: '{clue['clue_num']}'
clue_category: 'down'
letters: '{clue['letters']}'
answer: '{clue['answer']}'
straight_is_first: '{'true' if clue['straight_is_first'] else 'false'}'
straight: '{clue['straight']}'
cryptic: '{clue['cryptic']}'
---
<li> → <b></b></li>''')

y,m,d = url.split('/')[-3:]
with open('puzzles_json/' + y + '_' + m + '_' + d + '.json', 'w') as outfile:
    outfile.write(json_object)