from authlib.jose import JsonWebKey, KeySet
from typing import Any


def create_json_web_key_set(jwks_dict: dict[str, Any]) -> KeySet:
    return JsonWebKey.import_key_set(jwks_dict)
