from selenium import webdriver
import pytest
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select



def setup_module(self):
        global driver 
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--window-size=1024,730')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
        driver.implicitly_wait(30)
        driver.get("http://192.168.1.136/")

def test_DesplegableFallido():
        """Test de visualizacion de la barra desplegable"""
        botonDesplegable = driver.find_element(By.ID,"btn-desplegable")
        widthDesplegado =driver.find_element(By.ID,"menu-options").get_attribute("style")
        driver.save_screenshot("testsCatedra/capturas/test_DesplegableFallido.png")
        assert widthDesplegado == "width: 100%;"

def test_Desplegable():
        """Test de visualizacion de la barra desplegable"""
        botonDesplegable = driver.find_element(By.ID,"btn-desplegable")
        botonDesplegable.click()
        widthDesplegado =driver.find_element(By.ID,"menu-options").get_attribute("style")
        driver.save_screenshot("testsCatedra/capturas/test_Desplegable.png")
        assert widthDesplegado == "width: 100%;"

def test_TemperaturasFallido():
        """Test de visualizacion de la ventana de temperatura"""
        botonTemperatura = driver.find_element(By.ID,"grafica")
        botonTemperatura.click()
        driver.save_screenshot("testsCatedra/capturas/test_TemperaturasFallido.png")
        assert not botonTemperatura.is_enabled()

def test_Temperaturas():
        """Test de visualizacion de la ventana de temperatura"""
        botonTemperatura = driver.find_element(By.ID,"grafica")
        botonTemperatura.click()
        driver.save_screenshot("testsCatedra/capturas/test_Temperaturas.png")
        assert botonTemperatura.is_enabled()

def test_IncidenciasFallido():
        """Test de visualizacion de la ventana de temperatura"""
        botonIncidencias = driver.find_element(By.ID,"auricular")
        botonIncidencias.click()
        driver.save_screenshot("testsCatedra/capturas/test_IncidenciasFallido.png")
        assert not botonIncidencias.is_enabled()

def test_Incidencias():
        """Test de visualizacion de la ventana de temperatura"""
        botonIncidencias = driver.find_element(By.ID,"auricular")
        botonIncidencias.click()
        driver.save_screenshot("testsCatedra/capturas/test_Incidencias.png")
        assert botonIncidencias.is_enabled()

def test_InputIncidenciasFallido():
        """Test del input de incidencias"""
        inputIncidencias = driver.find_element(By.ID, "select-incidencia")
        select = Select(inputIncidencias)
        select.select_by_visible_text("Avería del motor")
        driver.save_screenshot("testsCatedra/capturas/test_InputIncidenciasFallido.png")
        table = driver.find_element(By.ID, "table_options3").get_attribute("style")
        assert table == "block;"
def test_InputIncidencias():
        """Test del input de incidencias"""
        inputIncidencias = driver.find_element(By.ID, "select-incidencia")
        select = Select(inputIncidencias)
        select.select_by_visible_text("Avería del motor")
        driver.save_screenshot("testsCatedra/capturas/test_InputIncidencias.png")
        table = driver.find_element(By.ID, "table_options3").get_attribute("style")
        assert table == "display: block;"

def teardown_module():
        driver.quit()

