from selenium import webdriver
import time
import random
from fake_useragent import UserAgent
import json
import re
import io
import csv
from selenium.webdriver.common.by import By

# Функция выгрузки Email со страницы MP

def get_email(link_mp):
    useragent = UserAgent()
    #options
    options = webdriver.FirefoxOptions()

    #change useragent
    options.set_preference('general.useragent.override', useragent.random)
    options.headless = True

    driver = webdriver.Firefox(
        executable_path='/home/twopercent/Python/Parse/Firefox_driver/geckodriver',
        options=options
        )

    try:
        driver.get(url=link_mp)
        driver.set_page_load_timeout(60)
        driver.implicitly_wait(random.randrange(3, 10))
        email_list = driver.find_elements(By.TAG_NAME, 'a')
        count_email = 0
        for item in email_list:
            if '@' in item.text:
                count_email += 1
        if count_email > 1:
            for item in email_list:
                if '@parliament' in item.text:
                    email = item.text
        if count_email == 1:
            for item in email_list:
                if '@' in item.text:
                    email = item.text
        if count_email == 0:
            email = 'No Email'
        return email



    #вывод ошибок
    except ConnectionRefusedError:
        print('Долго грузимся...')
    #код закрытия драйвера
    finally:
        # time.sleep(60)
        driver.close()
        time.sleep(1)
        driver.quit()

# Основная программа

with open('links_to_pages.json', encoding = 'utf-8-sig') as file:
    all_pages = json.load(file)

with open('MP-information.csv', 'w', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(
                    (
                     'Name MP',
                     'Party',
                     'Email'
                    )
                    )

count_page = 0
mp_info = []
for page_name, link_page in all_pages.items():

    useragent = UserAgent()
    #options
    options = webdriver.FirefoxOptions()

    #change useragent
    options.set_preference('general.useragent.override', useragent.random)
    options.headless = True

    driver = webdriver.Firefox(
        executable_path='/home/twopercent/Python/Parse/Firefox_driver/geckodriver',
        options=options
        )

    try:
        driver.get(url=link_page)
        driver.implicitly_wait(random.randrange(3, 10))
        card_members = driver.find_elements(By.CLASS_NAME, 'card-member')
        count_mp = 0
        for item in card_members:
            link_mp = item.get_attribute("href")
            name_mp = item.find_element(By.CLASS_NAME, 'primary-info').text
            party_mp = item.find_element(By.CLASS_NAME, 'secondary-info').text
            email_mp = get_email(link_mp)
            mp_info.append(
                            {
                            'Name': name_mp,
                            'Party': party_mp,
                            'E-Mail': email_mp
                            }
                            )
            count_mp += 1
            print(f'{name_mp} сохранён!')
            with open('MP-information.csv', 'a', encoding='utf-8-sig') as file:   #w меняется на а потому что в файл дозаписываются строки (от слова append)
                writer = csv.writer(file, lineterminator='\n')
                writer.writerow(
                                (
                                 name_mp,
                                 party_mp,
                                 email_mp
                                )
                                )
        count_page += 1
        print(f'Загружено {count_page} страниц')
        with open('mp_information.json', 'w', encoding = 'utf-8-sig') as file:
            json.dump(mp_info, file, indent=4, ensure_ascii=False)


    #вывод ошибок
    except Exception as ex:
        print(ex)
    #код закрытия драйвера
    finally:
        # time.sleep(60)
        driver.close()
        driver.quit()
