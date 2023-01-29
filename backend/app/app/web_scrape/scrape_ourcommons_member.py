import time
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import pathlib

project_name = "lobby-force"
data_dir = "data"
save_dir = "data/members_xml"
parliament_start = 36
parliament_end = 44
url = r"https://www.ourcommons.ca/Members/en/search?parliament={}&caucusId=all&province=all&gender=all"
# https://www.ourcommons.ca/Members/en/search/xml?parliament=43&caucusId=all&province=all&gender=all  # this is the URL for the xml of the sitting members

curr_dir_name = os.path.dirname(__file__)

absolute_project_path = None
for i in pathlib.Path(curr_dir_name).parents:
    if i.name == project_name:
        absolute_project_path = i.absolute()
        break

if not os.path.exists(os.path.join(absolute_project_path, data_dir)):
    os.mkdir(os.path.join(absolute_project_path, data_dir))

if not os.path.exists(os.path.join(absolute_project_path, save_dir)):
    os.mkdir(os.path.join(absolute_project_path, save_dir))

save_dir = os.path.join(absolute_project_path, save_dir)
link_dir = os.path.join(save_dir, 'links')

if not os.path.exists(link_dir):
    os.mkdir(link_dir)

options = webdriver.ChromeOptions()
options.add_argument("window-size=1920,1080")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
try:
    driver = uc.Chrome(options=options)
except:
    raise RuntimeError("failed to initialize driver")

driver.get("https://www.google.com")
time.sleep(2)

for p in range(parliament_start, parliament_end + 1):
    formatted_url = url.format(p)

    print(formatted_url)
    driver.get(formatted_url)

    try:
        wait = WebDriverWait(driver, 60)
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ce-mip-mp-tile")))
    except TimeoutException:
        print("timed out")

    t_element = driver.find_elements_by_class_name(name='ce-mip-mp-tile')

    links = []
    for t in t_element:
        fish = t.get_attribute('href')
        links.append(fish+"\n")

    fn = os.path.join(link_dir, f'parl_{p}.txt')
    with open(fn, 'w') as handle:
        handle.writelines(links)

driver.close()
