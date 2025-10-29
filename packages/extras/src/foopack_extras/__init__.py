from importlib.metadata import PackageNotFoundError, version

from foopack_core import hello as _h

__all__ = ["hello_extras"]

try:
    __version__ = version("foopack-extras")
except PackageNotFoundError:
    __version__ = "unknown"


def hello_extras():
    return _h() + " + extras"
