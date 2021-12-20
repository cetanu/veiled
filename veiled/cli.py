from veiled import __version__
from pathlib import Path
from typing import Callable, MutableMapping, Optional, Any

import yaml
import typer
from cryptography.fernet import Fernet

app = typer.Typer()

KEY = typer.Argument(default=..., envvar=["VEILED_ENCRYPTION_KEY", "bamboo_veiled_encryption_key"])


@app.command()
def version() -> None:
    typer.echo(__version__)


@app.command()
def encrypt(secret: str, key: str = KEY) -> None:
    suite = Fernet(key)
    typer.echo(suite.encrypt(secret.encode()))


@app.command()
def decrypt(secret: str, key: str = KEY) -> None:
    suite = Fernet(key)
    typer.echo(suite.decrypt(secret.encode()))


def veil_file(
    mode: str, path: Path, key: str = KEY, output: Optional[Path] = None
) -> None:
    src, dst = "plaintext", "secret"
    if mode == "encrypt":
        src, dst == dst, src

    suite = Fernet(key)
    method = getattr(suite, mode)

    content = method(path.read_bytes())
    typer.echo(f"Read {src} from {path}")
    if output is None:
        output = path
    output.write_bytes(content)
    typer.echo(f"Wrote {dst} to {output}")


@app.command()
def encrypt_file(path: Path, key: str = KEY, output: Optional[Path] = None) -> None:
    veil_file("encrypt", path, key, output)


@app.command()
def decrypt_file(path: Path, key: str = KEY, output: Optional[Path] = None) -> None:
    veil_file("decrypt", path, key, output)


def walk_and_veil(
    structure: MutableMapping[Any, Any], crypto: Callable[[bytes], bytes]
) -> None:
    # The YAML is expected to contain a key:value structure
    for k, v in structure.items():
        # Ignore non-strings
        if isinstance(v, str):
            v = v.encode()
            structure[k] = crypto(v).decode()
        if isinstance(v, MutableMapping):
            walk_and_veil(v, crypto)


def veil_yaml(
    mode: str, path: Path, key: str = KEY, output: Optional[Path] = None
) -> None:
    src, dst = "plaintext", "secret"
    if mode == "encrypt":
        src, dst == dst, src

    suite = Fernet(key)
    method = getattr(suite, mode)

    y = yaml.safe_load(path.read_text())
    typer.echo(f"Read {src} from {path}")
    walk_and_veil(y, method)
    content = yaml.safe_dump(y)

    if output is None:
        output = path
    output.write_text(content)
    typer.echo(f"Wrote {dst} to {output}")


@app.command()
def decrypt_yaml(path: Path, key: str = KEY, output: Optional[Path] = None) -> None:
    veil_yaml("decrypt", path, key, output)


@app.command()
def encrypt_yaml(path: Path, key: str = KEY, output: Optional[Path] = None) -> None:
    veil_yaml("encrypt", path, key, output)


@app.command()
def generate_key() -> None:
    typer.echo(Fernet.generate_key().decode())


def run() -> None:
    app()
