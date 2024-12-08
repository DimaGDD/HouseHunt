import undetected_chromedriver as uc
import time
import unicodedata
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import csv

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

        with open('houses.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Room_number', 'Squares', 'Living_squares', 'Floor', 'Place', 'Price'])
            
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

    houses = soup.select('a.iva-item-sliderLink-Fvfau')
    all_houses = []

    for house in houses:
        try:
            link = house['href']
            if not link.startswith("http"):
                link = f'http://ww.avito.ru{link}'

            driver.get(link)
            time.sleep(3)

            detail_html = driver.page_source
            detail_soup = BeautifulSoup(detail_html, "html.parser")

            params = detail_soup.select('li.params-paramsList__item-_2Y2O')
            house_data = {
                "rooms": None,
                "total_area": None,
                "living_area": None,
                "floor": None,
                "price": None,
                "place": None,
            }

            for param in params:
                param_text = param.text.split(":")

                if len(param_text) < 2:
                    continue

                label, value = param_text[0].strip(), param_text[1].strip()

                if "Количество комнат" in label:
                    house_data["rooms"] = 0 if "студия" in value.lower() else int(value.split()[0])
                elif "Общая площадь" in label:
                    house_data["total_area"] = float(value.split()[0].replace(',', '.'))
                elif "Жилая площадь" in label:
                    house_data["living_area"] = float(value.split()[0].replace(',', '.'))
                elif "Этаж" in label:
                    house_data["floor"] = int(value.split()[0])


            price_elem = detail_soup.select_one('span.styles-module-size_xxxl-GRUMY')
            place_elem = detail_soup.select('span')

            if place_elem:
                for x in place_elem:
                    if "р-н" in x.text:
                        place_elem = x.text.split()[1]

            house_data["price"] = price_elem.text.strip().replace('\xa0', '') if price_elem else None
            house_data["price"] = house_data["price"].replace('₽', '') if house_data["price"] else None
            print(int(house_data["price"]))
            if int(house_data["price"]) <= 500000 : continue

            house_data["place"] = place_elem if place_elem else None


            all_houses.append((house_data["rooms"], house_data["total_area"], house_data["living_area"], house_data["floor"], house_data["price"], house_data["place"]))
            print(f'-- {house_id} --', link, all_houses[-1])
            house_id += 1
        except:
            continue
        #     value = param.select_one('span.params-paramsList__item-value-_2FQg').text.strip()

        #     if "комнаты" in label.lower():
        #         house_data["rooms"] = value
        #     elif "этаж" in label.lower():
        #         house_data["floor"] = value
        #     elif "жилая площадь" in label.lower():
        #         house_data["living_area"] = value
        #     elif "площадь" in label.lower() and "жилая" not in label.lower():
        #         house_data["area"] = value

        # price = detail_soup.select_one('span.styles-module-size_xxxl-GRUMY').text.strip()
        # place = detail_soup.select_one('span.style-item-address-georeferences-item-icons-_Zkh_').text.strip()

        # all_houses.append((house_data["rooms"], house_data["floor"], house_data["living_area"], house_data["area"], place, price))
        # print(all_houses)



    # for house in houses:
    #     title_elem = house.select_one('h3')
    #     title = unicodedata.normalize("NFKD", title_elem.text) if title_elem else "N/A"
    #     title = parse_string(title, 'title')
    #     if title == None: continue

    #     place_elem = house.select_one('p.styles-module-root-s4tZ2.styles-module-size_s-nEvE8.styles-module-size_s_compensated-wyNaE.styles-module-size_s-PDQal.styles-module-ellipsis-A5gkK.styles-module-ellipsis_oneLine-xwEfT.stylesMarningNormal-module-root-_xKyG.stylesMarningNormal-module-paragraph-s-HX94M.styles-module-root_top-f1wIA.styles-module-margin-top_0-j226g')
    #     # place = unicodedata.normalize("NFKD", place_elem.text) if place_elem else "N/A"
    #     place = unicodedata.normalize('NFD', place_elem.text) if place_elem else "N/A"
    #     place = parse_string(place, 'place')
    #     if place == None: continue

    #     price_elem = house.select_one('strong')
    #     price = unicodedata.normalize("NFKD", price_elem.text) if price_elem else "N/A"
    #     if 'месяц' in price: continue
    #     price = parse_string(price, 'price')
    #     if price == None: continue

    #     all_houses.append((title[0], title[1], title[2], place, price))

    #     house_id += 1

    try:

        with open('houses.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for house in all_houses:
                writer.writerow(house)
                print(f'{house[0]}\tTitle: {house[1]}\tPlace: {house[2]}\tPrice: {house[3]}\n')
    except Exception as e:
        print(e)

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
        place = ''.join([char for char in string if unicodedata.category(char) != 'Mn'])
        place = re.sub(r'\s+', ' ', place).strip()

        place = re.search(r"р-н\s+(\S+)", place)
        place = place.group(1) if place else None
        
        return place

    elif func == 'price':
        price = re.search(r"\d[\d\s]*", string)
        price = int(price.group(0).replace(' ', '')) if price else None

        return price

if __name__ == '__main__':
    start()
