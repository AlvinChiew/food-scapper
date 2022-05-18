from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time

url = "https://i.fnri.dost.gov.ph/fct/library/food_content/all"
driver_path = "../driver/chromedriver.exe"
export_path = "../ph_food_item_options_raw_foodlist.csv"


cols = ["food_id", "food_name", "scientific_name", "common_name", "edible_portion"]

with open(export_path, "w", encoding="utf-8") as f:
    f.write("|".join(cols) + "\n")


serv = Service(driver_path)
driver = Chrome(service=serv)

driver.get(url)
time.sleep(20)

records_per_page_btn = driver.find_element(
    By.XPATH,
    "/html/body/div[2]/div[3]/div/div/div[1543]/div[2]/div[3]/div[1]/span[2]/span/button",
)
records_per_page_btn.click()
records_per_page_100 = driver.find_element(
    By.XPATH,
    "/html/body/div[2]/div[3]/div/div/div[1543]/div[2]/div[3]/div[1]/span[2]/span/ul/li[4]/a",
)
records_per_page_100.click()

ended = False
while ended is False:
    food_datatable = driver.find_element(
        By.XPATH, "/html/body/div[2]/div[3]/div/div/div[1543]/div[2]/div[2]/table/tbody"
    )
    rows = food_datatable.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        vals = []
        cols = row.find_elements(By.TAG_NAME, "td")
        for col in cols[:-1]:
            vals.append(col.text)

        with open(export_path, "a", encoding="utf-8") as f:
            f.write("|".join(vals) + "\n")

    try:
        next_page_btn = driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div[3]/div/div/div[1543]/div[2]/div[3]/div[2]/ul/li[8]/a",
        )
        next_page_btn.click()
    except:
        ended = True
    print(ended)

driver.quit()
