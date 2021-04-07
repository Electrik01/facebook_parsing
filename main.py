import selenium
import time
from constant import *
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

def scroll_down(driver):
    time.sleep(2)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height



def get_driver(driver_path):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values.notifications': 2}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        executable_path=driver_path, chrome_options=chrome_options
    )
    return driver

def loginToFacebook(driver,login,password):
    driver.get('https://www.facebook.com/')
    login_element = driver.find_element_by_name('email')
    password_element = driver.find_element_by_name('pass')
    enter_element = driver.find_element_by_name('login')
    login_element.send_keys(login)
    password_element.send_keys(password)
    enter_element.click()

def get_friend_list(driver):
    friend_list = []
    iter = 1     
    scroll_down(driver)
    while True:
        try:
            items = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,FRIEND_PATH.format(iter))))
            friend_list.append(
                [
                items.find_element_by_xpath("div[2]/div[1]").text,
                items.find_element_by_tag_name('a').get_attribute("href")
                ])
            iter+=1
        except TimeoutException:
            break
    return friend_list

def click_object(driver, xpath):
    #driver.execute_script("window.scrollTo(0, 0);")
    profile = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,xpath)
            )).click()

def write_to_file(path,list_):
    file = open(path,'w',encoding='utf-8')
    for item in list_:
        file.write('{}   |  {}\n'.format(item[0],item[1]))
    file.close()

def workflow():
    login = input("Login: ")
    password = getpass("Password: ")
    driver = get_driver(DRIVER_PATH)
    loginToFacebook(driver,login,password)
    click_object(driver,PROFILE_PATH)
    click_object(driver,FRIENDS_PATH)
    friend_list = get_friend_list(driver)
    write_to_file(FILE_PATH,friend_list)



if __name__ == "__main__":
    workflow()    
