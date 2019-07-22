from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = Chrome(executable_path="install/chromedriver.exe")
browser.get('https://vk.com/')

email = browser.find_element_by_id('index_email')
email.click()
email.clear()
email.send_keys('healyou1994@gmail.com')

password = browser.find_element_by_id('index_pass')
password.click()
password.clear()
password.send_keys('jhDfY57')

login = browser.find_element_by_id('index_login_button')
login.click()

# sleep(1)

# wait for element
try:
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "l_fr"))
    )

    news = browser.find_element_by_id('l_fr')
    if (news.is_displayed()):
        print ('Компонент виден')
        news.click()
    else:
        print ('Компонент не виден')
except:
    print ('Компонент не виден')
finally:
    print('exit')
