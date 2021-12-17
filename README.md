veiled
======
A very thin CLI wrapper around `cryptography.fernet:Fernet` for symmetric encryption.

I made this to use in CI things, so I can keep encrypted secrets in my git repositories,
and have my build agents decrypt them using a centralized key.

