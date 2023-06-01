
import datetime
import pytest, sys
import getpass
from py._xmlgen import *
sys.path.append('../')
import tests.test_HMI as test_HMI, tests.test_Selenium as test_Selenium, tests.test_Selenium2 as test_Selenium2
import inspect,ast
from bs4 import BeautifulSoup
modulos= [test_HMI,test_Selenium,test_Selenium2]
test_info_dict ={}
errores = {
        "AssertionError": " \nFallo en el Assert: Comprobar valores en pagina web",
        "ValueError": " \nValor incorrecto en el test: Comprobar variables, argumentos y comparaciones",
        "TypeError": " \nTipo incorrecto: Comprobar variables, argumentos y comparaciones",
        "AttributeError": " \nAtributo inexistente: Revisar documentacion y código",
        "KeyError": " \nClave inexistente: Revisar documentación y diccionarios",
        "IndexError": " \nIndex inexistente: Verificar longitud de lista y bucles",
        "FileNotFoundError": " \nArchivo inexistente o fuera de alcance: Verificar path, nombre y permisos del archivo",
        "ImportError": " \nError al importar: Comprobar environment y un correcto import",
        "TimeoutError": " \nTiempo excedido: Verificar rendimiento y conectividad o ajusta el tiempo de la operación",
        "StopIteration": " \nIteraciones excedidas: Verificar que la estructura contenga elementos y sean validos",
        "WebDriverException": " \nProblemas de conexion: Comprobar que la pagina web esta en funcionamiento y las urls",
    }
numeroReporte = 0
testcounter = 0
with open ('numeroReporte.txt','r') as numero:
    contenido = numero.read()
    if contenido:
        numeroReporte = int(contenido)
    else: 
        numeroReporte = 1

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
        'status': ""
    }
def get_colores(str):
    if str == "Passed":
        return "green"
    elif str == "Error" or str == "Failed" or str == "XPassed":
        return "red"
    else: return "orange"
def get_status(report):
    if report.passed:
        if hasattr(report, "wasxfail"):
               
                return"XPassed"
        else:
                return "Passed"
    if report.failed:
        if getattr(report, "when", None) == "call":
                if hasattr(report, "wasxfail"):
                    return"XPassed"
                else:
                    return"Failed"
        else:
                return "Error"
    if report.skipped:
        if hasattr(report, "wasxfail"):
            return"XFailed"
        else:
            return "Skipped"
        
def obtener_valores(linea):
    if 'assert' in linea:
        if 'and' in linea:
            for parte in linea.split("assert")[1].split("and"):
                valores = parte.split("==")
        elif '==' in linea:
            valores = linea.split("assert")[1].split("==")
        else:
            valores = ["false","true"]
    else:
            valores = ["error","error"]
    return valores
