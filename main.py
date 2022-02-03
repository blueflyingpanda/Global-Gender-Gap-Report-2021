from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import os.path

LINK = 'https://assets.weforum.org/static/reports/gender-gap-report-2021/v9/index.html'
TABLE_HEADER = 'country;' \
               'gggi2006rank;gggi2006score;gggi2021rank;gggi2021score;' \
               'epo2006rank;epo2006score;epo2021rank;epo2021score;' \
               'ea2006rank;ea2006score;ea2021rank;ea2021score;' \
               'hs2006rank;hs2006score;hs2021rank;hs2021score;' \
               'pe2006rank;pe2006score;pe2021rank;pe2021score\n'


def get_data(page) -> str:
    soup = BeautifulSoup(page)
    data = soup.find_all('div', {'class': 'sc-jDwBTQ fxLtQa'})
    country_name = soup.find('h1').text
    for i in range(len(data)):
        data[i] = data[i].text  # get list of text from list of divs
    #  form one csv row (country and all indicators)
    return f'{country_name};' \
           f'{data[0]};{data[5]};{data[10]};{data[15]};' \
           f'{data[1]};{data[6]};{data[11]};{data[16]};' \
           f'{data[2]};{data[7]};{data[12]};{data[17]};' \
           f'{data[3]};{data[8]};{data[13]};{data[18]};' \
           f'{data[4]};{data[9]};{data[14]};{data[19]}\n'


def main():
    browser = webdriver.Chrome()
    browser.get(LINK)
    try:
        # if not os.path.isfile('gggr2021.csv'):
        with open('gggi2021.csv', 'w') as csv:
            csv.write(TABLE_HEADER)
            for i in range(1, 157):  # 156 countries
                view = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/*[name()="svg"][2]')))
                view.click()
                country = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="root"]/div/div[3]/a[{i}]')))
                country.click()
                csv.write(get_data(browser.page_source))
                back_to_countries = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div/div[1]/a[1]')))
                back_to_countries.click()
    except NoSuchElementException:
        print('no such element')
        browser.close()
    except TimeoutException:
        print('timeout')
        browser.close()


if __name__ == '__main__':
    main()