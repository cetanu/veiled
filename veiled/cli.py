import typer
from pathlib import Path
from cryptography.fernet import Fernet

app = typer.Typer()
colors = typer.colors


def green(msg):
    return typer.style(msg, fg=colors.GREEN)


def red(msg):
    return typer.style(msg, fg=colors.RED)


@app.command()
def encrypt(secret: str, key: str):
    suite = Fernet(key)
    typer.echo(suite.encrypt(secret.encode()))


@app.command()
def encrypt_file(path: Path, key: str, output: Path):
    suite = Fernet(key)
    content = suite.encrypt(path.read_bytes())
    typer.echo(green("Read plaintext from {path}"))
    output.write_bytes(content)
    typer.echo(green("Wrote secret to {output}"))


@app.command()
def decrypt(secret: str, key: str):
    suite = Fernet(key)
    typer.echo(suite.decrypt(secret.encode()))


@app.command()
def decrypt_file(path: Path, key: str, output: Path):
    suite = Fernet(key)
    content = suite.decrypt(path.read_bytes())
    typer.echo(green("Read secret from {path}"))
    output.write_bytes(content)
    typer.echo(green("Wrote plaintext to {output}"))


@app.command()
def generate_key():
    typer.echo(Fernet.generate_key().decode())


def run():
    app()
