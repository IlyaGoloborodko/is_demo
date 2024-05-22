from integration_utils.bitrix24.bitrix_token import BitrixToken

from settings import HOOK_TOKEN, APP_SETTINGS


def get_bitrix_token():
    return BitrixToken(APP_SETTINGS.portal_domain, web_hook_auth=HOOK_TOKEN)