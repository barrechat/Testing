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
        driver.quit()

