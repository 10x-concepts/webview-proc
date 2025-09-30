# webview-proc

`webview-proc` is a Python package that simplifies running `pywebview` windows in a separate thread, enhancing stability and performance for desktop applications by isolating webview operations from the main thread. The `WebViewProcess` class provides a synchronous API for creating, managing, and communicating with webview windows, supporting operations like opening, closing, resizing, maximizing, toggling fullscreen, setting titles, handling file dialogs, and evaluating JavaScript. Ideal for hybrid applications combining web technologies with native interfaces, `webview-proc` offers a lightweight and extensible solution for Python developers.

## Features
- Run `pywebview` windows in a separate thread for crash isolation.
- Synchronous `WebViewProcess` class for simple, blocking operations.
- Comprehensive API for window operations: open, close, resize, maximize, fullscreen, set title, file dialogs, and JavaScript evaluation.
- Thread-safe communication for reliable control.
- Cross-platform support (Windows, macOS, Linux) with flexible `pywebview` GUI backends (e.g., Qt, GTK, Cocoa).
- Extensible for other webview engines (e.g., QtWebEngine, CEF).

## Installation
```bash
pip install webview-proc
```

## Basic Usage
```python
from webview_proc import WebViewProcess

# Create a webview process
webview = WebViewProcess(
    url="http://localhost:8000",
    title="My App",
    width=800,
    height=600,
    icon_path="path/to/icon.png",
)

# Start the webview in a separate thread
webview.start()

# Perform window operations
webview.set_title("New Title")
webview.resize(1000, 700)
webview.toggle_fullscreen()

# Open a file dialog
files = webview.pick_file(file_types=["pdf", "png"], multiple=True)

# Close the window
webview.close()

# Wait for the thread to terminate
webview.join()
```

## Why webview-proc?
`webview-proc` addresses the need for stable and isolated webview management in Python applications. By running `pywebview` windows in a separate thread, it prevents crashes from affecting the main application. The synchronous `WebViewProcess` class is ideal for scripts and applications requiring simple, blocking operations, and it integrates seamlessly with web servers (e.g., FastAPI). The package handles platform-specific quirks (e.g., main-thread requirements on macOS), making it suitable for desktop and hybrid web apps.

## Contributing
Contributions are welcome! Check out our [Contributing Guidelines](https://github.com/10x-concepts/webview-proc/blob/main/CONTRIBUTING.md) and [Issue Tracker](https://github.com/10x-concepts/webview-proc/issues) to get started.

## License
MIT License