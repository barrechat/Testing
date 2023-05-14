
import datetime
import pytest
from py._xmlgen import *
import test_HMI, test_Selenium, test_Selenium2
import inspect

modulos= [test_HMI,test_Selenium,test_Selenium2]

def obtener_codigo_fuente(func):
    archivo = inspect.getsourcefile(func)
    with open(archivo, 'r') as f:
        codigo = f.read()
    return codigo

def get_test_info(test_function):
    return {
        'name': test_function.__name__,
        'docstring': test_function.__doc__,
        'source': obtener_codigo_fuente(test_function),
        'result': '',
        'duration': 0,
        # Agrega aquí cualquier otra información que desees
    }
    

def pytest_configure(config):
    config._metadata['test_descriptions'] = {}

def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("Description"))
    cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.datetime.now(), class_="col-time"))
    cells.pop()

def pytest_html_report_title(report):
    report.title = "My very own title!"
def pytest_configure(config):
    config._metadata["foo"] = "bar"
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("foo: bar")])

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    global codigo 
    codigo = get_test_info(item.function)

def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.p("No log output captured."))
        data.append(html.p(codigo))