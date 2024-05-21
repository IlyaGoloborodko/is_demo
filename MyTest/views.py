from django.shortcuts import render
from django.test import Client

import requests

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.its_utils.app_get_params import get_params_from_sources


@main_auth(on_cookies=True)
@get_params_from_sources
def main(request):
    but = request.bitrix_user_token

    PORTAL_URL: str = "https://b1624879.bi.bitrix24.ru"
    # LOGIN_URL: str = "https://it-solution.bitrix24.ru/"
    LOGIN_URL = "https://it-solution.bitrix24.ru/bitrix/services/main/ajax.php?action=biconnector.dashboard.getEditUrl"
    METHOD: str = "api/v1/sqllab/execute/"

    BASE_URL = f"{PORTAL_URL}/{METHOD}"

    payload = {
        "client_id": "tbYM4OMjD",
        "database_id": 1,
        "json": True,
        "runAsync": False,
        "schema": "bitrix24",
        "sql": "SELECT *\nFROM crm_activity;",
        "sql_editor_id": "327",
        "tab": "Untitled Query 1",
        "tmp_table_name": "",
        "select_as_cta": False,
        "ctas_method": "TABLE",
        "queryLimit": 1000,
        "expand_data": True
    }

    # https://github.com/apache/superset/issues/16398

    client = requests.session()
    client.get(LOGIN_URL)

    cookies = client.cookies.get_dict()

    response = requests.post(BASE_URL)

    csrf = 'IjE1NzA5MmI0YTY3M2E0OTBiYmU0OTMyYjYyNWQ0NGU4YzVjZDZiYjAi.ZjAjdA.fWgYqZXVrXRcAXhX5F9XajfGTvk'

    headers = {'accept': 'application/json',
               'X-Csrftoken': csrf
               }
    response = requests.post(BASE_URL, headers=headers, json=payload)
    return render(request, 'test.html')
