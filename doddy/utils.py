from aiogram.utils.web_app import safe_parse_webapp_init_data
from django.core.exceptions import PermissionDenied
import json

from DoddyNFT.settings import TG_API_TOKEN


def get_init_data(auth):
    if auth is None:
        raise PermissionDenied
    try:
        print(auth)
        print(TG_API_TOKEN)
        data = safe_parse_webapp_init_data(token=TG_API_TOKEN, init_data=auth, _loads=json.loads)
    except ValueError:
        raise PermissionDenied
    return data
