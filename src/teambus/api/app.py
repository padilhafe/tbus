from fastapi import FastAPI

from teambus import __version__


def create_app() -> FastAPI:
    app = FastAPI(title="Team Bus", version=__version__)

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    return app
