from selenium import webdriver
import time

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Remote(
    command_executor='http://localhost:5000',
    options=chrome_options
)

# time.sleep(10)

driver.get("http://www.google.com")

driver.quit() 