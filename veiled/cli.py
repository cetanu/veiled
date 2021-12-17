import yaml
import typer
from typing import Dict, Any, MutableMapping
from pathlib import Path
from cryptography.fernet import Fernet

app = typer.Typer()


@app.command()
def encrypt(secret: str, key: str) -> None:
    suite = Fernet(key)
    typer.echo(suite.encrypt(secret.encode()))


@app.command()
def encrypt_file(path: Path, key: str, output: Path) -> None:
    suite = Fernet(key)
    content = suite.encrypt(path.read_bytes())
    typer.echo(f"Read plaintext from {path}")
    output.write_bytes(content)
    typer.echo(f"Wrote secret to {output}")


@app.command()
def decrypt(secret: str, key: str) -> None:
    suite = Fernet(key)
    typer.echo(suite.decrypt(secret.encode()))


@app.command()
def decrypt_file(path: Path, key: str, output: Path) -> None:
    suite = Fernet(key)
    content = suite.decrypt(path.read_bytes())
    typer.echo(f"Read secret from {path}")
    output.write_bytes(content)
    typer.echo(f"Wrote plaintext to {output}")


def walk_and_encrypt(structure: MutableMapping, crypto) -> None:
    # The YAML is expected to contain a key:value structure
    for k, v in structure.items():
        # Ignore non-strings
        if isinstance(v, str):
            v = v.encode()
            structure[k] = crypto(v).decode()
        if isinstance(v, MutableMapping):
            walk_and_encrypt(v, crypto)


def veil_yaml(mode: str, path: Path, key: str, output: Path) -> None:
    src, dst = "plaintext", "secret"
    if mode == "encrypt":
        src, dst == dst, src

    suite = Fernet(key)
    method = getattr(suite, mode)

    y = yaml.safe_load(path.read_text())
    typer.echo(f"Read secret from {path}")
    walk_and_encrypt(y, method)
    content = yaml.safe_dump(y)

    output.write_text(content)
    typer.echo(f"Wrote plaintext to {output}")


@app.command()
def decrypt_yaml(path: Path, key: str, output: Path) -> None:
    veil_yaml("decrypt", path, key, output)


@app.command()
def encrypt_yaml(path: Path, key: str, output: Path) -> None:
    veil_yaml("encrypt", path, key, output)


@app.command()
def generate_key() -> None:
    typer.echo(Fernet.generate_key().decode())


def run() -> None:
    app()
