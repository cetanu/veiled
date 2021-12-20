veiled
======
A very thin CLI wrapper around `cryptography.fernet:Fernet` for symmetric encryption.

I made this to use in CI things, so I can keep encrypted secrets in my git repositories,
and have my build agents decrypt them using a centralized key.

installation
------------
`pip install veiled`

It's recommended to pin the install to a specific version

usage
-----
Use `--help` to view command-specific usage.

```
Usage: veil [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  decrypt
  decrypt-file
  decrypt-yaml
  encrypt
  encrypt-file
  encrypt-yaml
  generate-key
  version
```
