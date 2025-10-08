import multiprocessing
import os
import tempfile
import threading
import time
import traceback
from contextlib import nullcontext
from functools import partial
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest import mock

import pytest
import webview
from webview import WebViewException

from webview_proc import WebViewProcess


def test_start_real_process_without_webview_on_close(monkeypatch):
    closed = threading.Event()

    def dummy_wait_for_window(p):
        assert p is proc

    def on_close():
        closed.set()

    monkeypatch.setattr(
        'webview_proc.webview_proc.WebViewProcess._wait_for_window',
        dummy_wait_for_window,
    )

    proc = WebViewProcess(
        url='http://test',
        title='Test',
        on_close=on_close,
    )
    proc.start()
    assert not closed.is_set()
    proc.close()
    proc.join()
    assert proc.process is None
    assert not proc.is_alive()
    closed.wait(timeout=5)
    assert closed.is_set()


def mock_webview_ops(event, method, return_value, *args, **kwargs):
    try:
        m = mock.patch(method, return_value=return_value).start()
        event.set()

        wait_for_call(m)

        if m.call_count != 1:
            os._exit(-1)

        if m.mock_calls[0].args != args or m.mock_calls[0].kwargs != kwargs:
            os._exit(-2)
    except Exception:
        traceback.print_exc()
        os._exit(-3)


def wait_for_call(m, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if m.call_count:
            break
        time.sleep(0.1)


def test_set_title():
    event = multiprocessing.Event()
    proc = WebViewProcess(
        url='http://test',
        title='Test',
        func=partial(
            mock_webview_ops, event, 'webview.Window.set_title', None, 'test_title'
        ),
    )
    proc.start()
    event.wait()
    assert proc.set_title('test_title') is None
    proc.close()
    assert proc.join() == 0


def test_evaluate_javascript():
    event = multiprocessing.Event()
    proc = WebViewProcess(
        url='http://test',
        title='Test',
        func=partial(
            mock_webview_ops, event, 'webview.Window.evaluate_js', 'js result', '1+1'
        ),
    )
    proc.start()
    event.wait()
    result = proc.evaluate_javascript('1+1')
    assert result == 'js result'
    proc.close()
    assert proc.join() == 0


def test_resize():
    event = multiprocessing.Event()
    proc = WebViewProcess(
        url='http://test',
        title='Test',
        func=partial(mock_webview_ops, event, 'webview.Window.resize', None, 800, 600),
    )
    proc.start()
    event.wait()
    assert proc.resize(800, 600) is None
    proc.close()
    assert proc.join() == 0


def test_toggle_fullscreen():
    event = multiprocessing.Event()
    proc = WebViewProcess(
        url='http://test',
        title='Test',
        func=partial(mock_webview_ops, event, 'webview.Window.toggle_fullscreen', None),
    )
    proc.start()
    event.wait()
    assert proc.toggle_fullscreen() is None
    proc.close()
    assert proc.join() == 0


def test_set_maximized():
    event = multiprocessing.Event()
    proc = WebViewProcess(
        url='http://test',
        title='Test',
        func=partial(mock_webview_ops, event, 'webview.Window.maximize', None),
    )
    proc.start()
    event.wait()
    assert proc.set_maximized(True) is None
    proc.close()
    assert proc.join() == 0


def test_set_restored():
    event = multiprocessing.Event()
    proc = WebViewProcess(
        url='http://test',
        title='Test',
        func=partial(mock_webview_ops, event, 'webview.Window.restore', None),
    )
    proc.start()
    event.wait()
    assert proc.set_maximized(False) is None
    proc.close()
    assert proc.join() == 0


def test_pick_file():
    event = multiprocessing.Event()
    proc = WebViewProcess(
        url='http://test',
        title='Test',
        func=partial(
            mock_webview_ops,
            event,
            'webview.Window.create_file_dialog',
            'file.txt',
            dialog_type=webview.FileDialog.OPEN,
            file_types=['txt (*.txt)'],
            allow_multiple=False,
        ),
    )
    proc.start()
    event.wait()
    result = proc.pick_file(file_types=['txt'], multiple=False)
    assert result == 'file.txt'
    proc.close()
    assert proc.join() == 0


def test_pick_folder():
    event = multiprocessing.Event()
    proc = WebViewProcess(
        url='http://test',
        title='Test',
        func=partial(
            mock_webview_ops,
            event,
            'webview.Window.create_file_dialog',
            'folder',
            dialog_type=webview.FileDialog.FOLDER,
            file_types=[],
            allow_multiple=False,
        ),
    )
    proc.start()
    event.wait()
    result = proc.pick_folder()
    assert result == 'folder'
    proc.close()
    assert proc.join() == 0


@pytest.mark.parametrize('data', ['data', b'data', (), Path])
@pytest.mark.parametrize('return_value', [True, False])
def test_save_file(data, return_value):
    event = multiprocessing.Event()
    directory = tempfile.gettempdir()
    with (
        tempfile.NamedTemporaryFile(dir=directory) as d,
        NamedTemporaryFile(dir=directory) as f,
    ):
        if data is Path:
            data = Path(d.name)
            data.write_bytes(b'data')
        filename = os.path.basename(f.name)
        proc = WebViewProcess(
            url='http://test',
            title='Test',
            func=partial(
                mock_webview_ops,
                event,
                'webview.Window.create_file_dialog',
                filename if return_value else None,
                dialog_type=webview.FileDialog.SAVE,
                save_filename=filename,
                directory=directory,
            ),
        )
        proc.start()
        event.wait()
        with (
            nullcontext()
            if not return_value or data != ()
            else pytest.raises(WebViewException)
        ):
            result = proc.save_file(data, directory=directory, file_name=filename)
            assert result is return_value
        proc.close()
        assert proc.join() == 0
        if not return_value or data == ():
            return
        if isinstance(data, str):
            with open(f.name) as saved:
                assert saved.read() == data
        elif isinstance(data, (bytes, bytearray, memoryview)):
            with open(f.name, 'rb') as saved:
                assert saved.read() == data
        else:
            assert isinstance(data, Path)
            with open(f.name, 'rb') as saved:
                assert saved.read() == data.open('rb').read()
