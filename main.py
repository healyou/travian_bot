from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from command.settext import SetTextCommand
from command.clicklink import ClickLinkCommand
from element.wait import *

browser = Chrome(executable_path="install/chromedriver.exe")
browser.get('https://vk.com/')

set_login = SetTextCommand(ElementById(browser, 'index_email'), text='healyou1994@gmail.com')
set_login.execute()

set_psw = SetTextCommand(ElementById(browser, 'index_pass'), text='test')
set_psw.execute()

login = ClickLinkCommand(browser.find_element_by_id('index_login_button'))
login.execute()

try:
    news = ClickLinkCommand(WaitElementById(browser=browser, id='l_fr'))
    news.execute()
except:
    print ('Компонент не виден')
finally:
    print('exit')
