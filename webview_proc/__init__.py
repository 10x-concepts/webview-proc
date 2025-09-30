"""Package for managing pywebview windows in a separate process."""

from __future__ import annotations

from .webview_proc import WebViewProcess

try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0+unknown'  # fallback for dev envs
__all__ = ['WebViewProcess']
