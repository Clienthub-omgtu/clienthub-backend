from functools import lru_cache

from .default import Settings


@lru_cache
def get_settings():
    return Settings()
