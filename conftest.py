
import datetime
import pytest
from py._xmlgen import *

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

def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append("<div class='empty log'>No log output captured.</div>")