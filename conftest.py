
import datetime
import pytest
from py._xmlgen import *
import test_HMI, test_Selenium, test_Selenium2
import inspect,ast

modulos= [test_HMI,test_Selenium,test_Selenium2]
test_info_dict ={}

def obtener_codigo_fuente(func):
    codigo_funcion = inspect.getsource(func)
    arbol_sintactico = ast.parse(codigo_funcion)
    cuerpo_funcion = ast.unparse(arbol_sintactico.body[0].body)
    lineas = cuerpo_funcion.split('\n')
    return lineas

def get_test_info(test_function):
    return {
        'name': test_function.__name__,
        'docstring': test_function.__doc__,
        'source': obtener_codigo_fuente(test_function),
        'result': "",
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
    test_name = item.function.__name__
    test_info_dict[test_name] = get_test_info(item.function)

def pytest_html_results_table_html(report, data):
   if report.passed:
    del data[:]
    data.append(html.p(report.description +"\n"))
    test_name = report.nodeid.split("::")[-1]
    test_info = test_info_dict[test_name]
    table = html.table(style ="width: 100%")
    data.append(table)
    thead = html.thead()
    table.append(thead)
    tbody = html.tbody()
    table.append(tbody)
    thead.append(html.tr(html.th(test_info["name"])))
    first_line = True

    for line in test_info["source"]:
        if first_line:
            first_line = False
        else:
            tbody.append(html.tr(html.td(line, class_="col-result", style="color: black")))
            tbody.append(html.tr(html.td("la linea es correcta", class_="extra")))

