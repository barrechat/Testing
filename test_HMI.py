from selenium import webdriver
import pytest
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By



def setup_module(self):
        global driver 
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
        driver.implicitly_wait(30)
        driver.minimize_window()
        driver.get("http://192.168.1.136/")

def test_Desplegable():
        botonDesplegable = driver.find_element(By.ID,"btn-desplegable")
        botonDesplegable.click()
        widthDesplegado =driver.find_element(By.ID,"menu-options").get_attribute("style")
        botonDesplegable.click()
        widthPlegado = driver.find_element(By.ID,"menu-options").get_attribute("style")
        assert widthPlegado == "width: 65px;" and widthDesplegado == "width: 100%;"

def teardown_module():
    driver.quit()
