import importlib.metadata

try:
    __version__ = importlib.metadata.version("veiled")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
