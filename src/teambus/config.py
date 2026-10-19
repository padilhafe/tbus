"""Configuração via variáveis de ambiente (prefixo TEAMBUS_). Nomes de campo são contrato."""

import json
from functools import lru_cache
from typing import Annotated, Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


def _split_list(value: Any) -> Any:
    """Aceita lista, JSON (`["a","b"]`) ou CSV (`a,b`) vindo do ambiente."""
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return []
        if raw.startswith("["):
            return json.loads(raw)
        return [item.strip() for item in raw.split(",") if item.strip()]
    return value


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TEAMBUS_", env_file=".env", extra="ignore")

    database_url: str = "postgresql://teambus:teambus@127.0.0.1:55432/teambus"
    session_max_hours: int = 24
    claim_sweep_seconds: int = 60
    blocked_cidrs: Annotated[list[str], NoDecode] = []
    blocked_host_suffixes: Annotated[list[str], NoDecode] = []

    @field_validator("blocked_cidrs", "blocked_host_suffixes", mode="before")
    @classmethod
    def _parse_list(cls, value: Any) -> Any:
        return _split_list(value)


@lru_cache
def get_settings() -> Settings:
    return Settings()
