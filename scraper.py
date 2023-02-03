from genericpath import exists
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def build_clue(clue_num, clue, letters):
    return {
        "clue_num": clue_num,
        "clue": clue,
        "letters": letters,
        "answer": "",
        "straight_explanation": "",
        "straight": "",
        "cryptic": "",
        "straight_is_first": False,
        "type_of_clue": "",
        "explanation": [
            {
                "puzzle_component": "",
                "component_solution": "",
                "parenthetical": ""
            }
        ]
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
    "clues": [],
}

# Add the across clues
a_clues_el = driver.find_element(By.CLASS_NAME, "aclues")
a_clue_divs = a_clues_el.find_elements(By.CLASS_NAME, "clueDiv")
for clue in a_clue_divs:
    clue_num_el = clue.find_element(By.CLASS_NAME, "clueNum")
    clue_text_el = clue.find_element(By.CLASS_NAME, "clueText")
    clue_text = clue_text_el.text

    puzzle["clues"].append(
        build_clue(
            clue_num_el.text + 'a',
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

    puzzle["clues"].append(
        build_clue(
            clue_num_el.text + 'd',
            ' '.join(clue_text.split(' ')[:-1]),
            clue_text.split(' ')[-1]
        )
    )

driver.close()

json_object = json.dumps(puzzle, indent=2)

y,m,d = url.split('/')[-3:]
with open('puzzles_json/' + y + '_' + m + '_' + d + '.json', 'w') as outfile:
    outfile.write(json_object)