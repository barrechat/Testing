from selenium import webdriver
import pytest
import pytest_html_reporter
from pytest_html_reporter import attach
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By



def setup_module(self):
        global driver 
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.implicitly_wait(30)
        driver.minimize_window()
        driver.get("http://127.0.0.1:5500/comparacion.html")
    
        

def test_Texto():
        texto = driver.find_element(By.ID,"texto").text
        assert texto == "Texto x"

def test_Imagen():
        ruta = driver.find_element(By.ID,"imagen").get_attribute("src")
        assert ruta == "http://127.0.0.1:5500/img/selenium.png"

def test_Boton():
    assert driver.find_element(By.ID,"boton").is_enabled()

def teardown_module():
    attach(data=driver.get_screenshot_as_png())
    driver.quit()
