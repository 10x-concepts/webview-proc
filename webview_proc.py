from __future__ import annotations

import pathlib
import sys
import threading
import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from multiprocessing import Pipe, Process
from typing import Any

from webview import (
    OPEN_DIALOG,
    SAVE_DIALOG,
    create_window,
    start,
)
from webview import (
    errors as webview_errors,
)

__all__ = ['WebViewProcess']

# --- Request/Response dataclasses ---


@dataclass
class Response:
    request_id: int = 0
    result: Any = None
    error: str | None = None


@dataclass
class Request(ABC):
    request_id: int

    @abstractmethod
    def process(self, window, conn) -> Response:
        """Process the request and return a Response object."""


@dataclass
class CloseRequest(Request):
    def process(self, window, conn) -> Response:
        window.destroy()
        return Response(request_id=self.request_id, result=True)


@dataclass
class ResizeRequest(Request):
    width: int
    height: int

    def process(self, window, conn) -> Response:
        window.resize(self.width, self.height)
        return Response(request_id=self.request_id, result=True)


@dataclass
class SetTitleRequest(Request):
    title: str

    def process(self, window, conn) -> Response:
        window.set_title(self.title)
        return Response(request_id=self.request_id, result=True)


@dataclass
class ToggleFullscreenRequest(Request):
    def process(self, window, conn) -> Response:
        window.toggle_fullscreen()
        return Response(request_id=self.request_id, result=True)


@dataclass
class SetMaximizedRequest(Request):
    maximized: bool

    def process(self, window, conn) -> Response:
        if self.maximized:
            window.maximize()
        else:
            window.restore()
        return Response(request_id=self.request_id, result=True)


@dataclass
class PickFileRequest(Request):
    file_types: list
    multiple: bool

    def process(self, window, conn) -> Response:
        file_types = (
            [f'{ext} (*.{ext})' for ext in self.file_types] if self.file_types else []
        )
        paths = window.create_file_dialog(
            dialog_type=OPEN_DIALOG,
            allow_multiple=self.multiple,
            file_types=file_types,
        )
        result = (
            [str(paths)]
            if isinstance(paths, str)
            else [str(p) for p in paths]
            if paths
            else []
        )
        return Response(request_id=self.request_id, result=result)


@dataclass
class SaveFileRequest(Request):
    file_contents: str | bytes
    file_name: str
    directory: str | None = None

    def process(self, window, conn) -> Response:
        destinations = window.create_file_dialog(
            dialog_type=SAVE_DIALOG,
            save_filename=self.file_name,
            directory=str(self.directory) if self.directory else '',
        )
        if not destinations:
            return Response(request_id=self.request_id, result=False)

        destination = destinations if isinstance(destinations, str) else destinations[0]
        if isinstance(self.file_contents, str):
            with open(destination, 'w', encoding='utf-8') as f:
                f.write(self.file_contents)
        else:
            with open(destination, 'wb') as f:
                f.write(self.file_contents)
        return Response(request_id=self.request_id, result=True)


@dataclass
class EvaluateJavascriptRequest(Request):
    js_code: str

    def process(self, window, conn) -> Response:
        result = window.evaluate_js(self.js_code)
        return Response(request_id=self.request_id, result=result)


@dataclass
class PingRequest(Request):
    def process(self, window, conn) -> Response:
        return Response(request_id=self.request_id, result=True)


# --- Main process class ---


