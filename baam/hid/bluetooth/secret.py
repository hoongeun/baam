import binascii
import json
from typing import Dict, Any, Tuple


class Secret:
    def save(self, keys: Dict[Tuple[str, bytes], Any]):
        with open("keys.json", "w") as file:
            secret = [
                (sec_type, binascii.b2a_base64(key), binascii.b2a_base64(value))
                for (sec_type, key), value in keys.items()
            ]
            json.dump(secret, file)

    def load(self) -> Dict[Tuple[str, bytes], Any]:
        try:
            with open("keys.json", "r") as file:
                secret = json.load(file)
                return { (key[0], binascii.a2b_base64(key[1])): binascii.a2b_base64(value) for key, value in secret.items() }
        except Exception as e:
            return {}
