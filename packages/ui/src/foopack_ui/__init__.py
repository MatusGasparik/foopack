from importlib.metadata import PackageNotFoundError, version

from foopack_core import hello as _h

__all__ = ["hello_ui"]

try:
    __version__ = version("foopack-ui")
except PackageNotFoundError:
    __version__ = "unknown"


def hello_ui():
    return _h() + " + ui"
