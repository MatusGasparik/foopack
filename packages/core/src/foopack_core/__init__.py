from importlib.metadata import PackageNotFoundError, version

__all__ = ["hello"]

try:
    __version__ = version("foopack-core")
except PackageNotFoundError:
    __version__ = "unknown"


def hello():
    return "hello from foopack-core"
