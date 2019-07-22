from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep

browser = Chrome(executable_path="install/chromedriver.exe")
browser.get('https://vk.com/')

email = browser.find_element_by_id('index_email')
email.click()
email.clear()
email.send_keys('test')

password = browser.find_element_by_id('index_pass')
password.click()
password.clear()
password.send_keys('test')

login = browser.find_element_by_id('index_login_button')
login.click()

sleep(1)

news = browser.find_element_by_id('l_fr')
news.click()