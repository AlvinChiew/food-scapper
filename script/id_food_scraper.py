from time import sleep
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

url = "http://www.panganku.org/en-EN/semua_nutrisi"
driver_path = "../driver/chromedriver.exe"
export_path = "../id_food_item_options_raw.csv"

serv = Service(driver_path)
driver = webdriver.Chrome(service=serv)
driver.get(url)


def fetch_tb(driver):

    # Expand table to get all rows
    entries_count = Select(
        driver.find_element(By.XPATH, '//*[@id="data_length"]/label/select')
    )
    entries_count.select_by_value("25")
    entries_count.select_by_value("-1")

    return driver.find_element(By.XPATH, '//*[@id="data"]/tbody')


food_tb = fetch_tb(driver)
food_item_count = len(food_tb.find_elements(By.TAG_NAME, "tr"))

for i in tqdm(range(food_item_count)):
    food_tb = fetch_tb(driver)  # re-fetch table after clicking `back` later
    food_item = food_tb.find_elements(By.TAG_NAME, "tr")[i]
    food_info = [x.text for x in food_item.find_elements(By.TAG_NAME, "td")]

    food_item.click()
    food_base_weight = driver.find_element(
        By.XPATH, '//*[@id="print-area"]/p/strong[1]'
    ).text
    food_edible_base_weight = driver.find_element(
        By.XPATH, '//*[@id="print-area"]/p/strong[2]'
    ).text
    food_base_weight, food_edible_base_weight

    food_info_output = []
    food_info_name = ["food_name", "food_group", "food_type"]
    food_id = food_info[1]
    for k, v in zip(food_info_name, food_info[2:]):
        food_info_output.append([food_id, k, v])
    food_info_output.append([food_id, "base_weight", food_base_weight])
    food_info_output.append([food_id, "base_weight_edible", food_edible_base_weight])

    food_detail_tb = driver.find_element(
        By.XPATH, '//*[@id="print-area"]/div[2]/section/div'
    )
    food_detail_rows = food_detail_tb.find_elements(By.TAG_NAME, "tr")

    for row in food_detail_rows:
        if row.text.strip() == "" or row is None:
            continue
        k, v = row.find_elements(By.TAG_NAME, "td")
        food_info_output.append([food_id, k.text, v.text])

    with open(export_path, "a", encoding="utf-8") as f:
        for i in food_info_output:
            f.write("|".join(i) + "\n")

    driver.back()

driver.quit()
