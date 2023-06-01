from selenium import webdriver
import pytest
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def test_passed():
        """test pasado"""
        assert True

def test_Failed():
        """test Fallado"""

        assert False
@pytest.mark.skip(reason="Motivo de salto")
def test_Skipped():
    """test skipeado"""
    # Código de prueba que no se ejecutará
    pass

@pytest.mark.xfail()
def test_Xfail():
    """test fallo esperado"""
    hola = 1+1
    assert False


@pytest.mark.xfail()
def test_Upasses():
    """test acierto inesperado"""
    adios = 2
    assert True