@dataclass
class WebViewProcess:
    """Synchronous API for managing a pywebview window in the main thread of a separate process."""

    url: str
    title: str
    width: float | None = None
    height: float | None = None
    icon_path: str | pathlib.Path | None = None
    maximized: bool = False
    fullscreen: bool = False
    gui: str | None = None
    debug: bool = False
    http_server: t.Any | None = None

    process: Process | None = field(init=False, default=None)
    parent_conn: Any = field(init=False)
    child_conn: Any = field(init=False)
    _is_alive: bool = field(init=False, default=False)
    _request_id: int = field(init=False, default=0)

    def __post_init__(self):
        if self.icon_path:
            self.icon_path = pathlib.Path(self.icon_path)
        self.parent_conn, self.child_conn = Pipe()

    def _new_request_id(self) -> int:
        """Generate a new request ID for tracking requests."""
        self._request_id += 1
        return self._request_id

    def _run_webview(self, conn: t.Any) -> None:
        original_argv = sys.argv
        sys.argv = sys.argv[:1]
        try:
            window = create_window(
                title=self.title,
                url=self.url,
                width=int(self.width) if self.width else 800,
                height=int(self.height) if self.height else 600,
            )

            if self.maximized:
                window.maximize()
            if self.fullscreen:
                window.toggle_fullscreen()

            def handle_commands():
                while True:
                    try:
                        if not conn.poll(0.1):
                            continue
                        request = conn.recv()
                        if request is None:
                            break
                        try:
                            response = request.process(window, conn)
                        except Exception as e:
                            response = Response(
                                request_id=request.request_id, error=str(e)
                            )
                        conn.send(response)
                    except Exception:
                        break

            command_thread = threading.Thread(target=handle_commands, daemon=True)
            command_thread.start()

            start(
                gui=self.gui,
                debug=self.debug,
                icon=str(self.icon_path) if self.icon_path else None,
            )
        except Exception as e:
            conn.send(Response(error=str(e)))

        finally:
            sys.argv = original_argv
            conn.close()

    def _send_command(self, request_obj: Request) -> Any:
        if not self._is_alive:
            raise RuntimeError('Webview process is not running.')
        self.parent_conn.send(request_obj)
        while True:
            response = self.parent_conn.recv()
            if response.request_id == request_obj.request_id:
                if response.error:
                    raise webview_errors.WebViewException(response.error)
                return response.result

    def _wait_for_window(self) -> None:
        req = PingRequest(request_id=self._new_request_id())
        self.parent_conn.send(req)
        while True:
            response = self.parent_conn.recv()
            if not response.request_id:
                raise RuntimeError(f'Webview initialization failed: {response.error}')
            if response.request_id == req.request_id:
                if response.error:
                    continue
                if response.result is True:
                    return

    def start(self) -> None:
        if self.process is not None and self.process.is_alive():
            raise RuntimeError('Webview process is already running.')
        original_argv = sys.argv
        sys.argv = sys.argv[:1]
        try:
            self.process = Process(
                target=self._run_webview,
                args=(self.child_conn,),
                daemon=True,
            )
            self.process.start()
            self._is_alive = True
            self._wait_for_window()
        finally:
            sys.argv = original_argv

    def close(self) -> None:
        self._send_command(CloseRequest(request_id=self._new_request_id()))
        self._is_alive = False

    def resize(self, width: float, height: float) -> None:
        self._send_command(
            ResizeRequest(
                request_id=self._new_request_id(), width=int(width), height=int(height)
            )
        )

    def set_title(self, title: str) -> None:
        self._send_command(
            SetTitleRequest(request_id=self._new_request_id(), title=title)
        )

    def toggle_fullscreen(self) -> None:
        self._send_command(ToggleFullscreenRequest(request_id=self._new_request_id()))

    def set_maximized(self, maximized: bool) -> None:
        self._send_command(
            SetMaximizedRequest(request_id=self._new_request_id(), maximized=maximized)
        )

    def pick_file(
        self, *, file_types: t.Iterable[str] | None = None, multiple: bool = False
    ) -> list[str] | str | None:
        result = self._send_command(
            PickFileRequest(
                request_id=self._new_request_id(),
                file_types=list(file_types) if file_types else [],
                multiple=multiple,
            )
        )
        return result if multiple else result[0] if result else None

    def save_file(
        self,
        file_contents: str | bytes,
        file_name: str = 'Unnamed File',
        *,
        directory: str | pathlib.Path | None = None,
    ) -> bool:
        req = SaveFileRequest(
            request_id=self._new_request_id(),
            file_contents=file_contents,
            file_name=file_name,
            directory=str(directory) if directory else None,
        )
        result = self._send_command(req)
        return result

    def evaluate_javascript(self, js_code: str) -> t.Any:
        req = EvaluateJavascriptRequest(
            request_id=self._new_request_id(), js_code=js_code
        )
        result = self._send_command(req)
        return result

    def join(self) -> None:
        if self.process is not None and self._is_alive:
            self.process.join()
            self._is_alive = False

    def __del__(self) -> None:
        if self.process is not None and self._is_alive:
            self.close()
            self.process.terminate()
            self.process.join()
