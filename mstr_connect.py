from mstrio.connection import Connection
from mstrio.server import Environment
from mstrio.project_objects import list_reports, Report

from mstrio.types import ObjectTypes
from mstrio.object_management import list_objects, list_folders, get_predefined_folder_contents, PredefinedFolders

url = 'https://env-270933.customer.cloud.microstrategy.com/MicroStrategyLibrary/api/'
mstr_username = 'mstr'
mstr_password = 'kcTCSvc5RGG7'
project_name = 'MicroStrategy Tutorial'


def get_connection():
    conn = Connection(base_url=url, username=mstr_username, password=mstr_password, login_mode=1,
                      project_name=project_name)
    return conn


def search_report(connection, report_name):
    rep = list_reports(connection, name_begins=report_name)
    return rep


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
    return attr_elements
