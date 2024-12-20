import undetected_chromedriver as uc
import time
import unicodedata
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

options = uc.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-images")
options.add_argument("--no-sandbox")
options.add_argument("--headless")

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"

driver = uc.Chrome(version_main=130, options=options, desired_capabilities=caps)

def start():
    house_id = 1

    try:
        driver.get("https://www.avito.ru/rostov-na-donu/kvartiry?context=H4sIAAAAAAAA_wEjANz_YToxOntzOjg6ImZyb21QYWdlIjtzOjc6ImNhdGFsb2ciO312FITcIwAAAA&district=349-350-351-353-354-355-356-357")
        time.sleep(5)

        with open('houses.txt', 'w') as file:
            file.write('ID\tTitle\tPlace\tPrice\n')
            
        scroll()
        house_id = parse_data(house_id)

        while True:
            next_buttons = driver.find_elements(By.CSS_SELECTOR, 'a.styles-module-item-QkAj5.styles-module-item_arrow-gwJ04.styles-module-item_size_s-hLYd4.styles-module-item_link-rcqQ0')

            if next_buttons:
                next_button = next_buttons[-1]
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(5)
                scroll()
                house_id = parse_data(house_id)
            else:
                break

    except Exception as ex:
        print("Error:", ex)
    finally:
        driver.close()
        driver.quit()


def parse_data(house_id):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    houses = soup.select('div.iva-item-root-Se7z4')
    all_houses = []

    for house in houses:
        title_elem = house.select_one('h3')
        title = unicodedata.normalize("NFKD", title_elem.text) if title_elem else "N/A"
        title = parse_string(title, 'title')
        if title == None: continue

        place_elem = house.select_one('p.styles-module-root-s4tZ2.styles-module-size_s-nEvE8.styles-module-size_s_compensated-wyNaE.styles-module-size_s-PDQal.styles-module-ellipsis-A5gkK.styles-module-ellipsis_oneLine-xwEfT.stylesMarningNormal-module-root-_xKyG.stylesMarningNormal-module-paragraph-s-HX94M.styles-module-root_top-f1wIA.styles-module-margin-top_0-j226g')
        place = unicodedata.normalize("NFKD", place_elem.text) if place_elem else "N/A"
        place = parse_string(place, 'place')
        if place == None: continue

        price_elem = house.select_one('strong')
        price = unicodedata.normalize("NFKD", price_elem.text) if price_elem else "N/A"
        if 'месяц' in price: continue
        price = parse_string(price, 'price')
        if price == None: continue

        all_houses.append((house_id, title, place, price))

        house_id += 1

    with open('houses.txt', 'a', encoding='utf-8') as file:
        for house in all_houses:
            file.write(f'{house[0]}\t{house[1]}\t{house[2]}\t{house[3]}\n')
            print(f'{house[0]}\tTitle: {house[1]}\tPlace: {house[2]}\tPrice: {house[3]}\n')

    return house_id


def scroll():
    scroll_pause_time = 0.3
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def parse_string(string, func):
    if func == 'title':
        if 'студия' in string:
            room = 0
        else:
            room = re.search(r'(\d+)-к', string)
            room = int(room.group(1)) if room else None

        area = re.search(r'(\d+[.,]?\d*)\s?м2', string)
        area = float(area.group(1).replace(',', '.')) if area else None

        floor = re.search(r'(\d+)/\d+\s?эт', string)
        floor = int(floor.group(1)) if floor else None

        return [room, area, floor]

    elif func == 'place':
        place = re.search(r"р-н\s+(\S+)", string)
        place = place.group(1) if place else None
        
        return place

    elif func == 'price':
        price = re.search(r"\d[\d\s]*", string)
        price = price.group(0).replace(' ', '') if price else None

        return price

if __name__ == '__main__':
    start()
