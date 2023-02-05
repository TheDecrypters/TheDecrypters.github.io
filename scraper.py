from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def scrape_clues(clue_category):
    clue_category_class_name = 'aclues' if clue_category == 'across' else 'dclues'

    clues_el = driver.find_element(By.CLASS_NAME, clue_category_class_name)
    clue_divs = clues_el.find_elements(By.CLASS_NAME, "clueDiv")

    for clue in clue_divs:
        clue_num_el = clue.find_element(By.CLASS_NAME, "clueNum")
        clue_text_el = clue.find_element(By.CLASS_NAME, "clueText")

        clue_text = clue_text_el.get_attribute('textContent')
        clue_num = clue_num_el.get_attribute('textContent')
        letters = clue_text.split(' ')[-1]

        write_clue_file(path + folder_name, clue_num,
                        clue_text, title, letters, clue_category)


def write_post_file(path):
    with open(f'{path}.md', 'w+') as f:
        f.write(f'''---
title: '{title}'
date: {y+'-'+m+'-'+d}
tags:
  - cryptic
  - posts
layout: layouts/post.njk
---''')


def write_clue_file(path, clue_num, clue_text, puzzle_title, letters, clue_category):
    with open(f'{path}/clues/{clue_category}/' + clue_num.zfill(2) + '_' + clue_text.replace(' ', '_').lower() + '.md', 'w+') as f:
        f.write(f'''---
layout: layouts/clue.njk
tags: clue
puzzle: '{puzzle_title}'
clue: '{clue_text}'
clue_num: '{clue_num}'
clue_category: '{clue_category}'
letters: '{letters}'
answer: ''
straight_is_first: ''
straight: ''
cryptic: ''
---
<li> → <b></b></li>''')


date = '2023/01/22'

# Navigate to the crossword in the the browser
driver = webdriver.Chrome()
url = f'https://www.newyorker.com/puzzles-and-games-dept/cryptic-crossword/{date}'
driver.get(
    url)
title = driver.find_element(By.TAG_NAME, "h1").text
WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
    (By.CSS_SELECTOR, "iframe[title='Embedded Crossword']")))

# Create the necessary folders
y, m, d = date.split('/')[-3:]
folder_name = y + '_' + m + '_' + d
path = os.getcwd() + '/puzzles/'
Path(path + folder_name).mkdir(parents=True, exist_ok=True)
Path(path + folder_name + '/clues/').mkdir(parents=True, exist_ok=True)
Path(path + folder_name + '/clues/across').mkdir(parents=True, exist_ok=True)
Path(path + folder_name + '/clues/down').mkdir(parents=True, exist_ok=True)

# Create the top-level post
write_post_file(path + folder_name + '/' + folder_name)

# Scrape the across clues, and create a post for each one
scrape_clues('across')
scrape_clues('down')

driver.close()
