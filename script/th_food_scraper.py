import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


url = "https://inmu2.mahidol.ac.th/thaifcd/search_food_by_group.php"
driver_path = "../driver/chromedriver.exe"
export_path = "../th_food_item_options_raw.csv"

# # Instantiate export file
# with open(export_path, "w") as f:
#     f.write("|".join(cols) + "\n")

serv = Service(driver_path)
driver = webdriver.Chrome(service=serv)
driver.get(url)

food_groups_sb = driver.find_element(By.XPATH, '//*[@id="frmfood_group_id"]')
food_groups = [x.text for x in food_groups_sb.find_elements(By.TAG_NAME, "option")]

food_add_on = [
    "A16",
    "C100",
    "C122",
    "D293",
    "E118",
    "E184",
    "E187",
    "E5",
    "F152",
    "G225",
    "G5",
    "G65",
    "G73",
    "N72",
    "T171",
    "T272",
]

for food_group in food_groups[1:]:

    food_groups_sb = driver.find_element(By.XPATH, '//*[@id="frmfood_group_id"]')
    food_groups_sb.send_keys(food_group)
    main_search_btn = driver.find_element(
        By.XPATH, '//*[@id="form1"]/div[1]/table/tbody/tr[3]/td[2]/input'
    )
    main_search_btn.click()
    food_tb = driver.find_element(By.XPATH, '//*[@id="form1"]/div[4]/table')

    # found_checkpoint = False  # find checkpoint
    for row in food_tb.find_elements(By.TAG_NAME, "tr")[1:]:

        row_data = []
        nutr_link = ""
        for cell in row.find_elements(By.TAG_NAME, "td")[1:]:
            if cell.text is None:
                continue

            row_data.append(cell.text)
            if nutr_link == "" and cell.find_elements(By.CSS_SELECTOR, "a"):
                nutr_link = cell.find_element(By.TAG_NAME, "a").get_attribute("href")

        food_info_output = []
        col_names = ["thai_name", "english_name", "scientific_name"]
        food_id = row_data[-1]

        # # find checkpoint
        # if food_id == "E135":
        #     found_checkpoint = True
        # if found_checkpoint is False:
        #     continue

        if food_id not in food_add_on:
            continue

        for k, v in zip(col_names, row_data):
            food_info_output.append([food_id, k, v, ""])

        # row_data.append(nutr_link)
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(nutr_link)

        time.sleep(2)
        nutr_baseweight = driver.find_element(
            By.XPATH, '//*[@id="form1"]/div[4]/div/div[1]/div/div[3]'
        )
        food_info_output.append([food_id, "base_weight", nutr_baseweight.text, ""])
        nutr_tb = driver.find_element(By.XPATH, '//*[@id="div_table_body"]')
        for row in nutr_tb.find_elements(By.TAG_NAME, "div"):
            cells = [cell.text for cell in row.find_elements(By.TAG_NAME, "div")]
            if food_id[0] == "Z":
                if len(cells) != 4:
                    continue
                k, unit, _, v = cells
                food_info_output.append([food_id, k, v, unit])
            else:
                if len(cells) != 3:
                    continue
                k, unit, v = cells
                food_info_output.append([food_id, k, v, unit])

        with open(export_path, "a", encoding="utf-8") as f:
            for row in food_info_output:
                f.write("|".join(row) + "\n")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    back_btn = driver.find_element(By.XPATH, '//*[@id="form1"]/div[5]/a[3]')
    back_btn.click()

driver.quit()
