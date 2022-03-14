from mstrio.connection import Connection
from mstrio.server import Environment
from mstrio.project_objects import list_reports, Report

from mstrio.types import ObjectTypes
from mstrio.object_management import list_objects, list_folders, get_predefined_folder_contents, PredefinedFolders
# https://dashboard-temp/MicroStrategy/servlet/mstrWeb?evt=3010&src=mstrWeb.3010&loginReq=true&ServerAlias=10.191.2.88&mstrWeb=-2AAAADDX3ujwopszPc2vqk4N5i6g8gR9AQ2qJR4iwWe9VHkAP30grHo2*_SQ%3D%3D..2AAAADGZDSHmYweoMjyVh3kvUMRCxHHXUZTHiRnW8B5to_&welcome=*-1.*-1.0.0.0&Server=10.191.2.88&Port=0&Project=Business+Intelligence&
url = 'https://mstr-sand-web.corp.mvideo.ru/MicroStrategyLibrary/api/'
mstr_username = 'Administrator'
mstr_password = 'SAdm1792@'
project_name = 'Business Intelligence'
# http://dashboards.corp.mvideo.ru/MicroStrategy/servlet/mstrWeb

def get_connection():
    conn = Connection(base_url=url, username=mstr_username, password=mstr_password, login_mode=1,
                      project_name=project_name, ssl_verify=False)
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
