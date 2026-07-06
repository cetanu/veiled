import os
import yaml
from pathlib import Path
from typer.testing import CliRunner
from cryptography.fernet import Fernet

from veiled.cli import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.stdout.strip() != ""


def test_generate_key():
    result = runner.invoke(app, ["generate-key"])
    assert result.exit_code == 0
    key = result.stdout.strip()
    # verify it's a valid fernet key
    Fernet(key)


def test_encrypt_decrypt_string():
    key = Fernet.generate_key().decode()
    os.environ["VEILED_ENCRYPTION_KEY"] = key
    
    secret_message = "hello world"
    
    # Encrypt
    encrypt_result = runner.invoke(app, ["encrypt", secret_message])
    assert encrypt_result.exit_code == 0
    encrypted_message = encrypt_result.stdout.strip()
    
    assert encrypted_message != secret_message
    
    # Decrypt
    decrypt_result = runner.invoke(app, ["decrypt", encrypted_message])
    assert decrypt_result.exit_code == 0
    decrypted_message = decrypt_result.stdout.strip()
    
    assert decrypted_message == secret_message


def test_encrypt_decrypt_file(tmp_path: Path):
    key = Fernet.generate_key().decode()
    os.environ["VEILED_ENCRYPTION_KEY"] = key
    
    file_path = tmp_path / "secret.txt"
    file_path.write_text("my super secret file content")
    
    # Encrypt
    encrypt_result = runner.invoke(app, ["encrypt-file", str(file_path)])
    assert encrypt_result.exit_code == 0
    
    encrypted_content = file_path.read_text()
    assert encrypted_content != "my super secret file content"
    
    # Decrypt
    decrypt_result = runner.invoke(app, ["decrypt-file", str(file_path)])
    assert decrypt_result.exit_code == 0
    
    decrypted_content = file_path.read_text()
    assert decrypted_content == "my super secret file content"


def test_encrypt_decrypt_yaml(tmp_path: Path):
    key = Fernet.generate_key().decode()
    os.environ["VEILED_ENCRYPTION_KEY"] = key
    
    yaml_path = tmp_path / "config.yaml"
    data = {
        "user": "admin",
        "nested": {
            "password": "supersecretpassword",
            "number": 123  # Should remain unencrypted as it's not a string
        }
    }
    yaml_path.write_text(yaml.dump(data))
    
    # Encrypt
    encrypt_result = runner.invoke(app, ["encrypt-yaml", str(yaml_path)])
    assert encrypt_result.exit_code == 0
    
    encrypted_data = yaml.safe_load(yaml_path.read_text())
    assert encrypted_data["user"] != "admin"
    assert encrypted_data["nested"]["password"] != "supersecretpassword"
    assert encrypted_data["nested"]["number"] == 123
    
    # Decrypt
    decrypt_result = runner.invoke(app, ["decrypt-yaml", str(yaml_path)])
    assert decrypt_result.exit_code == 0
    
    decrypted_data = yaml.safe_load(yaml_path.read_text())
    assert decrypted_data["user"] == "admin"
    assert decrypted_data["nested"]["password"] == "supersecretpassword"
    assert decrypted_data["nested"]["number"] == 123
