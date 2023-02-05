import time
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from DirectoryHandler import DirectoryHandler
import datetime


def scrape_member_links(parliament_start, parliament_end):
    """Retrieves house of commons individual member links over specified range of parliaments.

    Parameters
    ----------
    parliament_start: int
    parliament_end: int

    Returns
    -------
    Nothing

    """
    dh_member_links = DirectoryHandler("members_xml links")
    dh_member_links.load_meta_file()
    dh_member_links.file_existing()
    link_dir = dh_member_links.path_of_interest
    output_list = []

    url = r"https://www.ourcommons.ca/Members/en/search?parliament={}&caucusId=all&province=all&gender=all"
    # https://www.ourcommons.ca/Members/en/search/xml?parliament=43&caucusId=all&province=all&gender=all  # this is the URL for the xml of the sitting members

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
        output_list.append(f'parl_{p}.txt')
    driver.close()

    dh_member_links.create_meta_file(
        source_date=datetime.datetime.now(),
        source_name="House of Commons Canada",
        source_dict={
            "url": "https://www.ourcommons.ca/members/en",
            "filenames": output_list
        }
    )
