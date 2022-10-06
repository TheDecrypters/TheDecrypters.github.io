from genericpath import exists
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
url =  'https://www.newyorker.com/puzzles-and-games-dept/cryptic-crossword/2022/10/02'
driver.get(
   url)
title = driver.find_element(By.TAG_NAME, "h1").text
WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
    (By.CSS_SELECTOR, "iframe[title='Embedded Crossword']")))

clues = []

a_clues_el = driver.find_element(By.CLASS_NAME, "aclues")
a_clues = a_clues_el.find_elements(By.CLASS_NAME, "clueText")
for clue in a_clues:
    clues.append(clue.text)

d_clues_el = driver.find_element(By.CLASS_NAME, "dclues")
d_clues = d_clues_el.find_elements(By.CLASS_NAME, "clueText")
for clue in d_clues:
    clues.append(clue.text)

driver.close()
y,m,d = url.split('/')[-3:]
folder_name=m+'_'+d+'_'+y
from pathlib import Path
import os
path = os.getcwd()+'/puzzles/'
Path(path+folder_name).mkdir(parents=True, exist_ok=True)
with open(path+folder_name+'/'+folder_name + '.md', 'w+') as f:
    f.write(f'''---
title: '{title}'
date: {y+'-'+m+'-'+d}
tags:
  - cryptic
  - posts
layout: layouts/post.njk
---
This puzzle sucked 

-Rex

## Clues
    ''')
  
for clue in clues:
    Path(path+folder_name+'/clues/').mkdir(parents=True, exist_ok=True)
    with open(path+folder_name+'/clues/' + clue.replace(' ','_').lower()+'.md', 'w+') as f:
        f.write(f'''---
layout: layouts/clue.njk
tags: clue
puzzle: '{title}'
clue: '{' '.join(clue.split(' ')[:-1])}'
letters: '{clue.split(' ')[-1]}'
answer:
straight:
cryptic:
straight_is_first:
---
<li><\li>''')