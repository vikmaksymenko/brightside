from selenium import webdriver
import time

# Not really a test, just a sample script for debugging
# TODO: add a real tests here

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Remote(
    command_executor="http://localhost:4444",
    options=chrome_options
)


driver.get("http://www.google.com")

time.sleep(30)

driver.quit() 