## estructura detalles assert
def assertStruc(esperado):
    return html.tr(
    html.td(
        html.div("línea correcta", style="float: left; color:black"),
        html.div(
    html.div(
        html.p("Valores del Assert", style="font-size: 15px; margin-top: 0; text-align: center;font-weight: bold;"),
        html.div(
            html.div(
                        html.p("Esperado:", style="font-size: 10px; margin-top: 0; text-align: center;font-weight: bold;"),
                        html.div(
                            html.p(esperado, style="font-size: 10px;"),
                            style="width: 60px; height: 60px; margin-right: 5px; word-wrap: break-word; ",
                            class_="resultado"
                        ),
                        style="display: flex; justify-content: center; align-items: center; flex-direction: column;"
                    ),
                    html.div(
                        html.p("Obtenido:", style="font-size: 10px; margin-top: 0; text-align: center;font-weight: bold;"),
                        html.div(
                            html.p(esperado, style="font-size: 10px;"),
                            style="width: 60px; height: 60px; margin-left: 5px; word-wrap: break-word;",
                            class_="resultado"
                        ),
                        style="display: flex; justify-content: center; align-items: center; flex-direction: column;"
                    ),
                    style="display: flex; justify-content: center; align-items: center; border: 2px solid black; padding: 10px; text-align: center;"
                ),
                style="display: flex; justify-content: center; align-items: center; flex-direction: column;"
            ),
            style="float: center; display: flex; justify-content: center; align-items: center; "
        ),
        html.div(style="", class_="empty-div"),
        style="overflow: auto; width: 100%; ",
        class_="extra"
    )
)
def assertErrorStruc(valoreserror, solucionerror,obtenido, esperado):
    return html.tr(
    html.td(
        html.div(html.p(valoreserror),html.p(solucionerror), style="float: left; color:black; max-width: 33.33%"),
      
        html.div(
    html.div(
        html.p("Valores del Assert", style="font-size: 15px; margin-top: 0; text-align: center;font-weight: bold;"),
        html.div(
            html.div(
                        html.p("Esperado:", style="font-size: 10px; margin-top: 0; text-align: center;font-weight: bold;"),
                        html.div(
                            html.p(esperado, style="font-size: 10px;"),
                            style="width: 60px; height: 60px; margin-right: 5px; word-wrap: break-word; ",
                            class_="resultado"
                        ),
                        style="display: flex; justify-content: center; align-items: center; flex-direction: column;"
                    ),
                    html.div(
                        html.p("Obtenido:", style="font-size: 10px; margin-top: 0; text-align: center;font-weight: bold;"),
                        html.div(
                            html.p(obtenido, style="font-size: 10px;"),
                            style="width: 60px; height: 60px; margin-left: 5px; word-wrap: break-word;",
                            class_="resultado"
                        ),
                        style="display: flex; justify-content: center; align-items: center; flex-direction: column;"
                    ),
                    style="display: flex; justify-content: center; align-items: center; border: 2px solid black; padding: 10px; text-align: center;"
                ),
                style="display: flex; justify-content: center; align-items: center; flex-direction: column;"
            ),
            style="float: center; display: flex; justify-content: center; align-items: center; "
        ),
        html.div(style="", class_="empty-div"),
        style="overflow: auto; width: 100%; ",
        class_="extra"
    )
)


def pytest_exception_interact(node, call, report):
    if report.failed:  # Solo modificar los mensajes de error para los tests que fallaron
        exception_type, exception_value, traceback = call.excinfo._excinfo
        # Aquí puedes personalizar el mensaje de error según tus necesidades
        exception_value = str(exception_value).split("-")[0]
        if exception_type.__name__ in errores:
            custom_error_message = f"ERROR: {exception_type.__name__}: {exception_value}" +"@solucion"+ errores[exception_type.__name__] 
        else:
            custom_error_message = (f"ERROR: {exception_type.__name__}: {exception_value}") + "@solucion"+ ""

        report.longrepr = custom_error_message # Reemplazar el mensaje de error original

def pytest_configure(config):
    config._metadata['test_descriptions'] = {}

def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("Time", class_="sortable time", col="time"))
    cells.insert(0, html.th('#', class_="sortable int", col='int'))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    global testcounter
    cells.insert(2, html.td(datetime.datetime.now(), class_="col-time"))
    testcounter += 1
    if(testcounter>9):
        cells.insert(0, html.td("0"+str(testcounter), id = f'paso-{testcounter}'))
    elif(testcounter>99):
        cells.insert(0, html.td(""+str(testcounter), id = f'paso-{testcounter}'))
    elif(testcounter>0):
        cells.insert(0, html.td("00"+str(testcounter), id = f'paso-{testcounter}'))
    cells.pop()

def pytest_html_report_title(report):
    report.title = "Reporte de ensayo"

def pytest_configure(config):
    global numeroReporte
    numeroReporte = 1 + numeroReporte
    config._metadata["User"] = getpass.getuser()
    config._metadata["Numero Reporte"] = numeroReporte
    
    with open("numeroReporte.txt", "w") as numero:
        numero.write(str(numeroReporte))
    
