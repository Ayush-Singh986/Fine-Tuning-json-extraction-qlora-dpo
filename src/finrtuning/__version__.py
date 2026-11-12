"""Version information for Finr-Tuning."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("finrtuning")
except PackageNotFoundError:
    __version__ = "0.1.0"

__all__ = ["__version__"]