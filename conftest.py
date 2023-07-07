
import datetime
import pytest, sys
import getpass
from py._xmlgen import *
sys.path.append('../')
import testsCatedra.test_HMI as test_HMI, tests.test_Selenium as test_Selenium, tests.test_Selenium2 as test_Selenium2
import inspect,ast
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
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
instrucciones = {
        "find_element": "Buscamos por ",
        "click" :"Pulsamos el boton",
        "save_screenshot": "Guardamos el screenshot",
        "is_enabled": "Comprobamos que este disponible",
        "Select" : "Convertimos el elemento en un selector",
        "select_by_visible_text": "Selecciona una opcion del select por su texto",
        "get_attribute": "Obtiene un atributo del elemento",
        
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

def obtener_explicacion_linea(str):
    if "assert" in str:
        return "Comprobamos la condicion"
    
    linea = str.split("(",1)
    if "." in linea[0]:
        instruccion = linea[0].split(".")[1]
    else:
        instruccion = linea[0].split("=")[1]
        instruccion= instruccion.replace(" ","")
        print(instruccion)
    valores = linea[1].split(")",1)[0]
    añadido=  linea[1].split(")",1)[1]
    if "." in añadido:

        if "(" in añadido:
            return obtener_str_linea([instruccion, valores, obtener_explicacion_linea(añadido)])
        else:
            return obtener_str_linea([instruccion,valores, añadido.split(".",1)[1]])
    return obtener_str_linea([instruccion,valores, " "])

def obtener_str_linea(array):
    if array[0] == " ": 
             return array[0]
    
    else:
        if array[0] in instrucciones:
            if array[0] == "find_element":
                argumentos = array[1].split(",",1)
                argumentos[0] = argumentos[0].split(".",1)[1]
                print(str(instrucciones[array[0]]) + str(argumentos[0]) +" el elemento "+ str(argumentos[1]) + str(obtener_str_linea(array[2])))
                return str(instrucciones[array[0]]) + str(argumentos[0]) +" el elemento "+ str(argumentos[1]) + str(obtener_str_linea(array[2]))
            else: 
                return str(instrucciones[array[0]])
        
    return ""

def get_test_info(test_function, ):
    return {
        'name': test_function.__name__,
        'docstring': test_function.__doc__,
        'source': obtener_codigo_fuente(test_function),
        'status': "",
        'captura': f"testsCatedra/capturas/{test_function.__name__}.png"
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

def assertStruc(esperado, captura):
    return html.tr(
    html.td(
        html.div(
                    html.div(html.table(
                        html.thead(
                    html.tr(
                        html.th(),
                        html.th("Resultados")
                    )
                ),
                html.tbody(
                    html.tr(
                        html.td("Resultado esperado"),
                        html.td(esperado)
                    ),
                    html.tr(
                        html.td("Resultado obtenido"),
                        html.td(esperado)
                    )
                ),style="float: left; color:black; margin:10px; background-color:rgb(228, 228, 228);"),), style="float: left; color:black;"),
                html.p("", style ="margin-top:100px;"),
                html.div(html.img(src= captura, style= " max-height: 200px; float: right; margin-right: 150px;"),style="margin-top:-100px; margin-bottom:20px; overflow: auto; max-height: 200px;"),
                style="overflow: auto; width: 100%;",
                class_="extr"
            )
)
def assertErrorStruc(valoreserror, solucionerror,obtenido, esperado, captura):
    return html.tr(
    html.td(
        html.div(
            html.div(
                    html.div(html.table(
                        html.thead(
                    html.tr(
                        html.th(),
                        html.th("Resultados")
                    )
                ),
                html.tbody(
                    html.tr(
                        html.td("Resultado esperado"),
                        html.td(esperado)
                    ),
                    html.tr(
                        html.td("Resultado obtenido"),
                        html.td(obtenido)
                    )
                ),style="float: left; color:black; margin:10px; background-color:rgb(228, 228, 228);"),), style="float: left; color:black;"),
                html.div(html.p(valoreserror, style = "color: red;"),html.p(solucionerror, style= "color: red;"),style = "margin-top:100px; max-width: 50vw;"),

                html.div(html.img(src= captura, style= " max-height: 200px; float: right; margin-right: 150px;"),style="margin-top:-100px; margin-bottom: 20px; overflow: auto; max-height: 200px;"),
                
                style="overflow: auto; width: 100%;",
                class_="extra"
            )
))




def pytest_exception_interact(node, call, report):
    global test_name
    if report.failed:  # Solo modificar los mensajes de error para los tests que fallaron
        exception_type, exception_value, traceback = call.excinfo._excinfo
        # Aquí puedes personalizar el mensaje de error según tus necesidades
        exception_value = str(exception_value).split("-")[0].split("Stacktrace:")[0]
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
    cells.insert(2,html.th('Title', class_= "sortable", col="title"))
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
    
    cells.insert(2,html.td(report.description, class_= "col-title"))
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
    for i, element in enumerate(summary):
        
        if ", " == element:
            summary.remove(element)
            summary.insert(i,html.br())

        if "span" in str(element):
            count += int(str(element).split(">")[1].split(" ")[0])
        

            
            
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
    summary.insert(2, html.h2("Filters"))

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    test_name = item.function.__name__
    test_info_dict[test_name] = get_test_info(item.function)

def pytest_html_results_table_html(report, data):
    test_name = report.nodeid.split("::")[-1]
    test_info = test_info_dict[test_name]
    status = get_status(report)
    test_info["status"]  = status
    if status == "Passed" or status =="Skipped" or status == "XFailed":
        del data[:]
        
        data.append(html.p(report.description +"\n", style = "font-weight: bold; font-size: 15px"))
        table = html.table(style ="width: 100%", class_ ="codigo")
        data.append(table)
        thead = html.thead()
        table.append(thead)
        tbody = html.tbody()
        table.append(tbody)
        thead.append(html.tr(html.th(test_info["name"], style= "font-size: 17px;")))
        first_line = True
        asserted = False
        i=0
        for line in test_info["source"]:
            if first_line:
                first_line = False
            elif "assert" in line:
                valores = obtener_valores(line)
                tbody.append(html.tr(html.td(html.div(html.div(str(testcounter)+ "."+ str(i)+ " "+str(obtener_explicacion_linea(line)), style ="float:left;  font-weight:bold;"), html.div(line,style="float:right; color: green;"), style="color: black;"))))
                tbody.append(assertStruc(valores[1],test_info["captura"]))            
                asserted =True
            else:
                tbody.append(html.tr(html.td(html.div(html.div(str(testcounter)+ "."+ str(i)+ " "+str(obtener_explicacion_linea(line)), style ="float:left;  font-weight:bold;"), html.div(line,style="float:right;"), style="color: black;"))))
            i+= 1
        if not asserted:
            tbody.append(html.tr(html.td(str(testcounter)+ "."+ str(i)+ " No hay assert", style="color: black")))
            tbody.append(assertStruc("Skipped",test_info["captura"]))    
    
    
    if status == "Failed" or status == "Error" or status == "XPassed":
        
        error = BeautifulSoup(str(data[0]), 'html.parser')
        
        error = error.find('div', class_ = 'log').get_text().split("@solucion")
        if error[0] == "No log output captured.":
            error =["UnexpectedPass", "Fallo desconocido, test deberia fallar"]
        if "<selenium.webdriver.remote.webelement.WebElement" in error[0]:
            error[0] = error[0].split("=")[0]
        valores = obtener_valores(error[0])
        del data[:]
        data.append(html.p(report.description +"\n",style = "font-weight: bold; font-size: 15px"))
        table = html.table(style ="width: 100%" , class_ ="codigo")
        data.append(table)
        thead = html.thead()
        table.append(thead)
        tbody = html.tbody()
        table.append(tbody)
        thead.append(html.tr(html.th(test_info["name"], style= "font-size: 17px;")))
        first_line = True
        asserted = False
        i=0
        
        for line in test_info["source"]:
            if first_line:
                first_line = False
            elif "assert" in line:
                tbody.append(html.tr(html.td(html.div(html.div(str(testcounter)+ "."+ str(i)+ " "+str(obtener_explicacion_linea(line)), style ="float:left; font-weight:bold;"), html.div(line,style="float:right; color: red;"), style="color: black;"))))
                tbody.append(assertErrorStruc(error[0],error[1], valores[0], valores[1],test_info["captura"]))  
                asserted = True
            else:
                tbody.append(html.tr(html.td(html.div(html.div(str(testcounter)+ "."+ str(i)+ " "+str(obtener_explicacion_linea(line)), style ="float:left; font-weight:bold;"), html.div(line,style="float:right;"), style="color: black;"))))
            i+=1

        if not asserted:
             tbody.append(html.tr(html.td(str(testcounter)+ "."+ str(i)+ " No hay assert",style="color: black")))
             tbody.append(assertErrorStruc(error[0],error[1], valores[0], valores[1]))  
    