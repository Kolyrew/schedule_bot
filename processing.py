from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_button(group_number, buttons):
    target_button = None
    for button in buttons:
        button_text = button.text
        if group_number in button_text:
            target_button = button
            return target_button
    return None

def delete_excess(line):
    substrings_to_remove = ["Потокпоказать группы", "СДО"]
    for substring in substrings_to_remove:
        line = line.replace(substring, '')
    return line.strip()

def markup_other_info(other_info):
    lines = other_info.split('\n')
    processed_lines = [delete_excess(line) for line in lines]
    result_string = '\n'.join(filter(lambda x: x.strip(), processed_lines)) + "\n\n"
    return result_string
