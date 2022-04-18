from mstrio.connection import Connection
from mstrio.project_objects import list_reports, Report, list_documents

import dotenv

import os


dotenv.load_dotenv('keys.env')

url = os.environ.get('SERVER_LINK') + '/MicroStrategyLibrary/api/'
mstr_username = os.environ.get('LOGIN')
mstr_password = os.environ.get('PASSWORD')
project_name = os.environ.get('PROJECT')


def get_connection():
    conn = Connection(base_url=url, username=mstr_username, password=mstr_password, login_mode=1,
                      project_name=project_name)
    return conn


def search_report(connection, report_name):
    reports = list_reports(connection, name_begins=report_name)
    return reports


def search_document(connection, doc_name):
    documents = list_documents(connection, doc_name)
    return documents

'''
def get_report(connection, report_id):
    my_report = Report(connection=connection, id=report_id, parallel=False)
    return my_report


def get_report_attributes(connection, report_id):
    report_attributes = Report(connection=connection, id=report_id, parallel=False).attributes
    return report_attributes


def get_report_metrics(connection, report_id):
    report_metrics = Report(connection=connection, id=report_id, parallel=False).metrics
    return report_metrics


def get_report_attr_elements(connection, report_id):
    attr_elements = Report(connection=connection, id=report_id, parallel=False).attr_elements
    return attr_elements'''