def pytest_html_results_summary(prefix, summary, postfix):
    global test_name
    count = 0
    filtered = False
    for i, element in enumerate(summary):
        if "span" in str(element):
            count+= int(str(element).split(">")[1].split(" ")[0])
        
        if "input" in str(element) and not filtered:
            summary.insert(i, html.h2("Filters"))
            filtered = True
        
    prefix.extend([
    html.ul(
        [
            html.li(
                html.p(html.a(
                    f'Paso {i + 1}', href=f'#paso-{i + 1}', style="color: black"
                ), f' {test_info_dict[test]["status"]}', style=f'color: {get_colores(test_info_dict[test]["status"])}')
            )
            for i, test in enumerate(test_info_dict)
            
        ]
    )
])

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    test_name = item.function.__name__
    test_info = get_test_info(item.function)
        
    test_info_dict[test_name] = test_info


def pytest_html_results_table_html(report, data):
    test_name = report.nodeid.split("::")[-1]
    test_info = test_info_dict[test_name]
    status = get_status(report)
    test_info["status"]  = status
    if status == "Passed" or status =="Skipped" or status == "XFailed":
        del data[:]
        
        data.append(html.p(report.description +"\n"))
        table = html.table(style ="width: 100%", class_ ="codigo")
        data.append(table)
        thead = html.thead()
        table.append(thead)
        tbody = html.tbody()
        table.append(tbody)
        thead.append(html.tr(html.th(test_info["name"])))
        first_line = True
        asserted = False
        i=0
        for line in test_info["source"]:
            if first_line:
                first_line = False
            elif "assert" in line:
                valores = obtener_valores(line)
                tbody.append(html.tr(html.td(str(testcounter)+ "."+ str(i)+ " "+line, class_="col-result", style="color: black")))
                tbody.append(assertStruc(valores[1]))            
                asserted =True
            else:
                tbody.append(html.tr(html.td(str(testcounter)+ "."+ str(i)+ " "+line, style="color: black")))
            i+= 1
        if not asserted:
            tbody.append(html.tr(html.td(str(testcounter)+ "."+ str(i)+ " No hay assert", class_="col-result", style="color: black")))
            tbody.append(assertStruc("Skipped"))    
    
    
    if status == "Failed" or status == "Error" or status == "XPassed":
        
        error = BeautifulSoup(str(data[0]), 'html.parser')
        
        error = error.find('div', class_ = 'log').get_text().split("@solucion")
        if error[0] == "No log output captured.":
            error =["UnexpectedPass", "Fallo desconocido, test deberia fallar"]

        valores = obtener_valores(error[0])
        del data[:]
        data.append(html.p(report.description +"\n"))
        table = html.table(style ="width: 100%" , class_ ="codigo")
        data.append(table)
        thead = html.thead()
        table.append(thead)
        tbody = html.tbody()
        table.append(tbody)
        thead.append(html.tr(html.th(test_info["name"])))
        first_line = True
        asserted = False
        i=0
        if "WebDriverException" in error[0]:
            error[0] = error[0].split("(Session info:")[0]
        for line in test_info["source"]:
            if first_line:
                first_line = False
            elif "assert" in line:
                tbody.append(html.tr(html.td(str(testcounter)+ "."+ str(i)+ " "+line, class_="col-result", style="color: red")))
                print(error, valores, test_name)
                tbody.append(assertErrorStruc(error[0],error[1], valores[0], valores[1]))  
                asserted = True
            else:
                tbody.append(html.tr(html.td(str(testcounter)+ "."+ str(i)+ " "+line, style="color: black")))
            i+=1

        if not asserted:
             tbody.append(html.tr(html.td(str(testcounter)+ "."+ str(i)+ " No hay assert", class_="col-result", style="color: black")))
             tbody.append(assertErrorStruc(error[0],error[1], valores[0], valores[1]))  
    