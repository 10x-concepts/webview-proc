from unittest.mock import MagicMock, patch

import pytest

from webview_proc import (
    WebViewProcess,
)
from webview_proc.webview_proc import (
    Response,
    EvaluateJavascriptRequest,
    PingRequest,
    ResizeRequest,
    SaveFileRequest,
    SetMaximizedRequest,
    SetTitleRequest,
    ToggleFullscreenRequest,
)


@pytest.fixture
def webview_proc():
    proc = WebViewProcess(url='http://test', title='Test')
    proc._is_alive = True
    proc.parent_conn = MagicMock()
    return proc


def test_send_command_success(webview_proc):
    webview_proc.parent_conn.recv.side_effect = [
        Response(result='ok')
    ]
    result = webview_proc._send_command(PingRequest(request_id=0))
    assert result == 'ok'
    webview_proc.parent_conn.send.assert_called_once()


def test_send_command_error(webview_proc):
    webview_proc.parent_conn.recv.side_effect = [
        Response(error='fail')
    ]
    with patch('webview_proc.webview_proc.WebViewException') as exc:
        exc.side_effect = Exception('fail')
        with pytest.raises(Exception, match='fail'):
            webview_proc._send_command(PingRequest(request_id=0))


def test_wait_for_window_success(webview_proc):
    webview_proc.parent_conn.recv.side_effect = [
        Response(request_id=1, result=True)
    ]
    webview_proc._wait_for_window()
    webview_proc.parent_conn.send.assert_called_once()


def test_wait_for_window_error(webview_proc):
    webview_proc.parent_conn.recv.side_effect = [
        Response(request_id=0, error='init fail')
    ]
    with pytest.raises(RuntimeError, match='init fail'):
        webview_proc._wait_for_window()


def test_resize(webview_proc):
    with patch.object(webview_proc, '_send_command') as send_cmd:
        webview_proc.resize(800, 600)
        send_cmd.assert_called_once()
        req = send_cmd.call_args[0][0]
        assert isinstance(req, ResizeRequest)
        assert req.width == 800 and req.height == 600


def test_set_title(webview_proc):
    with patch.object(webview_proc, '_send_command') as send_cmd:
        webview_proc.set_title('NewTitle')
        send_cmd.assert_called_once()
        req = send_cmd.call_args[0][0]
        assert isinstance(req, SetTitleRequest)
        assert req.title == 'NewTitle'


def test_toggle_fullscreen(webview_proc):
    with patch.object(webview_proc, '_send_command') as send_cmd:
        webview_proc.toggle_fullscreen()
        send_cmd.assert_called_once()
        req = send_cmd.call_args[0][0]
        assert isinstance(req, ToggleFullscreenRequest)


def test_set_maximized(webview_proc):
    with patch.object(webview_proc, '_send_command') as send_cmd:
        webview_proc.set_maximized(True)
        send_cmd.assert_called_once()
        req = send_cmd.call_args[0][0]
        assert isinstance(req, SetMaximizedRequest)
        assert req.maximized is True


def test_pick_file_multiple(webview_proc):
    with patch.object(webview_proc, '_send_command', return_value=['a.txt', 'b.txt']):
        result = webview_proc.pick_file(file_types=['txt'], multiple=True)
        assert result == ['a.txt', 'b.txt']


def test_pick_file_single(webview_proc):
    with patch.object(webview_proc, '_send_command', return_value=['a.txt']):
        result = webview_proc.pick_file(file_types=['txt'], multiple=False)
        assert result == 'a.txt'


def test_save_file(webview_proc):
    with patch.object(webview_proc, '_send_command', return_value=True) as send_cmd:
        result = webview_proc.save_file('data', 'file.txt')
        assert result is True
        req = send_cmd.call_args[0][0]
        assert isinstance(req, SaveFileRequest)
        assert req.file_contents == 'data'
        assert req.file_name == 'file.txt'


def test_evaluate_javascript(webview_proc):
    with patch.object(
        webview_proc, '_send_command', return_value='js_result'
    ) as send_cmd:
        result = webview_proc.evaluate_javascript('1+1')
        assert result == 'js_result'
        req = send_cmd.call_args[0][0]
        assert isinstance(req, EvaluateJavascriptRequest)
        assert req.js_code == '1+1'
