import selenium
import time
from constant import *
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_driver(driver_path):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values.notifications': 2}
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(
        executable_path=driver_path, chrome_options=chrome_options
    )
    return driver

def login(driver,login):
    driver.get('https://www.facebook.com/')
    login_element = driver.find_element_by_name('email')
    password_element = driver.find_element_by_name('pass')
    enter_element = driver.find_element_by_name('login')
    login_element.send_keys(login)
    password_element.send_keys(getpass('Password: '))
    enter_element.click()

def get_friend_list(driver,friends_range):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")    
    time.sleep(10)
    friend_list = []
    for iter in range(friends_range):
        items = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,FRIEND_PATH.format(iter+1))))
        friend_list.append(
            items.find_element_by_xpath('.//div[2]/div[1]/a/span')
                .get_attribute('innerText')
        )
    return friend_list

def click_object(driver, xpath):
    profile = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,xpath)
            )).click()

def write_to_file(path,list_):
    file = open(path,'w',encoding='utf-8')
    for item in list_:
        file.write(str(item)+'\n')
    file.close()

def workflow():
    driver = get_driver(DRIVER_PATH)
    login(driver,LOGIN)
    click_object(driver,PROFILE_PATH)
    click_object(driver,FRIENDS_PATH)
    friend_list = get_friend_list(driver,FRIENDS_RANGE)
    write_to_file(FILE_PATH,friend_list)




if __name__ == "__main__":
    workflow()    
