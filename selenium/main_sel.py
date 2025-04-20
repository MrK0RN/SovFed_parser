import random
import time

import pyautogui

from selenium import webdriver

import time

import config
import scrap

scrap = scrap.Scraper()
scrap.parse_links_from_files()

browser = webdriver.Chrome()
time.sleep(2)
pyautogui.moveTo(400, 300, 40)

for personal_link in scrap.personal_links:
    print(personal_link)
    full_link = config.base_link + personal_link
    id = personal_link.split("/")[-2]
    browser.get(full_link)
    scrap.save_html_to_file(id, browser.page_source)
    pyautogui.moveTo(300, 400, 10)
    time.sleep(10)
    pyautogui.moveTo(400, 300, 10)
    time.sleep(10)
    pyautogui.moveTo(400, 500, 10)