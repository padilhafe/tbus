from httpx import ASGITransport, AsyncClient
from typer.testing import CliRunner

from teambus import __version__
from teambus.api.app import create_app
from teambus.cli import app as cli_app
from teambus.config import Settings


async def test_healthz() -> None:
    transport = ASGITransport(app=create_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "version": "0.1.0"}
    assert __version__ == "0.1.0"


def test_cli_version() -> None:
    result = CliRunner().invoke(cli_app, ["version"])
    assert result.exit_code == 0
    assert result.output.strip() == __version__


def test_settings_defaults(monkeypatch) -> None:
    for name in ("DATABASE_URL", "BLOCKED_CIDRS", "BLOCKED_HOST_SUFFIXES"):
        monkeypatch.delenv(f"TEAMBUS_{name}", raising=False)
    s = Settings(_env_file=None)
    assert s.database_url == "postgresql://teambus:teambus@127.0.0.1:55432/teambus"
    assert s.session_max_hours == 24
    assert s.claim_sweep_seconds == 60
    assert s.blocked_cidrs == []
    assert s.blocked_host_suffixes == []


def test_settings_list_from_env(monkeypatch) -> None:
    monkeypatch.setenv("TEAMBUS_BLOCKED_CIDRS", "10.0.0.0/8,172.16.0.0/12")
    monkeypatch.setenv("TEAMBUS_BLOCKED_HOST_SUFFIXES", '[".internal", ".lan"]')
    s = Settings(_env_file=None)
    assert s.blocked_cidrs == ["10.0.0.0/8", "172.16.0.0/12"]
    assert s.blocked_host_suffixes == [".internal", ".lan"]
