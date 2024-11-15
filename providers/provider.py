from abc import ABC, abstractmethod

import requests


class Provider(ABC):
    @staticmethod
    def get_text(s: str) -> str | None:
        r = requests.get(url=s)
        if r.status_code != 200:
            return None
        return r.text


    @abstractmethod
    def fetch(self, conf) -> list:
        pass
