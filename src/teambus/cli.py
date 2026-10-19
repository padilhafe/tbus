import typer

from teambus import __version__

app = typer.Typer(help="Team Bus CLI.", no_args_is_help=True)
db_app = typer.Typer(help="Banco de dados (migrations etc.).", no_args_is_help=True)
admin_app = typer.Typer(help="Administração (projetos, tokens etc.).", no_args_is_help=True)
app.add_typer(db_app, name="db")
app.add_typer(admin_app, name="admin")


@app.command()
def version() -> None:
    """Imprime a versão do Team Bus."""
    typer.echo(__version__)


if __name__ == "__main__":
    app()
