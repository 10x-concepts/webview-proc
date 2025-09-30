"""Demonstrate basic usage of the webview process API."""

import pathlib

from webview_proc import WebViewProcess


def demo():
    """Demonstrates basic usage of WebViewProcess."""
    webview = WebViewProcess(
        url='icon.jpg',
        title='Local Files',
        width=800,
        height=600,
        http_server=True,
        icon_path='icon.jpg',
    )

    # Start the webview in a separate thread
    webview.start()

    # Perform window operations
    input('Press Enter to set title...')
    webview.set_title('New Title')

    input('Press Enter to resize the window...')
    webview.resize(1000, 700)

    input('Press Enter to toggle fullscreen...')
    webview.toggle_fullscreen()

    input('Press Enter to maximize the window...')
    webview.set_maximized(True)

    # Pick a file
    input('Press Enter to pick a file...')
    picked = webview.pick_file(file_types=['txt', 'md'], multiple=False)
    print('Picked file:', picked)

    # Save a file
    input('Press Enter to save a file...')
    saved = webview.save_file('Hello, world!', 'hello.txt', directory=pathlib.Path('.'))
    print('File saved:', saved)

    # Evaluate JavaScript
    input('Press Enter to evaluate JavaScript...')
    result = webview.evaluate_javascript('2 + 2')
    print('JS result:', result)

    # Close the window
    input('Press Enter to close webview...')
    webview.close()

    # Wait for the thread to terminate
    webview.join()


if __name__ == '__main__':
    demo()
